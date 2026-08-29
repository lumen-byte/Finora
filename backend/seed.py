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
            # Clear existing transactions for fresh Indian seed
            db.query(Transaction).filter(Transaction.user_id == user.id).delete()
            db.commit()
            print("Cleared existing transactions for fresh seed.")

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
            ("Savings & Investments", TransactionType.EXPENSE, "💰"),
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
            ("HDFC Salary Account", AccountType.BANK, "INR"),
            ("SBI Credit Card", AccountType.CREDIT_CARD, "INR"),
            ("Zerodha Demat", AccountType.INVESTMENT, "INR")
        ]
        
        account_map = {}
        for name, atype, curr in accounts_data:
            acc = db.query(Account).filter(Account.name == name, Account.user_id == user.id).first()
            if not acc:
                acc = Account(user_id=user.id, name=name, account_type=atype, currency=curr, current_balance=Decimal("0.00"))
                db.add(acc)
                db.commit()
                db.refresh(acc)
            else:
                acc.current_balance = Decimal("0.00")
                db.commit()
                db.refresh(acc)
            account_map[name] = acc
            
        # Create 12 months of realistic transactions
        print("Creating 12 months of realistic transactions...")
        tx_service = TransactionService(db)
        
        from backend.app.schemas.transaction import TransactionCreate
        
        end_date = date.today()
        start_date = end_date - timedelta(days=365)
        
        current_date = start_date
        
        while current_date <= end_date:
            # Salary (1st of every month)
            if current_date.day == 1:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["HDFC Salary Account"].id,
                    category_id=category_map["Salary"].id,
                    type=TransactionType.INCOME,
                    amount=Decimal("80000.00"),
                    description="Infosys Salary",
                    merchant="Infosys Ltd",
                    transaction_date=current_date
                ))
            
            # Rent (3rd of every month)
            if current_date.day == 3:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["HDFC Salary Account"].id,
                    category_id=category_map["Rent"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("18500.00"),
                    description="Monthly Rent Transfer",
                    merchant="Landlord",
                    transaction_date=current_date
                ))

            # SIP Investment (10th of every month)
            if current_date.day == 10:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["HDFC Salary Account"].id,
                    category_id=category_map["Savings & Investments"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("5000.00"),
                    description="Mutual Fund SIP",
                    merchant="Zerodha Coin",
                    transaction_date=current_date
                ))
                
            # Subscriptions & Bills
            if current_date.day == 5:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["SBI Credit Card"].id,
                    category_id=category_map["Subscriptions"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("199.00"),
                    description="Netflix Mobile",
                    merchant="Netflix India",
                    transaction_date=current_date
                ))
            if current_date.day == 12:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["SBI Credit Card"].id,
                    category_id=category_map["Bills & Utilities"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("749.00"),
                    description="Jio Postpaid",
                    merchant="Reliance Jio",
                    transaction_date=current_date
                ))
                
            # Groceries & Food (Randomly throughout week)
            if random.random() < 0.5:
                merchants = ["Zomato", "Swiggy", "Blinkit", "Zepto", "D-Mart", "Starbucks", "Local Kirana"]
                merchant = random.choice(merchants)
                amt = Decimal(str(round(random.uniform(150.0, 1200.0), 2)))
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["SBI Credit Card"].id if amt > 300 else account_map["HDFC Salary Account"].id,
                    category_id=category_map["Food & Dining"].id,
                    type=TransactionType.EXPENSE,
                    amount=amt,
                    description=f"{merchant} Order",
                    merchant=merchant,
                    transaction_date=current_date
                ))
                
            # Transportation
            if random.random() < 0.3:
                merchants = ["Ola Cabs", "Uber India", "Namma Metro", "IRCTC"]
                merchant = random.choice(merchants)
                amt = Decimal(str(round(random.uniform(40.0, 600.0), 2)))
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["HDFC Salary Account"].id,
                    category_id=category_map["Transportation"].id,
                    type=TransactionType.EXPENSE,
                    amount=amt,
                    description=f"{merchant} Ride",
                    merchant=merchant,
                    transaction_date=current_date
                ))

            # iPhone Anomaly (Exactly 1 month ago)
            last_month_date = end_date - timedelta(days=30)
            if current_date == last_month_date:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["SBI Credit Card"].id,
                    category_id=category_map["Shopping"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("79900.00"),
                    description="Apple iPhone 15",
                    merchant="Imagine Store",
                    transaction_date=current_date,
                    notes="Bought a new iPhone!"
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

