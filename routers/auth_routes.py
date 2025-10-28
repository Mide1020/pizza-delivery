from fastapi import APIRouter, Depends, status
from database import Session, engine
from schema import SignupModel, LoginModel
from models import User
from fastapi import Body

from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth2 import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix= "/auth",
    tags=['auth']
)


session = Session(bind=engine)

@auth_router.get("/")
def auth(Authorize: AuthJWT = Depends()):
  """
        ## Sample hello Auth route
    
    """
  try: 
      Authorize.jwt_required()

  except Exception as e:
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
        detail= "Invalid Token"
    )

  return {"mesaage": "Hello authentication"}


#signup route
@auth_router.post("/signup",
 status_code=status.HTTP_201_CREATED
)
async def signup(user: SignupModel = Body(...)):
    """
        ## Create a user
        This requires the following
        ```
                username:str
                email:str
                password:str
                is_staff:bool
                is_active:bool

        ```
    
    """

    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
      raise HTTPException(status_code=400,
      detail="User with email already exists")

      #  return HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
        #  detail= "A User with the Email already exist")

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code = 400,
          detail= "A User with the username already exist"
        )
    new_user = User (
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
        )
    session.add(new_user)
    session.commit()

    return {"username": new_user.username, "email": new_user.email}


  #login router
@auth_router.post("/login")
def loging(user: LoginModel, Authorize: AuthJWT= Depends()):
   """     
        ## Login a user
        This requires
            ```
                username:str
                password:str
            ```
        and returns a token pair `access` and `refresh`
   """
   db_user = session.query(User).filter(User.username == user.username).first()
   if db_user and check_password_hash(db_user.password, user.password):
    access_token = Authorize.create_access_token(subject = db_user.username)
    refresh_token = Authorize.create_refresh_token(subject = db_user.username)

    response = {
     "access": access_token, 
      "refresh": refresh_token
    }  


    return jsonable_encoder(response)

   raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
      detail = "Invalid Username Or Password"
  )

#refreshing tokens

@auth_router.get("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
  """
    ## Create a fresh token
    This creates a fresh token. It requires an refresh token.
    """
  try:
    Authorize.jwt_refresh_token_required()

  except Exception as e:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
        detail = "Please provide an valid refresh token"
    )
  current_user =  Authorize.get_jwt_identity()
  access_token = Authorize.create_access_token(subject=current_user)
  return jsonable_encoder({"access": access_token})
  