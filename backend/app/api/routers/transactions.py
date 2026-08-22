from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from backend.app.api.deps import get_db
from backend.app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from backend.app.models.category import TransactionType
from backend.app.schemas.user import UserResponse
from backend.app.services.transaction_service import TransactionService
from backend.app.api.deps import get_current_user

router = APIRouter(tags=["transactions"])

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_in: TransactionCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.create_transaction(current_user.id, transaction_in)

@router.get("", response_model=List[TransactionResponse])
def get_transactions(
    account_id: Optional[UUID] = Query(None, description="Filter by account"),
    category_id: Optional[UUID] = Query(None, description="Filter by category"),
    type: Optional[TransactionType] = Query(None, description="Filter by transaction type"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search merchant or description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_transactions(
        user_id=current_user.id,
        account_id=account_id,
        category_id=category_id,
        type=type,
        start_date=start_date,
        end_date=end_date,
        search=search,
        skip=skip,
        limit=limit
    )

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_transaction(transaction_id, current_user.id)

@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: UUID,
    transaction_in: TransactionUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.update_transaction(transaction_id, current_user.id, transaction_in)

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    service.delete_transaction(transaction_id, current_user.id)

@router.post("/import", status_code=status.HTTP_200_OK)
async def import_transactions(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return await service.import_csv(current_user.id, file)
