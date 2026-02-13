import logging
from app.db.session import SessionLocal
from app.services.user import user
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: SessionLocal) -> None:
    user_in = UserCreate(
        email="admin@example.com",
        password="admin",
        is_superuser=True,
        is_active=True,
    )
    user_exists = user.get_by_email(db, email=user_in.email)
    if not user_exists:
        user.create(db, obj_in=user_in)
        logger.info("Superuser created")
    else:
        logger.info("Superuser already exists")

if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
