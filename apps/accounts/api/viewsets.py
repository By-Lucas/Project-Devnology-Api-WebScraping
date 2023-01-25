from rest_framework import generics, viewsets
from rest_framework import permissions, authentication

from accounts.models import User
from accounts.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_queryset(self, format=None):
        query = User.objects.filter(email=self.request.user)
        return query
    

class UsersListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication] 
    serializer_class = UserSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = User.objects.all()
            return queryset
    



