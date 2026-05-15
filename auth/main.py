from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import model
import schemas
import utils
from auth_database import get_db
from datetime import datetime, timedelta
from jose import jwt
from utils import hash_password
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError



SECRET_KEY = "R52mpURsKyhoCUIVScvF3CFVlVD0bV54nPrKSEkEOEQ"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Helper function
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encode_jwt


app = FastAPI()


@app.post("/signup")
def user_registration(user: schemas.CreateUser, db: Session=Depends(get_db)):
    existing_user = db.query(model.User).filter(model.User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pass = hash_password(user.password)

    new_user = model.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pass,
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id":new_user.id, "username": new_user.username, "email": new_user.email, "role": new_user.role}


@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(model.User).filter(model.User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")

    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    token_data = {"sub":user.username, "role":user.role}
    token = create_access_token(token_data)
    return {"access_token":token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    return {
        "username": username,
        "role": role
    }


@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"Message": f"Hello {current_user['username']} | You accessed a protected route"}


def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission")

        return current_user

    return role_checker


@app.get("/profile")
def profile(current_user: dict = Depends(require_roles(["user","admin"]))):
    return {"message": f"Profile of {current_user['username']} ({current_user['role']})"}


@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(require_roles(["user"]))):
    return {"message": f"Welcome {current_user['username']} - {current_user['role']}"}


@app.get("/admin/dashbaord")
def admin_dashboard(current_user: dict = Depends(require_roles(["admin"]))):
    return {"message": f"Welcome {current_user['username']} - {current_user['role']}"}