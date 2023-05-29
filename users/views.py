from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from users.serializers import SignUpSerializer, ChangePasswordSerializer, MyPageSerializer
from users.models import User
from django.utils import timezone

import traceback
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
import jwt
from django.conf import settings
secret_key = settings.SECRET_KEY


# 회원가입
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# 회원 비활성화
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # 회원 비활성화
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user.email == user.email:
            user.withdraw = True
            user.withdraw_at = timezone.now()
            user.is_active = False
            user.save()
            return Response({"message": "사용자 계정이 비활성화 되었습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)


# 비밀번호 변경
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user.email == user.email:
            serializer = ChangePasswordSerializer(user, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "비밀번호 변경이 완료되었습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

# 이메일 인증관련
class UserActivate(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            # JWT 토큰 검증
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            if payload['user_id'] != user.id:
                return Response('토큰이 올바르지 않습니다', status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response('만료된 토큰입니다', status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response('잘못된 토큰입니다', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())

        if user is not None:
            user.is_active = True
            user.save()
            return Response(user.email + '계정이 활성화 되었습니다', status=status.HTTP_200_OK)
        else:
            return Response('사용자를 찾을 수 없습니다', status=status.HTTP_400_BAD_REQUEST)


# 마이 페이지
class MyPageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # 마이 페이지 - 회원 정보 조회
    def get(self, request, user_id):
        my_page = get_object_or_404(User, id=user_id)
        if request.user.email == my_page.email:
            serializer = MyPageSerializer(my_page)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)