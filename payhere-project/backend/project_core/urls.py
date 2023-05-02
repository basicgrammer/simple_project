from django.urls import path
from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.conf import settings
import jwt, json
from auth_app.apis import router as auth_router
from platform_app.apis import router as platfrom_router
from ninja.errors import HttpError

'''
## JWT 인증 관리 구역, Bearer을 통해 통과되는 경우에만 해당 API 응답을 받을 수 있다.
'''
class GlobalAUth(HttpBearer) :

    def authenticate(self, request, token) :

        ## 인코딩된 데이터로 Token 해석에 필요한 정보들을 가져오기 때문에, 문서와 다르게 직접 핸들링 처리
        try : 
            decode = jwt.decode(str(token), settings.SECRET_KEY, algorithms=["HS256"])
            access = decode['access']

            if access == "authuser" :
                return access

        ## Access Token을 재발급 받는 2가지 방식 중 하나를 선택해야함
        ## 1. 요청마다 Access Token과 Refresh Token을 같이 넘기는 방법
        ## 2. 재발급 API를 만들어서 서버에서 Access Token이 만료되었다고 응답 시 Refresh Token으로 요청하여 재발급 받는 방법
        ## 여기서는 2번 과정으로 만들어야한다고 판단됨

        except jwt.ExpiredSignatureError as e:

            messages = "JWT 토큰 만료, 신규 발급 필요"

            meta = {
                "code": 401,
                "message": messages,
                "api-url": "/api/auth/new-token"
            }

            raise HttpError(401, meta)


'''
## API 라우터 등록 및 URL 관리 영역
'''

api = NinjaAPI(auth=GlobalAUth())

api.add_router("auth/", auth_router)
api.add_router("plat/", platfrom_router)

urlpatterns = [
    path('api/', api.urls),
]
