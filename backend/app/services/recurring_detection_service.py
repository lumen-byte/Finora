from typing import List, Dict, Any
from uuid import UUID
import math
from datetime import date, timedelta
from sqlalchemy.orm import Session
from backend.app.models.transaction import Transaction
from backend.app.models.category import TransactionType
from backend.app.schemas.analytics import RecurringTransactionResponse
from decimal import Decimal

class RecurringDetectionService:
    def __init__(self, session: Session):
        self.session = session

    def detect_recurring(self, user_id: UUID) -> List[RecurringTransactionResponse]:
        # Fetch all expenses grouped by merchant in Python for determinism
        transactions = self.session.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.merchant.isnot(None)
        ).order_by(Transaction.merchant, Transaction.transaction_date).all()
        
        merchant_groups: Dict[str, List[Transaction]] = {}
        for tx in transactions:
            merchant_groups.setdefault(tx.merchant, []).append(tx)
            
        results = []
        
        for merchant, txs in merchant_groups.items():
            if len(txs) < 3:
                continue
                
            # Calculate standard deviation of intervals
            intervals = []
            for i in range(1, len(txs)):
                delta = (txs[i].transaction_date - txs[i-1].transaction_date).days
                intervals.append(delta)
                
            mean_interval = sum(intervals) / len(intervals)
            variance_interval = sum((x - mean_interval) ** 2 for x in intervals) / len(intervals)
            std_dev_interval = math.sqrt(variance_interval)
            
            # Determine frequency
            frequency = "UNKNOWN"
            if 25 <= mean_interval <= 35 and std_dev_interval <= 5:
                frequency = "MONTHLY"
            elif 6 <= mean_interval <= 8 and std_dev_interval <= 2:
                frequency = "WEEKLY"
            elif 360 <= mean_interval <= 370 and std_dev_interval <= 10:
                frequency = "YEARLY"
            else:
                # Too irregular
                continue
                
            # Check amount variation
            amounts = [float(tx.amount) for tx in txs]
            mean_amount = sum(amounts) / len(amounts)
            variance_amount = sum((x - mean_amount) ** 2 for x in amounts) / len(amounts)
            std_dev_amount = math.sqrt(variance_amount)
            
            # If standard deviation of amount is huge relative to mean (e.g. > 20%), it's not a standard recurring subscription
            if mean_amount == 0 or (std_dev_amount / mean_amount) > 0.2:
                # However, things like utility bills fluctuate. So we allow some variance, but not extreme randomness.
                if (std_dev_amount / mean_amount) > 0.4:
                    continue # Too much variance, likely regular shopping (like 'Uber' or 'Whole Foods') not a recurring bill
                    
            # Compute confidence score based on consistency
            # Max score 1.0. Penalize for high std dev in interval or amount
            interval_penalty = min(0.3, std_dev_interval / mean_interval)
            amount_penalty = min(0.3, std_dev_amount / mean_amount)
            confidence = max(0.4, 1.0 - interval_penalty - amount_penalty)
            
            # Estimate next date
            last_date = txs[-1].transaction_date
            next_date = last_date + timedelta(days=int(mean_interval))
            
            results.append(RecurringTransactionResponse(
                merchant=merchant,
                average_amount=Decimal(str(round(mean_amount, 2))),
                frequency=frequency,
                estimated_next_date=next_date,
                transaction_count=len(txs),
                confidence_score=Decimal(str(round(confidence, 2)))
            ))
            
        results.sort(key=lambda x: x.confidence_score, reverse=True)
        return results
