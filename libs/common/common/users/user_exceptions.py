from fastapi import HTTPException
from starlette import status

# TODO: remove dependency of FASTAPI HTTPException in this package - User
credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
