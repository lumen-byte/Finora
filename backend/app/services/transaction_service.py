import csv
import io
from typing import List, Optional
from uuid import UUID
from datetime import date
from dateutil import parser
from decimal import Decimal
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from backend.app.repositories.transaction_repository import TransactionRepository
from backend.app.repositories.account_repository import AccountRepository
from backend.app.repositories.category_repository import CategoryRepository
from backend.app.schemas.transaction import TransactionCreate, TransactionUpdate
from backend.app.models.transaction import Transaction
from backend.app.models.category import TransactionType
from backend.app.models.account import Account

class TransactionService:
    def __init__(self, session: Session):
        self.session = session
        self.transaction_repo = TransactionRepository(session)
        self.account_repo = AccountRepository(session)
        self.category_repo = CategoryRepository(session)

    def _update_balance(self, account: Account, type: TransactionType, amount: Decimal, reverse: bool = False):
        multiplier = Decimal('1') if type == TransactionType.INCOME else Decimal('-1')
        if reverse:
            multiplier *= Decimal('-1')
        account.current_balance += amount * multiplier

    def get_transaction(self, transaction_id: UUID, user_id: UUID) -> Transaction:
        transaction = self.transaction_repo.get(transaction_id, user_id)
        if not transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        return transaction

    def get_transactions(
        self,
        user_id: UUID,
        account_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
        type: Optional[TransactionType] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Transaction]:
        return self.transaction_repo.get_all(
            user_id=user_id, account_id=account_id, category_id=category_id,
            type=type, start_date=start_date, end_date=end_date, search=search, skip=skip, limit=limit
        )

    def create_transaction(self, user_id: UUID, transaction_in: TransactionCreate) -> Transaction:
        account = self.account_repo.get(transaction_in.account_id, user_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        
        if transaction_in.category_id:
            category = self.category_repo.get(transaction_in.category_id)
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
            if category.type != transaction_in.type:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category type mismatch")

        transaction = self.transaction_repo.create(user_id, transaction_in)
        self._update_balance(account, transaction.type, transaction.amount)
        
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def update_transaction(self, transaction_id: UUID, user_id: UUID, transaction_in: TransactionUpdate) -> Transaction:
        transaction = self.get_transaction(transaction_id, user_id)
        old_account_id = transaction.account_id
        old_type = transaction.type
        old_amount = transaction.amount
        
        # Get old account and reverse balance
        old_account = self.account_repo.get(old_account_id, user_id)
        self._update_balance(old_account, old_type, old_amount, reverse=True)
        
        # Validate new account if changing
        new_account_id = transaction_in.account_id if transaction_in.account_id else old_account_id
        if new_account_id != old_account_id:
            new_account = self.account_repo.get(new_account_id, user_id)
            if not new_account:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="New account not found")
        else:
            new_account = old_account

        # Apply new balance
        new_type = transaction_in.type if transaction_in.type else old_type
        new_amount = transaction_in.amount if transaction_in.amount is not None else old_amount
        self._update_balance(new_account, new_type, new_amount)

        # Validate category if changing
        new_category_id = transaction_in.category_id if transaction_in.category_id else transaction.category_id
        if new_category_id:
            category = self.category_repo.get(new_category_id)
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
            if category.type != new_type:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category type mismatch")

        transaction = self.transaction_repo.update(transaction, transaction_in)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def delete_transaction(self, transaction_id: UUID, user_id: UUID) -> None:
        transaction = self.get_transaction(transaction_id, user_id)
        account = self.account_repo.get(transaction.account_id, user_id)
        
        self._update_balance(account, transaction.type, transaction.amount, reverse=True)
        self.transaction_repo.delete(transaction)
        self.session.commit()

    async def import_csv(self, user_id: UUID, file: UploadFile) -> dict:
        content = await file.read()
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be UTF-8 encoded")
            
        reader = csv.DictReader(io.StringIO(text))
        expected_fields = ['date', 'description', 'merchant', 'amount', 'type', 'category', 'account']
        if not reader.fieldnames or not all(f in reader.fieldnames for f in expected_fields):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"CSV must contain headers: {', '.join(expected_fields)}")
            
        transactions_to_create = []
        errors = []
        
        # Pre-fetch user accounts and all categories for fast lookup
        accounts = {acc.name: acc for acc in self.account_repo.get_all(user_id)}
        categories = {cat.name: cat for cat in self.category_repo.get_all()}
        
        for i, row in enumerate(reader, start=2): # line 2 is first data row
            try:
                date_val = parser.parse(row['date']).date()
                amount_val = Decimal(row['amount'])
                type_val = TransactionType(row['type'].upper())
                
                account_name = row['account']
                if account_name not in accounts:
                    errors.append(f"Row {i}: Account '{account_name}' not found")
                    continue
                    
                category_name = row['category']
                category_id = None
                if category_name:
                    if category_name not in categories:
                        errors.append(f"Row {i}: Category '{category_name}' not found")
                        continue
                    cat = categories[category_name]
                    if cat.type != type_val:
                        errors.append(f"Row {i}: Category type mismatch. Expected {type_val}")
                        continue
                    category_id = cat.id
                    
                transactions_to_create.append(TransactionCreate(
                    account_id=accounts[account_name].id,
                    category_id=category_id,
                    type=type_val,
                    amount=amount_val,
                    description=row['description'],
                    merchant=row['merchant'] or None,
                    transaction_date=date_val
                ))
            except Exception as e:
                errors.append(f"Row {i}: Invalid data formatting ({str(e)})")

        if errors:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"errors": errors})
            
        count = 0
        for tx in transactions_to_create:
            self.create_transaction(user_id, tx)
            count += 1
            
        return {"message": f"Successfully imported {count} transactions"}
