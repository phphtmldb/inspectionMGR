from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from punchMGR import views

urlpatterns = [
    # Django 내장 관리자 경로를 'django_admin/'으로 변경
    path('django_admin/', admin.site.urls),  
    
    # 메인
    path('', TemplateView.as_view(template_name='main.html'), name='home'),
    
    # 계정/인증 관련
    path('accounts/', include('django.contrib.auth.urls')),  # 로그인, 로그아웃, 비밀번호 변경 기능
    path('accounts/signup/', views.register, name='signup'),  # 회원가입
    path('accounts/', include('punchMGR.urls')),             # 이메일 인증 등 추가 URL
]