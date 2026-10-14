"""Create or promote an administrator without exposing an unsafe public endpoint."""

import argparse
import getpass
import sys
from pathlib import Path

# `python scripts/create_admin.py` makes scripts/ the first import directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User
from app.repositories.user_repo import UserRepository


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or promote a CineVault administrator.")
    parser.add_argument("--name", required=True, help="Administrator display name")
    parser.add_argument("--email", required=True, help="Administrator email address")
    args = parser.parse_args()

    password = getpass.getpass("Password: ")
    if len(password) < 8:
        raise SystemExit("Password must contain at least 8 characters.")

    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.get_by_email(args.email)
        if user is None:
            user = User(
                name=args.name,
                email=args.email,
                password_hash=hash_password(password),
                is_admin=True,
            )
            db.add(user)
            action = "Created"
        else:
            user.name = args.name
            user.password_hash = hash_password(password)
            user.is_admin = True
            user.is_active = True
            action = "Promoted"
        db.commit()
        print(f"{action} administrator: {user.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
