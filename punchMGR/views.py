from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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

            # 가입 시점에 username을 email과 동일하게 설정
            user.username = user.email
            
            # 이메일 인증을 위한 토큰 생성 및 저장
            token = get_random_string(length=32)
            user.email_token = token
            user.save()

            # 이메일 인증 링크 생성
            verification_link = request.build_absolute_uri(f'/accounts/verify/{token}/')

            # HTML 이메일 템플릿 사용
            subject = '이메일 인증 요청'
            html_message = render_to_string('email/verify_email.html', {'verification_link': verification_link})
            plain_message = strip_tags(html_message)  # HTML 태그 제거 후 텍스트 버전 생성
            
            try:
            # 이메일 전송
                send_mail(
                    subject,
                    plain_message,  # 텍스트 버전
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message=html_message,  # HTML 버전
                    fail_silently=False,
                )
            except Exception as e:
                # 이메일 전송 실패
                messages.error(request, "이메일 전송에 실패했습니다. 다시 시도해 주세요.")
                return redirect('register')

            # 메시지 프레임워크를 이용한 알림
            messages.success(request, "회원가입이 완료되었습니다. 이메일을 확인하여 인증을 완료하세요.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def verify_email(request, token):
    """
    이메일 인증 처리
    """
    try:
        user = CustomUser.objects.get(email_token=token)
        if user.is_active:
            # 이미 인증된 사용자인 경우
            messages.info(request, "이미 인증된 이메일입니다. 로그인 해주세요.")
        else:
            # 아직 인증되지 않은 사용자인 경우
            user.is_active = True
            user.email_token = None # 인증 후 토큰 삭제 (보안강화)
            user.save()
            messages.success(request, "이메일 인증이 완료되었습니다. 로그인해 주세요.")
        return redirect('login')
    except CustomUser.DoesNotExist:
        # 인증 토큰이 존재하지 않는 경우
        messages.error(request, "유효하지 않은 인증 링크입니다.")
        return redirect('home')


def home(request):
    return render(request, 'home.html')
