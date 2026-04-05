from backend.database import SessionLocal
from backend.models.user import User, UserRole
from backend.utils.security import hash_password

db = SessionLocal()
try:
    email = "uatadmin@demo"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        new_admin = User(
            email=email,
            name="UAT Admin",
            password_hash=hash_password("adminUAT123"), # Default test password
            phone="+919999999999",
            country="India",
            role=UserRole.admin
        )
        db.add(new_admin)
        db.commit()
        print(f"UAT Admin '{email}' created successfully with password: adminUAT123")
    else:
        print(f"UAT Admin '{email}' already exists.")
except Exception as e:
    print(f"Error seeding UAT Admin: {e}")
finally:
    db.close()
