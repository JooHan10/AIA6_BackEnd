from rest_framework import serializers
from users.models import User
from .models import User, password_validator, password_pattern, user_name_validator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from reviews.models import Review
from reviews.serializers import ReviewSerializer

from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.urls import reverse
from rest_framework_jwt.settings import api_settings


# 회원가입에 필요한 serializer
class SignUpSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        error_messages={
            "required": "비밀번호 확인은 필수 입력 사항입니다!",
            "blank": "비밀번호 확인은 필수 입력 사항입니다!",
            "write_only": True,
        }
    )
    
    class Meta:
        model = User
        fields = (
            "user_name",
            "password",
            "re_password",
            "email",
        )
        extra_kwargs = {
            "user_name": {
                "error_messages": {
                    "required": "ID는 필수 입력 사항입니다!",
                    "blank": "ID는 필수 입력 사항입니다!",
                }
            },
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": "비밀번호는 필수 입력 사항입니다!",
                    "blank": "비밀번호는 필수 입력 사항입니다!",
                },
            },
            "email": {
                "error_messages": {
                    "required": "email은 필수 입력 사항입니다!",
                    "invalid": "email 형식이 맞지 않습니다. 알맞은 형식의 email을 입력해주세요!",
                    "blank": "email은 필수 입력 사항입니다!",
                }
            },
        }

    def validate(self, data):
        user_name = data.get("user_name")
        password = data.get("password")
        re_password = data.get("re_password")

        # 아이디 유효성 검사
        if user_name_validator(user_name):
            raise serializers.ValidationError(detail={"username": "아이디는 6자 이상 30자 이하의 숫자, 영문 대/소문자를 포함하여야 합니다!"})

        # 비밀번호 & 비밀번호 확인 일치 검사
        if password != re_password:
            raise serializers.ValidationError(detail={"password": "비밀번호와 비밀번호 확인이 일치하지 않습니다!"})

        # 비밀번호 유효성 검사
        if password_validator(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 8자 이상의 영문 대소문자와 숫자, 특수문자를 포함하여야 합니다!"})

        # 비밀번호 유효성 검사
        if password_pattern(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 연속해서 3자리 이상 동일한 영문,숫자,특수문자 사용이 불가합니다!"})

        return data

    def create(self, validated_data):
        user_name = validated_data["user_name"]
        email = validated_data["email"]
        password = validated_data["password"]
        # 새로운 User 인스턴스를 생성과정에서 re_password가 예외를 발생시킬 수 있기 때문에 create() 메소드에서 check_password 필드를 제거합니다.
        validated_data.pop("re_password", None)
        user = User.objects.create(user_name=user_name, email=email,)
        
        user.set_password(password)

        # is_active = False로 지정해주어 email 인증을 하기 전에 접속 불가능하게 설정
        user.is_active = False
        user.save()

        # jwt 토큰 생성
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # email을 생성하여 보내는 부분
        message = f"{user.email}님 링크를 클릭해 계정을 활성화 해주세요\n"
        message += f"http://127.0.0.1:5500/auth.html?uidb64={urlsafe_base64_encode(force_bytes(user.pk))}&token={token}"
        email = EmailMessage('test', message, to=[user.email])
        email.send()

        return validated_data


# 마이 페이지 serializer
class MyPageSerializer(serializers.ModelSerializer):
    user_reviews = serializers.SerializerMethodField()
    
    def get_user_reviews(self, obj):
        user_id = obj.id
        reviews = Review.objects.filter(user_id=user_id)
        reviews = ReviewSerializer(reviews, many=True).data
        return reviews
    
    class Meta:
        model = User
        fields = (
            "id",
            "user_name",
            "email",
            "user_reviews",
        )


# 비밀번호 변경에 필요한 serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        error_messages={
            "required": "비밀번호 확인은 필수 입력 사항입니다!",
            "blank": "비밀번호 확인은 필수 입력 사항입니다!",
            "write_only": True,
        }
    )

    class Meta:
        model = User
        fields = (
            "password",
            "re_password",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": "비밀번호는 필수 입력 사항입니다!",
                    "blank": "비밀번호는 필수 입력 사항입니다!",
                },
            },
        }

    def validate(self, data):
        current_password = self.context.get("request").user.password
        password = data.get("password")
        re_password = data.get("re_password")

        # 현재 비밀번호와 바꿀 비밀번호 비교
        if check_password(password, current_password):
            raise serializers.ValidationError(detail={"password": "현재 사용 중인 비밀번호와 동일한 비밀번호입니다!"})

        # 비밀번호 & 비밀번호 확인 일치 검사
        if password != re_password:
            raise serializers.ValidationError(detail={"password": "비밀번호와 비밀번호 확인이 일치하지 않습니다!"})

        # 비밀번호 유효성 검사
        if password_validator(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 8자 이상의 영문 대소문자와 숫자, 특수문자를 포함하여야 합니다!"})

        # 비밀번호 유효성 검사
        if password_pattern(password):
            raise serializers.ValidationError(detail={"password": "비밀번호는 연속해서 3자리 이상 동일한 영문,숫자,특수문자 사용이 불가합니다!"})

        return data

    def update(self, instance, validated_data):
        instance.password = validated_data.get("password", instance.password)
        instance.set_password(instance.password)
        instance.save()

        return instance


# 로그인시 필요한 토큰 serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_name'] = user.user_name
        token["is_admin"] = user.is_admin
        return token