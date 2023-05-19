from datetime import timedelta

# Seceret Key의 경우, django env or json으로 분리하는 것이 더 좋다고 생각됨
SECRET_KEY = "django-insecure-lm4qzcyq6f$7a&%p3ul_g(-x6i6$xhq2f@a_mr2f6tja!b8wr!"

## django db setting
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_db',
        'USER': 'test',
        'PASSWORD': 'test123',
        'HOST': 'database',
        'PORT': '3306',
    }
}

NINJA_JWT = {
    ## 임시로 엑세스 토큰 LIFETIME을 120분으로 조종함
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=60),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'USER_ID_FIELD': 'user_id',
    'USER_ID_CLAIM': 'user_id',

    'USER_AUTHENTICATION_RULE': 'ninja_jwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('ninja_jwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'ninja_jwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}