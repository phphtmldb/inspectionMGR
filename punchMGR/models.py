from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.conf import settings

# 기본 테이블 Prefix 설정
DB_TABLE_PREFIX = getattr(settings, "DB_TABLE_PREFIX", "inspmgr_")


class BaseModel(models.Model):
    """
    모든 모델이 상속받을 기본 모델 (자동으로 테이블 이름에 Prefix 추가)
    """
    class Meta:
        abstract = True  # 이 모델은 직접 테이블을 생성하지 않음

    @classmethod
    def get_table_name(cls):
        """ 테이블명 앞에 설정된 Prefix를 자동으로 추가 """
        return f"{DB_TABLE_PREFIX}{cls.__name__.lower()}"
    

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        주어진 이메일과 비밀번호로 일반 사용자 생성
        """
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)  # 기본적으로 계정 비활성화 (이메일 인증 필요)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        주어진 이메일과 비밀번호로 관리자(superuser) 생성
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('관리자는 is_staff=True여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('관리자는 is_superuser=True여야 합니다.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):  # BaseModel을 상속받도록 변경
    email = models.EmailField(unique=True)
    email_token = models.CharField(max_length=32, blank=True, null=True, unique=True)  # 중복 방지를 위해 unique=True 추가
    is_active = models.BooleanField(default=False)  # 기본적으로 비활성화 상태
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # 기존 user_set 충돌 방지
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # 기존 user_set 충돌 방지
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = DB_TABLE_PREFIX + "customuser"  # 클래스 내부에서 직접 get_table_name() 호출 불가, 수동 지정

    def __str__(self):
        return self.email