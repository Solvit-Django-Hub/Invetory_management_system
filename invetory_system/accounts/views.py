from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


from .serializers import  ProfileUpdateSerializer, UserSerializer, CreateUserSerializer



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        })

    def put(self, request):
        serializer = ProfileUpdateSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "message": "Profile updated successfully.",
                "user": {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                }
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful."},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception:
            return Response(
                {"error": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )

class IsAdminUser(BasePermission):
    message = "Only administrators can access this resource."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )
class IsAdminOrManager(BasePermission):
    message = "Only administrators and managers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "manager"]
        )


class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

class CreateUserView(APIView):
    permission_classes = [IsAdminOrManager]

    def post(self, request):

        
        if (
            request.user.role == "manager"
            and request.data.get("role") == "admin"
        ):
            return Response(
                {
                    "error": "Managers cannot create admin accounts."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User created successfully.",
                    "user": {
                        "user_id": user.user_id,
                        "name": user.name,
                        "email": user.email,
                        "role": user.role,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )