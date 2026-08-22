from typing import List, Dict, Tuple
from uuid import UUID
import math
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from backend.app.models.transaction import Transaction
from backend.app.models.category import TransactionType, Category
from backend.app.schemas.analytics import AnomalyResponse
from backend.app.schemas.transaction import TransactionResponse

class AnomalyDetectionService:
    def __init__(self, session: Session):
        self.session = session

    def detect_anomalies(self, user_id: UUID, days_lookback: int = 30) -> List[AnomalyResponse]:
        # We define anomalies by looking at the user's historical spending per category.
        # If a recent transaction in a category is significantly higher than the mean (e.g. > 2.0 std dev), it's an anomaly.
        
        # 1. Fetch all expense transactions with a category
        transactions = self.session.query(Transaction, Category.name.label("category_name")).join(
            Category, Transaction.category_id == Category.id
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.category_id.isnot(None)
        ).all()
        
        category_stats: Dict[str, List[float]] = {}
        for tx, cat_name in transactions:
            category_stats.setdefault(cat_name, []).append(float(tx.amount))
            
        # 2. Calculate mean and std dev per category
        stats = {}
        for cat_name, amounts in category_stats.items():
            if len(amounts) < 3:
                continue # Need at least 3 transactions to establish a baseline
                
            mean = sum(amounts) / len(amounts)
            variance = sum((x - mean) ** 2 for x in amounts) / len(amounts)
            std_dev = math.sqrt(variance)
            stats[cat_name] = (mean, std_dev)
            
        # 3. Find recent transactions (e.g., last 30 days) and check for anomalies
        cutoff_date = date.today() - timedelta(days=days_lookback)
        anomalies = []
        
        for tx, cat_name in transactions:
            if tx.transaction_date < cutoff_date:
                continue
                
            if cat_name not in stats:
                continue
                
            mean, std_dev = stats[cat_name]
            amt = float(tx.amount)
            
            # If std_dev is 0, they always spend exactly the same amount. An anomaly would be anything different, but let's be careful.
            if std_dev == 0:
                std_dev = mean * 0.1 # Assume at least 10% variance for safety
                if std_dev == 0:
                    continue # Free stuff?
                    
            z_score = (amt - mean) / std_dev
            
            if z_score > 2.0:
                expected_max = mean + (2 * std_dev)
                reason = f"This transaction is significantly higher than your typical spending in the '{cat_name}' category. You normally spend around {mean:.2f}."
                
                # Create a schema response
                tx_resp = TransactionResponse.model_validate(tx)
                
                anomalies.append(AnomalyResponse(
                    transaction=tx_resp,
                    expected_range_min=Decimal("0.00"),
                    expected_range_max=Decimal(str(round(expected_max, 2))),
                    anomaly_score=Decimal(str(round(z_score, 2))),
                    reason=reason
                ))
                
        # Sort by anomaly score descending
        anomalies.sort(key=lambda x: x.anomaly_score, reverse=True)
        return anomalies
