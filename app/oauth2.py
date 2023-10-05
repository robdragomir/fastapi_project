# JWT token
"""
A token provided to a user after they successfully authenticate to an API. The token is then sent to the API
during each request, to be verified. If the token is valid, the request gets processed.
JWT tokens have 3 components:
    HEADER - metadata about the token (type of token, algorithm used, etc.); same for all tokens
    PAYLOAD - optional; can be anything; the JWT token is not encrypted so don't include any confidential info here!!!
    VERIFY SIGNATURE - created using the information in the header and payload combined with a SECRET KEY stored here;
    used to determine if the token is valid;
"""

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from .config import settings

# token url has to be the same as the route address for the login function
oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

# The key required to generate the signatures
# Any string will do, but you can run the following command to
# generate a string such as the one below: openssl rand -hex 32
SECRET_KEY = settings.secret_key
# Algorithm to be used for generating the signature from the secret
ALGORITHM = settings.algorithm
# token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """
    Generate JWT token for authenticated user.
    :param data:
        The user's payload.
    :return:
        The new JWT token
    """
    to_encode = data.copy()
    # set expiration time for the token to be generated
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # create the JWT token using the ALGORITHM to create the signature from the payload and the secret.
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
