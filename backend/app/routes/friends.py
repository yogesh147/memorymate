from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Friend, Memory
from ..schemas import FriendCreate

router = APIRouter(
    prefix="/api/friends",
    tags=["friends"],
)


@router.post("")
def create_friend(
        friend: FriendCreate,
        db: Session = Depends(get_db),
):
    existing = (
        db.query(Friend)
        .filter(Friend.name == friend.name)
        .first()
    )

    if existing:
        return existing

    item = Friend(name=friend.name)

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get("")
def get_friends(
        db: Session = Depends(get_db),
):
    return (
        db.query(Friend)
        .order_by(Friend.name)
        .all()
    )


@router.get("/{name}")
def get_friend(
        name: str,
        db: Session = Depends(get_db),
):
    friend = (
        db.query(Friend)
        .filter(Friend.name.ilike(name))
        .first()
    )

    if not friend:
        raise HTTPException(
            status_code=404,
            detail="Friend not found",
        )

    memories = (
        db.query(Memory)
        .filter(Memory.person.ilike(name))
        .order_by(Memory.created_at.desc())
        .limit(20)
        .all()
    )

    return {
        "friend": friend,
        "memories": memories,
    }
