import json

from django.db import transaction
from .Services.AuthService import *

from ninja import Field, Schema, Router


router = Router()


'''
## API 반환 정보 설정
## API의 응답값을 수정하려면 이곳에서 수정하시면 됩니다.
'''

## Code 200
class Success(Schema) :
    message : dict

## Code 201
class Created(Schema) :
    message : dict

## Code 400
class Message(Schema) :
    message : dict

# ## Code 500
# class ServerMessage(Schema) :
#     res_data : str



'''
## API 입력값 수정
'''

class RegiUserData(Schema) :
    userid : str 
    userpw : str
    userpw2 : str

class SignInUserData(Schema) :
    userid : str
    userpw : str

class SignOutUserData(Schema) :
    userid : str


## ====> 회원가입 API 
@router.post('/regi-user', auth=None, response={201:Created, 400:Message, 500:Message})
@transaction.atomic
def regi_user(request, data : RegiUserData) :

    # user_data = data.dict()
    
    res_code, message = AuthService.insert_user_data(data.dict())

    res_message = {
        "message" : message
    }

    return res_code, {'message' : res_message}

## ====> 로그인 API
@router.post('/sign-in', auth=None, response = {200: Success, 400: Message})
@transaction.atomic
def sign_in(request, data : SignInUserData) :

    user_data = data.dict()

    res_code, message = AuthService.sign_in_user(user_data['userid'], user_data['userpw'])
    jwt_token = AuthService.get_jwt_token(user_data['userid'])

    res_message = {
        "message": message,
        "refreshToken": jwt_token['refresh'],
        "accessToken": jwt_token['access']
    }

    return res_code, {'message' : res_message}


## 로그아웃
@router.post('/sign-out', response={200: Success, 500: Message})
@transaction.atomic
def sign_out(request, data : SignOutUserData) :

    user_data = data.dict()

    res_code, message = AuthService.sign_out_user(user_data['userid'])

    res_message = {
        "message": message
    }

    return res_code, {'message' : res_message}


## 신규 Access Token 발급
@router.post('/get-new-token', auth=None, response={200 : Success, 400 : Message, 500 : Message})
def get_access_token(request) :

    user_data = json.loads(request.body)

    res_code, message, token_data = AuthService.get_new_acces_token(user_data['user_id'], user_data['refreshToken'])


    res_message = {
        "message": message,
        "accessToken": token_data['access'],
        "refreshToken": token_data['refresh']
    }

    return res_code, {'message' : res_message}




