from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from punchMGR import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main.html'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),  # 로그인, 로그아웃, 비밀번호 변경 기능
    path('accounts/signup/', views.register, name='signup'),  # 올바른 뷰로 수정
    path('accounts/', include('punchMGR.urls')),  # 이메일 인증 관련 URL 포함
]    
