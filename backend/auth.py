from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# this handles password hashing
pwd_context = CryptContext(schemes=["bcrypt"])

# secret key used to sign tokens - keep this private
SECRET_KEY = "codesentinel-secret-key-change-this"
ALGORITHM = "HS256"

def hash_password(password):
    # converts "mypassword" → "$2b$12$randomhash..."
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    # checks if the plain password matches the hash
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data):
    # make a copy of the data
    to_encode = data.copy()
    
    # token expires in 24 hours
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    
    # create and return the token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        # decode and return the data inside the token
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None