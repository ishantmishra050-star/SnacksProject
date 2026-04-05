from backend.database import SessionLocal
from backend.models.user import User

db = SessionLocal()
try:
    users = db.query(User).all()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"ID: {u.id}, Email: {u.email}, Name: {u.name}, Phone: {u.phone}")
finally:
    db.close()
