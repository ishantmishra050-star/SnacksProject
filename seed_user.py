from backend.database import SessionLocal
from backend.models.user import User, UserRole
from backend.utils.security import hash_password

db = SessionLocal()
try:
    email = "ishantmishra050@gmail.com"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        new_user = User(
            email=email,
            name="Ishant Mishra",
            password_hash=hash_password("password123"), # Default test password
            phone="9876543210",
            country="India",
            role=UserRole.customer
        )
        db.add(new_user)
        db.commit()
        print(f"User {email} created successfully with password: password123")
    else:
        print(f"User {email} already exists.")
finally:
    db.close()
