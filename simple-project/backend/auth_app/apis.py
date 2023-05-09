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
    meta: dict

## Code 201
class Created(Schema) :
    meta: dict

## Code 400
class Error(Schema) :
    meta: dict

## Code 500
class ServerError(Schema) :
    meta: dict

'''
## API 입력값 수정
'''

class RegiUserData(Schema) :
    # userid : str = Field(alias="계정 ID로 사용할 전화번호를 입력하세요. (-을 포함해주세요.)")
    # userpw : str = Field(alias="암호를 입력해주세요.")
    # userpw2 : str = Field(alias="동일한 암호를 한번 더 입력해주세요.")
    userid : str 
    userpw : str
    userpw2 : str

class SignInUserData(Schema) :
    userid : str
    userpw : str

class SignOutUserData(Schema) :
    userid : str


## ====> 회원가입 API 
@router.post('/regi-user', auth=None, response={201:Created, 400:Error, 500:ServerError})
@transaction.atomic
def regi_user(request, data : RegiUserData) :

    user_data = data.dict()
    
    res_code, message = AuthService.insert_user_data(user_data)

    meta = {
        "code": res_code,
        "message": message
    }

    return res_code, {'meta': meta}


## ====> 로그인 API
@router.post('/sign-in', auth=None, response = {200: Success, 400: Error})
@transaction.atomic
def sign_in(request, data : SignInUserData) :

    user_data = data.dict()

    res_code, message = AuthService.sign_in_user(user_data['userid'], user_data['userpw'])
    jwt_token = AuthService.get_jwt_token(user_data['userid'])

    meta = {
        "code": res_code,
        "message": message,
        "refreshToken": jwt_token['refresh'],
        "accessToken": jwt_token['access']
    }

    return res_code, {'meta': meta}  


## 로그아웃
@router.post('/sign-out', response={200: Success, 500: ServerError})
@transaction.atomic
def sign_out(request, data : SignOutUserData) :

    user_data = data.dict()

    res_code, message = AuthService.sign_out_user(user_data['userid'])

    meta = {
        "code": res_code,
        "message": message
    }

    return res_code, {'meta': meta}


## 신규 Access Token 발급
@router.post('/get-new-token', auth=None, response={200:Success, 400:Error, 500: ServerError})

def get_access_token(request) :

    user_data = json.loads(request.body)

    res_code, message, token_data = AuthService.get_new_acces_token(user_data['user_id'], user_data['refreshToken'])


    meta = {
        "code": res_code,
        "message": message,
        "accessToken": token_data['access'],
        "refreshToken": token_data['refresh']
    }

    return res_code, {'meta': meta}




