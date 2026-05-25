import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from ..core.config import config
from ..core.logger import get_logger
from ..core.database import User, SessionLocal

logger = get_logger(__name__)


class AuthenticationService:
    """JWT-based authentication service"""

    def __init__(self):
        self.secret = config.get("security.jwt_secret")
        self.algorithm = config.get("security.jwt_algorithm")
        self.expiration_hours = config.get("security.jwt_expiration_hours")

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    def create_token(self, user_id: int, username: str, role: str) -> str:
        """Create a JWT token"""
        payload = {
            "user_id": user_id,
            "username": username,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=self.expiration_hours),
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user and return token"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()

            if not user:
                logger.warning(f"User not found: {username}")
                return None

            if not user.is_active:
                logger.warning(f"User is inactive: {username}")
                return None

            # Check if account is locked
            if user.locked_until and user.locked_until > datetime.utcnow():
                logger.warning(f"User account is locked: {username}")
                return None

            # Verify password
            if not self.verify_password(password, user.password_hash):
                # Increment failed login attempts
                user.failed_login_attempts += 1

                max_attempts = config.get("security.max_login_attempts")
                if user.failed_login_attempts >= max_attempts:
                    lockout_minutes = config.get("security.lockout_duration_minutes")
                    user.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
                    logger.warning(f"User account locked due to failed attempts: {username}")

                db.commit()
                return None

            # Reset failed attempts on successful login
            user.failed_login_attempts = 0
            user.locked_until = None
            db.commit()

            # Create token
            token = self.create_token(user.id, user.username, user.role)

            return {
                "token": token,
                "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role},
            }
        finally:
            db.close()

    def create_user(self, username: str, email: str, password: str, role: str = "agent") -> Optional[Dict[str, Any]]:
        """Create a new user"""
        db = SessionLocal()
        try:
            # Check if user exists
            existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()

            if existing_user:
                logger.warning(f"User already exists: {username} or {email}")
                return None

            # Validate password strength
            if len(password) < config.get("security.password_min_length"):
                logger.warning("Password does not meet minimum length requirement")
                return None

            # Create user
            user = User(username=username, email=email, password_hash=self.hash_password(password), role=role)

            db.add(user)
            db.commit()
            db.refresh(user)

            logger.info(f"User created: {username}")

            return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create user: {e}")
            return None
        finally:
            db.close()


# Global authentication service instance
auth_service = AuthenticationService()
