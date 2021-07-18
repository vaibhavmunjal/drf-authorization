"""Default + Custom Permissions APIView Example
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated


from app.models import Blog, Comments
from app.api.serializers import BlogSerializer, CommentSerializer
from app.api.permissions import CustomPermissions


class BlogAPIView(ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (CustomPermissions,)


class CommentsAPIView(ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, CustomPermissions, DjangoObjectPermissions)
