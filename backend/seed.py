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
    print("Starting B2B database seeding...")
    db = SessionLocal()
    
    try:
        # Create Demo User (Represents the Company Admin)
        auth_service = AuthService(db)
        demo_email = "demo@finora.ai"
        user = db.query(User).filter(User.email == demo_email).first()
        if not user:
            print("Creating demo company admin...")
            from backend.app.schemas.user import UserCreate
            user = auth_service.register_user(UserCreate(
                email=demo_email,
                password="password123",
                full_name="Finora Corp Admin"
            ))
        else:
            print("Demo admin already exists.")
            # Clear existing transactions and accounts for fresh B2B seed
            db.query(Transaction).filter(Transaction.user_id == user.id).delete()
            db.query(Account).filter(Account.user_id == user.id).delete()
            db.commit()
            print("Cleared existing personal data for fresh enterprise seed.")

        # Create Default Categories (Global)
        categories_data = [
            ("Client Revenue", TransactionType.INCOME, "💸"),
            ("Capital Injection", TransactionType.INCOME, "🏦"),
            ("Payroll", TransactionType.EXPENSE, "👥"),
            ("Software Subscriptions", TransactionType.EXPENSE, "💻"),
            ("Cloud Infrastructure", TransactionType.EXPENSE, "☁️"),
            ("Marketing Ads", TransactionType.EXPENSE, "📢"),
            ("Travel & Events", TransactionType.EXPENSE, "✈️"),
            ("Office Operations", TransactionType.EXPENSE, "🏢"),
            ("Legal & Compliance", TransactionType.EXPENSE, "⚖️"),
            ("Miscellaneous", TransactionType.EXPENSE, "📦")
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
            
        print(f"Ensured {len(categories_data)} B2B categories exist.")

        # Create Demo Departments (Accounts)
        print("Creating enterprise departments...")
        accounts_data = [
            ("Engineering", AccountType.BANK, "INR"),
            ("Human Resources", AccountType.BANK, "INR"),
            ("Marketing", AccountType.BANK, "INR"),
            ("Sales", AccountType.BANK, "INR"),
            ("Executive", AccountType.BANK, "INR")
        ]
        
        account_map = {}
        for name, atype, curr in accounts_data:
            acc = Account(user_id=user.id, name=name, account_type=atype, currency=curr, current_balance=Decimal("0.00"))
            db.add(acc)
            db.commit()
            db.refresh(acc)
            account_map[name] = acc
            
        # Create 12 months of realistic B2B transactions
        print("Creating 12 months of enterprise transactions...")
        tx_service = TransactionService(db)
        
        from backend.app.schemas.transaction import TransactionCreate
        
        end_date = date.today()
        start_date = end_date - timedelta(days=365)
        
        current_date = start_date
        
        while current_date <= end_date:
            # Monthly Client Revenue (Sales Dept)
            if current_date.day == 1:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Sales"].id,
                    category_id=category_map["Client Revenue"].id,
                    type=TransactionType.INCOME,
                    amount=Decimal(str(random.randint(180000, 250000))),
                    description="Monthly Enterprise Retainers",
                    merchant="Enterprise Clients",
                    transaction_date=current_date
                ))
            
            # Payroll (HR Dept) - 3rd of month
            if current_date.day == 3:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Human Resources"].id,
                    category_id=category_map["Payroll"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("85000.00"),
                    description="Monthly Employee Salaries",
                    merchant="RazorpayX Payroll",
                    transaction_date=current_date
                ))

            # Cloud Infrastructure (Engineering) - 10th of month
            if current_date.day == 10:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Engineering"].id,
                    category_id=category_map["Cloud Infrastructure"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("15000.00"),
                    description="AWS Hosting & DB RDS",
                    merchant="Amazon Web Services",
                    transaction_date=current_date
                ))
                
            # Marketing Subscriptions & Ads
            if current_date.day == 5:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Marketing"].id,
                    category_id=category_map["Marketing Ads"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("12000.00"),
                    description="Google Ads Campaign",
                    merchant="Google Ireland",
                    transaction_date=current_date
                ))
            if current_date.day == 12:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Marketing"].id,
                    category_id=category_map["Marketing Ads"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("8500.00"),
                    description="LinkedIn Sponsored Content",
                    merchant="LinkedIn Corp",
                    transaction_date=current_date
                ))
                
            # Engineering Software Subs
            if current_date.day == 15:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Engineering"].id,
                    category_id=category_map["Software Subscriptions"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("2500.00"),
                    description="GitHub Enterprise Licenses",
                    merchant="GitHub Inc",
                    transaction_date=current_date
                ))
                
            # Office & Admin (Randomly throughout week)
            if random.random() < 0.2:
                merchants = ["WeWork", "Amazon Business", "Zoom Video", "Slack", "Figma"]
                merchant = random.choice(merchants)
                amt = Decimal(str(round(random.uniform(500.0, 4500.0), 2)))
                dept = "Executive" if merchant in ["WeWork"] else "Engineering" if merchant in ["Figma"] else "Human Resources"
                
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map[dept].id,
                    category_id=category_map["Software Subscriptions" if merchant in ["Zoom Video", "Slack", "Figma"] else "Office Operations"].id,
                    type=TransactionType.EXPENSE,
                    amount=amt,
                    description=f"{merchant} Invoice",
                    merchant=merchant,
                    transaction_date=current_date
                ))

            # Team Travel & Offsites (Sales / Exec)
            if random.random() < 0.1:
                amt = Decimal(str(round(random.uniform(5000.0, 15000.0), 2)))
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Sales"].id,
                    category_id=category_map["Travel & Events"].id,
                    type=TransactionType.EXPENSE,
                    amount=amt,
                    description="Client Meeting Flights & Hotels",
                    merchant="MakeMyTrip Corporate",
                    transaction_date=current_date
                ))

            # Anomaly Example: Massive Legal Bill (Exactly 1 month ago)
            last_month_date = end_date - timedelta(days=30)
            if current_date == last_month_date:
                tx_service.create_transaction(user.id, TransactionCreate(
                    account_id=account_map["Executive"].id,
                    category_id=category_map["Legal & Compliance"].id,
                    type=TransactionType.EXPENSE,
                    amount=Decimal("150000.00"),
                    description="Annual Corporate Audit & Legal Filing",
                    merchant="Deloitte & Touche",
                    transaction_date=current_date,
                    notes="One-time audit fee."
                ))
                
            current_date += timedelta(days=1)
            
        print("Enterprise demo data seeded successfully!")
        
        for name, acc in account_map.items():
            db.refresh(acc)
            print(f"Department: {acc.name} - Budget Spend/Balance: {acc.current_balance}")
            
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
