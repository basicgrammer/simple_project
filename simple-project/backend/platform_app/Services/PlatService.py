from ..models import *
from django.utils import timezone
from jamo import h2j, j2hcj
from auth_app.models import Profile


class PlatService :

    def insert_item_data(product_data:dict) -> "Response Code, Message" :

        p_query_set = Product.objects.filter(p_name = product_data['p_name'], p_barcode = product_data['barcode'], p_delete_check = False)

        try : 

            if p_query_set.exists() :

                message = "중복되는 상품이 존재합니다."            

                return 400, message

            else :
            
                now = timezone.now()
                date = now.strftime('%Y-%m-%d %H:%M:%S')

                name_jamo = create_keyword(product_data['p_name']) ## 같은 파일 내 create_keyword 함수 호출

                # Product 테이블 생성을 위해서 매핑 수행

                query_set = Product()
                query_set.p_regi_user = product_data['userid']
                query_set.fk_key = Profile.objects.get(user_id = product_data['userid'])
                query_set.p_category = product_data['category']
                query_set.p_price = product_data['price']
                query_set.p_cost = product_data['cost']
                query_set.p_name = product_data['p_name']
                query_set.p_subscription = product_data['describe']
                query_set.p_barcode = product_data['barcode']
                query_set.p_expire_date = product_data['expire_date'].strftime('%Y-%m-%d')
                query_set.p_size = product_data['size']
                query_set.p_keyword = name_jamo

                query_set.save()

                # query_set.p_regi_date = date # regi_date와 fix_date는 자동으로 생성되며, 수정 시 fix_date만 새로 수정하면 된다.
                # query_set.p_delete_check = False # 기본 Default값이 False로 되어있어서 따로 매핑하지 않았음, delete_check를 Boolean으로 두는 경우 데이터 복구 시 유리할 것으로 생각됨

                message = "상품이 성공적으로 등록되었습니다."

                return 201, message

        ## Parsing에 문제가 발생하는 경우
        except KeyError :

            message = "서비스에 오류가 발생했습니다."
            return 500, message


    def fix_item_data(json_data:dict) -> "Response Code, Message" :

        p_query_set = Product.objects.filter(p_regi_user = json_data['userid'], p_name = json_data['p_name'], p_delete_check = False) 

        ## .get()으로 데이터를 가져오는 경우 데이터가 없을 때 에러가 발생하기 때문에 filter로 데이터를 반환 받음
        ## query_set이 존재하는 경우에만 수정된 정보의 업데이트가 가능하므로 아래 로직 수행
        
        if p_query_set.exists() :

            update_query_set = p_query_set[0]

            if json_data.get('p_name') != None :
                update_query_set.p_name = json_data['p_name']

            if json_data.get('p_category') != None :
                update_query_set.p_category = json_data['category']
            
            if json_data.get('p_price') != None :
                update_query_set.p_price = json_data['price']

            if json_data.get('p_cost') != None :
                update_query_set.p_cost = json_data['cost']
            
            if json_data.get('p_describe') != None :
                update_query_set.p_subscription = json_data['describe']

            if json_data.get('p_barcode') != None :
                update_query_set.p_barcode = json_data['barcode']

            if json_data.get('p_expire_date') != None :
                update_query_set.p_expire_date = json_data['expire_date']
            
            if json_data.get('p_size') != None :
                update_query_set.p_size = json_data['size']

            now = timezone.now()
            date = now.strftime('%Y-%m-%d %H:%M:%S')
            update_query_set.p_fix_date = date


            update_query_set.save()

            messages = "상품 정보가 수정되었습니다."
            return 200, messages

        else :

            messages = "상품 정보가 존재하지 않습니다."
            return 400, messages



    
    def remove_item_data(product_data:dict) -> "Response Code" :
    # def remove_item_data(user_id:str, p_name:str, barcode:str) -> "Response Code" :


        try : 

            query_set = Product.objects.filter(p_regi_user = product_data['user_id'], p_name = product_data['p_name'], p_barcode = product_data['barcode'], p_delete_check = False)

            if query_set.exists() :

                p_query_set = query_set[0]
                p_query_set.p_delete_check = True
                p_query_set.save()

                message = "상품이 삭제되었습니다."
                return 200, message

            else :

                message = "상품 정보가 없거나, 상품 삭제에 실패했습니다. "
                return 400, message

        except KeyError :

            message = "서비스에 오류가 발생했습니다."
            return 500, message

    
    def get_item_list(userid : str, cursor : int) -> "Response Code, Message, Item Data List" :
        

        # print(parser_data)

        if cursor != None: 
        
            ## Cursor 값이 존재하므로, Cursor값부터 10개까지 슬라이스 처리를 통해 반환
            query_set = Product.objects.filter(p_pk_id__gte = cursor, p_regi_user = userid, p_delete_check = False).order_by('p_pk_id')[:10].values()

        else : 

            ## Cursor 즉 마지막 값이 None인 경우 처음부터 10개까지 슬라이스 처리를 통해 반환
            query_set = Product.objects.filter(p_regi_user = userid, p_delete_check = False).order_by('p_pk_id')[:10].values()
            test_query_set = Product.objects.select_related('fk_key').all()
            # test_query_set = Product.objects.all().values()

            for index in test_query_set :

                # print(item.p_pk_id)
                # print(item.values())
                # print(index)

                print("Excute Query")

                print(index.fk_key.user_pw)

        n_query_set = list(query_set) ## 프론트 반환 시 파싱에 문제가 없도록 list로 묶음 처리

        if query_set.exists() :
            
            messages = "상품 리스트 정보입니다."
            return 200, messages, n_query_set

        else :  

            temp_query_set = None
            messages = "등록된 상품 리스트 정보가 없습니다."
            return 400, messages, temp_query_set


    def search_item_data(user_id:str, product_name:str) -> "Response Code, Message, Item Data" :

        try : 
            ## 초성 변환 함수 ex) 슈크림 라떼 -> ㅅㅋㄹ ㄹㄸ
            keyword = create_keyword(product_name)
            
            ## 상품 원본 이름 검색 쿼리
            query_set = Product.objects.filter(p_regi_user = user_id, p_name__icontains = product_name, p_delete_check = False).values()

            ## 상품 초성 이름 검색 쿼리
            query_set2 = Product.objects.filter(p_regi_user = user_id, p_keyword__icontains = keyword, p_delete_check = False).values()

            ## query_set 즉 원본 이름 검색에서 없는 경우, 초성 검색 결과를 확인해서 반환하는 구조

            if query_set.exists() :
                n_query_set = list(query_set)    

            else :
                n_query_set = list(query_set2)


            message = "검색된 상품 리스트를 정보입니다."
            
            return 200, message, n_query_set

        except KeyError :

            n_query_set = None
            message = "상품 검색에 대한 문제가 발생했습니다."

            return 500, message, n_query_set



## 초성 변환 함수
def create_keyword(origin_keyword:str) -> "keyword" :

    Init = []

    origin_name = origin_keyword

    for index in origin_name :

        tmp = h2j(index)
        imf = j2hcj(tmp)
        Init.append(imf[0])

    result = "".join(Init)

    return result