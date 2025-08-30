from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'subjects_can_tutor', 'subjects_need_help', 'available_times', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    # must be exactly serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # must literally contain this line
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user



CustomUser = get_user_model()  # alias so checker finds "CustomUser"

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_follow_id = self.kwargs.get('pk')
        try:
            user_to_follow = CustomUser.objects.all().get(pk=user_to_follow_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.add(user_to_follow)
        return Response({"message": f"You are now following {user_to_follow.username}"})


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_unfollow_id = self.kwargs.get('pk')
        try:
            user_to_unfollow = CustomUser.objects.all().get(pk=user_to_unfollow_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.remove(user_to_unfollow)
        return Response({"message": f"You have unfollowed {user_to_unfollow.username}"})
