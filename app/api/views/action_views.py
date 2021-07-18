from rest_framework.viewsets import ModelViewSet


from app.models import Blog, Comments
from app.api.serializers import BlogSerializer, CommentSerializer
from app.api.permissions import ActionPermissions

class BlogAPIView(ModelViewSet):
    # action: permission_list
    # to set permission for corrosponding method
    action_perms_map = {
        "list": ["app.can_view_blog"],
        "retrieve": ["forbidden_403"],
    }
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (ActionPermissions,)

class CommentsAPIView(ModelViewSet):
    # action: permission_list
    # to set permission for corrosponding method
    action_perms_map = {
        "list": ["app.can_view_comments"]
    }
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ActionPermissions,)
