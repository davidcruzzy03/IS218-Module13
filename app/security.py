"""Security utilities for password hashing and verification."""

from passlib.context import CryptContext

# Configure bcrypt as the password hashing algorithm
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.

    Args:
        password: The user's plain-text password.

    Returns:
        A securely hashed password.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against its hash.

    Args:
        plain_password: Password entered by the user.
        hashed_password: Stored password hash.

    Returns:
        True if the password matches, otherwise False.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )