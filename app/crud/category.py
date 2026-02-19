from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(
        name=category.name,
        description=category.description,
        is_active=category.is_active,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
