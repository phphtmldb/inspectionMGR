from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser

def register(request):
    """
    이메일을 이용한 회원가입 뷰
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 이메일 인증 전까지 계정 비활성화

            # 이메일 인증을 위한 토큰 생성 및 저장
            token = get_random_string(length=32)
            user.email_token = token
            user.save()

            # 이메일 인증 링크 생성
            verification_link = request.build_absolute_uri(f'/accounts/verify/{token}/')

            # 이메일 전송
            send_mail(
                '이메일 인증',
                f'아래 링크를 클릭하여 이메일을 인증하세요: {verification_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            # 메시지 프레임워크를 이용한 알림
            messages.success(request, "회원가입이 완료되었습니다. 이메일을 확인하여 인증을 완료하세요.")

            # 홈페이지로 이동 (urls.py에서 name='home'으로 설정한 URL로 이동한다고 가정)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def email_verification_sent(request):
    """
    기존에 있던 뷰.
    더 이상 사용하지 않는다면 삭제해도 무방합니다.
    """
    return render(request, 'email_verification_sent.html')


def verify_email(request, token):
    """
    이메일 인증 처리
    """
    user = get_object_or_404(CustomUser, email_token=token)
    user.is_active = True  # 이메일 인증 완료 후 활성화
    user.email_token = ""  # 🔹 인증 후 토큰 삭제 (보안 강화)
    user.save()
    
    # 이메일 인증 완료 후 메시지 표시 및 로그인 페이지로 이동
    messages.success(request, "이메일 인증이 완료되었습니다. 로그인해 주세요.")
    return redirect('login')


def home(request):
    return render(request, 'home.html')
