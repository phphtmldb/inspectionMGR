from django.urls import path
from punchMGR import views  # views 모듈 전체를 임포트

urlpatterns = [
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
]
