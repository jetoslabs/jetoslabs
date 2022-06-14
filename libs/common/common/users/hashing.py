from passlib.context import CryptContext

import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        authentic = pwd_context.verify(plain_password, hashed_password)
        return authentic
    except Exception as e:
        logger.get_logger().debug("Password is not a match")
        return False



def get_password_hash(password):
    return pwd_context.hash(password)
