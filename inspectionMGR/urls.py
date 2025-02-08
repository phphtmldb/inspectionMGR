from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main.html'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),  # 로그인, 로그아웃, 비밀번호 변경 기능
    path('accounts/signup/', include('punchMGR.urls')),  # 회원가입 기능 추가
]
