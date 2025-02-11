from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    이메일을 아이디로 사용하는 회원가입 폼
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일 입력'})
    )
    
    password1 = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호 입력'}),
    )
    
    password2 = forms.CharField(
        label="비밀번호 확인",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호 확인'}),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def clean_email(self):
        """
        이메일 중복 체크
        """
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 사용 중인 이메일입니다.")
        return email

    def clean_password1(self):
        """
        비밀번호 강도 검사 (선택 사항)
        """
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise forms.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        return password
