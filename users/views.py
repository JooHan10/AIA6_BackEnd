from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from users.serializers import SignUpSerializer, ChangePasswordSerializer, MyPageSerializer
from users.models import User
from django.utils import timezone


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