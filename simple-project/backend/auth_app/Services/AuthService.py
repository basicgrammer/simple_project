import bcrypt, jwt
from django.utils import timezone
from .cryptService import *
from ..models import *
from django.db import transaction
from django.conf import settings

from ninja_jwt.tokens import RefreshToken


class AuthService :
    @transaction.atomic
    def insert_user_data(user_data:dict) -> "Response Code":

        
        try : 
            # print(user_data)
    
            user_phone = user_data['userid']
            pw_check = user_data['userpw']
            pw_check_pair = user_data['userpw2']

            # print("--check")

            # print(user_phone)

            ## 휴대폰 번호 저장 필드에서는 - 를 제거하고 저장하는 것이 검색 등의 여러 방법을 고려할때 좋은 방법 생각함
            convert_phone_num = user_phone.replace("-", "")

            ## 보편적으로 회원가입 시 암호 입력 2번을 고려하여 비교 처리
            if pw_check == pw_check_pair :

                ## 중복 체크에서 한번 걸러내야하는 과정이 필요함.
                result = duplicate_check(user_phone)

                if result == False :

                    convert_pw = CryptService.pw_crypt(pw_check)

                    profile = Profile()

                    profile.user_id = user_phone
                    profile.user_pw = convert_pw
                    profile.phone_num = convert_phone_num
                    profile.save()

                    token = Token()

                    token.relation_id = profile
                    token.refresh_token = ''

                    token.save()

                    message = "회원가입이 성공적으로 진행되었습니다."
                    return 201, message

                else : 
                    ## 중복 체크에서 False가 되는 경우 중복되는 ID가 있다는 것
                
                    message = "중복된 계정이 존재합니다. "
                    return 400, message

            ## 암호가 일치하지 않는 경우
            else :

                message = "입력된 암호가 일치하지 않습니다."
                return 400, message

        except :

            message = "서비스에 오류가 발생했습니다."
            return 500, message



    
    def sign_in_user(user_id:str, user_pw:str) -> "Response Code, Message" :

        query_set = Profile.objects.filter(user_id = user_id) 

        if query_set.exists() :       

            pair_pw = query_set[0].user_pw
            pair_pw = pair_pw.encode('utf-8')

            check_result = bcrypt.checkpw(user_pw.encode('utf-8'), pair_pw)

            if check_result == True:

                query_set[0].last_login = get_now_time()
                query_set[0].save()


                ## 정상 처리되는 경우, 200
                message = "로그인 되었습니다 :)"
                return 200, message

            else :
                ## 정상 처리되지 않는 경우, 400
                message = "ID 또는 PW가 일치하지 않습니다."
                return 400, message
        else :

            ## 정상 처리되지 않는 경우, 400
            message = "해당하는 정보가 없습니다."
            return 400, message


    def sign_out_user(user_id:str)  -> "Response Code" :

        try :

            query_set = Profile.objects.get(user_id = user_id)

            ## 로그아웃 처리되므로 refresh 토큰 자체가 제거된다.
            query_set2 = Token.objects.get(relation_id = query_set.profile_pk_id)

            ## 리프레시 토큰 초기화 처리
            query_set2.refresh_token = ''

            query_set.save()
            query_set2.save()

            message = "성공적으로 로그아웃 되었습니다."
            return 200, message 

        except:

            message = "서비스 기능에 문제가 발생했습니다."
            return 500, message

    def get_jwt_token(user_id:str) -> "JWT Token Info" :

        # print(user_id)

        profile = Profile.objects.get(user_id = user_id)
        token = Token.objects.get(relation_id = profile.profile_pk_id)

        refresh_token = RefreshToken.for_user(profile)

        token.refresh_token = refresh_token
        token.save()

        access_token = refresh_token.access_token

        decode = jwt.decode(str(access_token), settings.SECRET_KEY, algorithms=["HS256"])

        decode['user_id'] = user_id
        decode['access'] = "authuser"

        encoded = jwt.encode(decode, settings.SECRET_KEY, algorithm="HS256")

        token_data = {
            'refresh': str(refresh_token),
            'access': str(encoded)
        }

        return token_data



    # def new_access_token(refresh_token:bytes) -> "JWT Access Token" :

    #     return accessToken
    def get_new_acces_token(user_id:str, refresh_token:bytes) -> "JWT Access Token" :
        
        try :

            # 분기 처리
            # 1. refresh Token 유효성 확인
            # 2. refresh Token DB 대조
            # 3. access Token 발급

            profile = Profile.objects.get(user_id = user_id)
            token = Token.objects.get(relation_id = profile.profile_pk_id)

            if token.refresh_token == refresh_token :

                refresh_token = RefreshToken.for_user(profile)

                token.refresh_token = refresh_token
                token.save()

                access_token = refresh_token.access_token

                decode = jwt.decode(str(access_token), settings.SECRET_KEY, algorithms=["HS256"])

                decode['user_id'] = user_id
                decode['access'] = "authuser"

                encoded = jwt.encode(decode, settings.SECRET_KEY, algorithm="HS256")

                token_data = {
                    'refresh': str(refresh_token),
                    'access': str(encoded)
                }

                message = "토큰이 성공적으로 발급되었습니다."
                res_code = 200

                return res_code, message, token_data

            else : 

                token_data = {
                    'refresh': None,
                    'access': None
                }
                res_code = 400
                message = "계정이 로그아웃 되었습니다. 다시 로그인해주세요."

                return res_code, message, token_data

        except  :
            
            token_data = {
                'refresh': None,
                'access': None
            }
            res_code = 400
            message = "계정이 로그아웃 되었습니다. 다시 로그인해주세요."

            return res_code, message, token_data





## 중복 체크 
def duplicate_check(user_id:str) -> bool :

    query_set = Profile.objects.filter(user_id = user_id)

    ## Count > 0 보다는 쿼리가 존재하는지 자체를 반환 받는게 더 좋다.
    ## 해당 쿼리 결과가 존재한다고 나타나는 경우, 동일한 휴대폰번호로 중복되는 ID가 존재, False 반환
    # 중복 존재 시 True, 존재하지 않는 경우 False 반환

    return query_set.exists()



## 현재 시간 가져오기
def get_now_time() -> "time" :

    now = timezone.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')

    return date