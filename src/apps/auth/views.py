from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status, generics, exceptions
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    LogoutSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "User registered successfully.", "user_id": user.id},
            status=status.HTTP_201_CREATED
        )


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user", None)

        user.status = "active"
        user.last_login = timezone.now()
        user.save()

        token = TokenObtainPairSerializer.get_token(user)
        return Response(
            {
                "refresh": str(token),
                "access": str(token.access_token),
                "user": UserSerializer(user).data,
                "message": "Login successful."
            },
            status=status.HTTP_200_OK
        )

        


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserLogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken(refresh_token)
        try:
            token.blacklist()
            user = request.user
            user.status = "inactive"
            user.save()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            raise exceptions.APIException(
                {"detail": "An error occurred while logging out.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
