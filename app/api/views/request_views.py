from rest_framework.viewsets import ModelViewSet


from app.models import Blog, Comments
from app.api.serializers import BlogSerializer, CommentSerializer
from app.api.permissions import RequestPermissions

class BlogAPIView(ModelViewSet):
    # request: permission_list
    # to set permission for corrosponding method
    request_perms_map = {
        "GET": ["app.view_blog"]
    }
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (RequestPermissions,)

class CommentsAPIView(ModelViewSet):
    # request: permission_list
    # to set permission for corrosponding method
    request_perms_map = {
        "GET": ["app.view_comments"]
    }
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (RequestPermissions,)
