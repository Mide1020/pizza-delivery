# from pydantic import BaseModel
# from typing import Optional

# class SignupModel(BaseModel):
#     id: Optional[int] = None
#     username: str
#     email: str
#     password: str
#     is_staff: Optional[bool]
#     is_active:  Optional[bool]


#     model_config = {
#         "from_attributes": True,
#         "json_schema_extra": {
#             "example": {
#                 "username": "JohnDoe",
#                 "email": "johndoe@example.com",
#                 "password": "strongpassword",
#                 "is_staff":False,
#                 "is_active":True
#             }
#         }
#     }

# class settings(BaseModel):
#     authjwt_secret_key: str = 'b05b4b3e86fd5ba6760fb2cb0ec0a57da01ff1ab5bc3d4583ccf37130bb9cc61'
#     authjwt_token_location: set = {"headers"}


# class LoginModel(BaseModel):
#     username: str
#     password: str
   

# # class OrderModel(BaseModel):
# #     id: Optional[int]
# #     quantity: int
# #     order_status : Optional[str] ="PENDNG"
# #     pizza_size : Optional [str] = "SMALL"
# #     user_id : Optional [int]


# class OrderModel(BaseModel):
#     id: Optional[int] = None
#     quantity: int
#     order_status: Optional[str] = "PENDING"
#     pizza_size: Optional[str] = "SMALL"
#     user_id: Optional[int] = None


# class config:
#     orn_mode = True
#     schema_extra = {
#         "example": {
#             "quantity": 2,
#             "pizza_size": "LARGE"
#         }
#     }

# class OrderStatusModel(BaseModel):
#     order_status:Optional[str]="PENDING"

#     class Config:
#         orm_mode=True
#         schema_extra={
#             "example":{
#                 "order_status":"PENDING"
#             }
#         }

from pydantic import BaseModel
from typing import Optional


class SignupModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "username": "JohnDoe",
                "email": "johndoe@example.com",
                "password": "strongpassword",
                "is_staff": False,
                "is_active": True
            }
        }
    }


class settings(BaseModel):
    authjwt_secret_key: str = "b05b4b3e86fd5ba6760fb2cb0ec0a57da01ff1ab5bc3d4583ccf37130bb9cc61"
    authjwt_token_location: set = {"headers"}


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"
    user_id: Optional[int] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }
    }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "order_status": "PENDING"
            }
        }
    }
