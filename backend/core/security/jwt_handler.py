from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from core.config.settings import settings


def create_access_token(data: dict):
    """
    Create JWT Access Token
    """

    payload = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_token(token: str):
    """
    Verify JWT Token
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )

        return payload

    except JWTError:
        return None