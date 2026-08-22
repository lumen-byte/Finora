import sys
import os
import uuid
from decimal import Decimal
from datetime import date, timedelta
import random

# Add parent dir to path so we can import backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.db.session import SessionLocal
from backend.app.models.user import User
from backend.app.models.account import Account, AccountType
from backend.app.models.category import Category, TransactionType
from backend.app.models.transaction import Transaction
from backend.app.services.auth_service import AuthService
from backend.app.services.transaction_service import TransactionService

# Ensure this only runs explicitly
def seed():
    print("Starting database seeding...")
    db = SessionLocal()
    
    try:
        # Create Demo User
        auth_service = AuthService(db)
        demo_email = "demo@finora.ai"
        user = db.query(User).filter(User.email == demo_email).first()
        if not user:
            print("Creating demo user...")
            from backend.app.schemas.user import UserCreate
            user = auth_service.register_user(UserCreate(
                email=demo_email,
                password="password123",
                full_name="Finora Demo User"
            ))
        else:
            print("Demo user already exists.")

        # Create Default Categories (Global)
        categories_data = [
            ("Salary", TransactionType.INCOME, "💸"),
            ("Freelance", TransactionType.INCOME, "💻"),
            ("Investment", TransactionType.INCOME, "📈"),
            ("Food & Dining", TransactionType.EXPENSE, "🍔"),
            ("Transportation", TransactionType.EXPENSE, "🚗"),
            ("Shopping", TransactionType.EXPENSE, "🛍️"),
            ("Entertainment", TransactionType.EXPENSE, "🍿"),
            ("Bills & Utilities", TransactionType.EXPENSE, "💡"),
            ("Healthcare", TransactionType.EXPENSE, "🏥"),
            ("Travel", TransactionType.EXPENSE, "✈️"),
            ("Rent", TransactionType.EXPENSE, "🏠"),
            ("Subscriptions", TransactionType.EXPENSE, "🔄"),
            ("Other", TransactionType.EXPENSE, "📦")
        ]
        
        category_map = {}
        for name, ctype, icon in categories_data:
            cat = db.query(Category).filter(Category.name == name).first()
            if not cat:
                cat = Category(name=name, type=ctype, icon=icon)
                db.add(cat)
                db.commit()
                db.refresh(cat)
            category_map[name] = cat
            
        print(f"Ensured {len(categories_data)} default categories exist.")

        # Create Demo Accounts
        print("Creating demo accounts...")
        accounts_data = [
            ("Chase Checking", AccountType.BANK, "USD"),
            ("Amex Platinum", AccountType.CREDIT_CARD, "USD"),
            ("Fidelity Brokerage", AccountType.INVESTMENT, "USD")
        ]
        
        account_map = {}
        for name, atype, curr in accounts_data:
            acc = db.query(Account).filter(Account.name == name, Account.user_id == user.id).first()
            if not acc:
                acc = Account(user_id=user.id, name=name, account_type=atype, currency=curr, current_balance=Decimal("0.00"))
                db.add(acc)
                db.commit()
                db.refresh(acc)
            account_map[name] = acc
            
        # Create 6 months of transactions
        print("Creating 6 months of realistic transactions...")
        tx_service = TransactionService(db)
        
        # Check if transactions already exist for this user
        existing_tx_count = db.query(Transaction).filter(Transaction.user_id == user.id).count()
        if existing_tx_count > 0:
            print(f"Found {existing_tx_count} existing transactions. Skipping transaction seed to avoid duplicates.")
            return

        from backend.app.schemas.transaction import TransactionCreate
        
        end_date = date.today()
        start_date = end_date - timedelta(days=180)
        
        current_date = start_date
        
        while current_date <= end_date:
            # Salary (1st and 15th)
            if current_date.day in (1, 15):
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Chase Checking"].id,
                    category_id=category_map["Salary"].id,
                    type=TransactionType.INCOME,
                    amount=Decimal("3500.00"),
                    description="Acme Corp Salary",
                    merchant="Acme Corp",
                    transaction_date=current_date
                ))
            
            # Rent (1st)
            if current_date.day == 1:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Chase Checking"].id,
                    category_id=category_map["Rent"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("2200.00"),
                    description="Monthly Rent",
                    merchant="Irvine Company",
                    transaction_date=current_date
                ))
                
            # Subscriptions
            if current_date.day == 5:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Amex Platinum"].id,
                    category_id=category_map["Subscriptions"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("15.99"),
                    description="Netflix Premium",
                    merchant="Netflix",
                    transaction_date=current_date
                ))
            if current_date.day == 12:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Amex Platinum"].id,
                    category_id=category_map["Subscriptions"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("10.99"),
                    description="Spotify Premium",
                    merchant="Spotify",
                    transaction_date=current_date
                ))
                
            # Groceries & Food (Randomly throughout week)
            if random.random() < 0.4:
                merchants = ["Whole Foods", "Trader Joe's", "Sweetgreen", "Starbucks", "Uber Eats"]
                merchant = random.choice(merchants)
                amt = Decimal(str(round(random.uniform(5.0, 150.0), 2)))
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Amex Platinum"].id if amt > 20 else account_map["Chase Checking"].id,
                    category_id=category_map["Food & Dining"].id,
                    type=TransactionType.EXPENSE,
                    amount=amt,
                    description=f"{merchant} Purchase",
                    merchant=merchant,
                    transaction_date=current_date
                ))
                
            # Transportation
            if random.random() < 0.2:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Amex Platinum"].id,
                    category_id=category_map["Transportation"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal(str(round(random.uniform(15.0, 60.0), 2))),
                    description="Uber Ride",
                    merchant="Uber",
                    transaction_date=current_date
                ))

            # Introduce an Anomaly (Once every ~45 days)
            if random.random() < 0.02:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Amex Platinum"].id,
                    category_id=category_map["Shopping"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal(str(round(random.uniform(800.0, 2500.0), 2))),
                    description="Apple Store",
                    merchant="Apple",
                    transaction_date=current_date,
                    notes="Unusually high transaction anomaly"
                ))
                
            current_date += timedelta(days=1)
            
        print("Demo data seeded successfully!")
        
        for name, acc in account_map.items():
            db.refresh(acc)
            print(f"Account: {acc.name} - Final Balance: {acc.current_balance}")
            
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
