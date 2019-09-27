from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from .models import User, Relationship
from .serializers import UserSerializer, RelationshipSerializer
from .permissions import IsSelf


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.action == 'follow':
            return RelationshipSerializer

        return serializer

    def get_permissions(self):
        if self.action == 'create':
            return []

        permissions = super().get_permissions()

        if self.action == ['update', 'partial_update']:
            permissions.append(IsSelf())

        if self.action == 'destroy':
            permissions.append(IsAdminUser())

        return permissions

    @action(['POST'], True)
    def follow(self, request, pk):
        from_user = request.user
        to_user = self.get_object()

        # relationship = Relationship.objects.create(
        #     from_user=from_user,
        #     to_user=to_user,
        #     is_agree=to_user.is_pubic,
        # )

        serializer = self.get_serializer(data={
            'from_user': from_user.id,
            'to_user': to_user.id,
            'is_agree': to_user.is_public,
        })

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'status': 'ok'})
