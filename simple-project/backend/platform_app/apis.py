from ninja import Router, Schema
# from .Services.PlatService import *
from .Services.PlatService import *
from django.db import transaction
from django.core import serializers
from datetime import date
import json

router = Router()



'''
## API 응답 스키마
## API의 응답값을 수정하려면 이곳에서 수정하시면 됩니다.
'''


## Code 200
class Success(Schema) :
    message: dict

## Code 201
class Created(Schema) :
    message: dict

## Code 400
class Error(Schema) :
    message: dict

## Code 500
class ServerError(Schema) :
    message: dict

'''
## API 입력 스키마 수정
## Swagger에서 입력값 예시에 해당하는 값을 여기서 등록합니다.
'''


class RegiItem(Schema) :

    userid : str
    category : str
    price : int
    cost : int
    p_name : str
    describe : str
    barcode : str
    expire_date : date
    size : str

class FixItem(Schema) :
    userid : str
    category : str = None
    price : int = None
    cost : int = None
    p_name : str
    describe : str = None
    barcode : str
    expire_date : date = None
    size : str = None

class DeleteItem(Schema) :
    userid : str
    p_name : str
    barcode : str

class GetItemList(Schema) :
    userid : str
    cursor : int = None

'''
## 상품 등록 API 
'''
# @router.post('/regi-item', auth=None, response={200: Success, 400: Error})
# auth=None이 추가되는 경우 urls.py의 GlobalAuth()를 거치지 않는다. 
@router.post('/regi-item', auth=None, response={200:Success, 201:Created, 400:Error, 500:ServerError})
@transaction.atomic
def regi_item(request, data : RegiItem) :


    '''
    -> 입력 데이터 명세 
    ### user_id = product_data['user_id'] | str
    ### category = product_data['p_category'] | str
    # price = product_data['p_price'] | integer
    # cost = product_data['p_cost'] | integer
    # p_name = product_data['p_name'] | str
    # describe = product_data['p_describe'] | str
    # barcode = product_data['p_barcode'] | str
    # expire_date = product_data['p_expire_date'] | date
    # size = product_data['p_size'] | str # S or L 사이즈 두종류 뿐임
    '''

    ## 데이터베이스에 관련된 로직을 다루는 컨트롤러(/Services/*Services.py) 영역에 접근함
    res_code, res_massage = PlatService.insert_item_data(data.dict())

    ## 컨트롤러 영역에서 반환된 정보를 토대로 응답을 설정함
    message = {
        "message": res_massage
    }

    return  res_code, {'message': message}
        


'''
## 상품 정보 수정 API
'''
@router.patch('/fix-item', auth = None, response={200: Success, 400: Error})
@transaction.atomic
def fix_info_item(request, data : FixItem) :

    '''
    -> json_data 명세
    category = json_data.get('p_category')
    price = json_data.get('p_price')
    cost = json_data.get('p_cost')
    describe = json_data.get('p_describe')
    barcode = json_data.get('p_barcode')
    expire_date = json_data.get('p_expire_date')
    size = json_data.get('p_size') # S or L 사이즈 두종류
    '''

    ## 입력 받는 인자들에 대한 유연성을 얻기 위해 해당 인자가 없는 경우 None값으로 대체되도록 처리함 (필수 입력은 제외)
    res_code, res_message = PlatService.fix_item_data(data.dict())
    # res_code, res_message = PlatService.fix_item_data(user_id, p_name, category, price, cost, describe, barcode, expire_date, size)


    message = {
        "message": res_message
    }

    return  res_code, {'message': message}


'''
## 상품 삭제 API
'''
@router.patch('/remove-item', response={200: Success, 400: Error})
@transaction.atomic
def delete_info_item(request) :

    product_data = json.loads(request.body)
    
    '''
    -> 요구 데이터 구조
    # user_id = product_data['user_id'] ## 필수 입력 필요
    # p_name = product_data['p_name'] ## 필수 입력 필요
    # barcode = product_data['p_barcode'] ## 필수 입력 필요
    '''
    res_code, res_message = PlatService.remove_item_data(product_data)

    message = {
        "code": res_code,
        "message": res_message
    }

    return 200, {"message":message}


'''
## 본인이 등록한 상품의 등록 리스트 및 상세 정보 호출 API
'''

@router.get('/list-item', auth=None, response={200: Success, 400: Error})
def list_time(request, userid:str, cursor:int=None) :

    print(userid)

    ## Cursor 기반 페이지네이션을  구현하는데, 1페이지 기준 10개의 상품 구현 
    ## auto increment로 설정된 primary키를 활용해서 cursor based pagination을 구현함

    # print(userid)
    # print(cursor)

    res_code, res_message, item_data = PlatService.get_item_list(userid, cursor)
    
    message = {

        "result":{
            "message":res_message
        },
        "data":{
            "products": item_data
        }
    }

    return res_code, {"message":message} 


'''
## 상품 검색 API
'''
@router.get('/search-item', response={200: Success, 400: Error})
def list_item(request, user_id:str, product_name:str) :

    ## 상품 이름 검색 - like 검색 및 초성 검색 지원 필요    
    res_code, res_message, item_data = PlatService.search_item_data(user_id, product_name)
    ## Controllers 영역에서 반환된 데이터를 처리
    message = {

        "result":{
            "message":res_message
        },
        "data":{
            "products": item_data
        }
    }

    return res_code, {"message":message}




