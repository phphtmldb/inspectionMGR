import os
from pathlib import Path
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

BASE_DIR = Path(__file__).resolve().parent.parent

#SECRET_KEY = 'your-secret-key'
# 보안 키를 .env에서 불러오기
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

DEBUG = True
# 디버그 모드 환경 변수 적용
#DEBUG = os.getenv("DEBUG", "False") == "True"

# ALLOWED_HOSTS = []
# ALLOWED_HOSTS 환경 변수 적용
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_recaptcha',
    'punchMGR',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inspectionMGR.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inspectionMGR.wsgi.application'

# Database 설정 부분

# 접두사 설정
DB_TABLE_PREFIX = "inspmgr_"

# 필수 환경 변수 확인 (설정되지 않았을 경우 오류 발생)
REQUIRED_ENV_VARS = ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        raise ValueError(f"⚠ 환경 변수 {var}가 설정되지 않았습니다. .env 파일을 확인하세요.")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # MySQL 엔진 설정
        'NAME': os.getenv('DB_NAME'),  # 데이터베이스 이름
        'USER': os.getenv('DB_USER'),  # DB 사용자명
        'PASSWORD': os.getenv('DB_PASSWORD'),  # DB 비밀번호 (10자리 유지)
        'HOST': os.getenv('DB_HOST'),  # 외부 DB 서버 주소
        'PORT': os.getenv('DB_PORT', '3306'),  # MySQL 기본 포트
        'OPTIONS': {
            'charset': 'utf8mb4',  # UTF-8 인코딩 설정
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'ssl': {'ssl-ca': os.getenv("DB_SSL_CERT", "")} if os.getenv("DB_USE_SSL") == "true" else {},  # SSL 설정
        },
        'CONN_MAX_AGE': 600,  # 연결 최대 유지 시간 (10분)
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'punchMGR.CustomUser'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# reCAPTCHA 설정
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")
