import jwt

def verify_jwt_token(func):   #데코레이터 명명
    def decorated(request, *args, **kwargs):

        print("decorator-verify-token")

    return decorated