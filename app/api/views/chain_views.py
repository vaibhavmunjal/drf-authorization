from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.models import Blog, Comments
from app.api.serializers import BlogSerializer, CommentSerializer
from app.api.permissions import (
    ChainPermissions,
    RequestPermissions,
    ActionPermissions,
    CustomPermissions,
)


class BlogAPIView(ModelViewSet):
    # http-method: permission_list
    # to set permission for corrosponding method
    request_perms_map = {
        "GET": ["app.view_blog"]
    }
    # drf-action: permission_list
    # to set permission for corrosponding method
    action_perms_map = {
        "new_action": ["forbidden_403"],
        "list": ["app.view_blog"]
    }
    # drf-action, http-method: permission_classes
    # to set permission classes for corrosponding method/action
    permissions_map = {
        "GET": (RequestPermissions,),
        ("PUT", "PATCH"): (ActionPermissions,),

        "list": (CustomPermissions, RequestPermissions),
        ("update", "partial_update"): (CustomPermissions, ActionPermissions),
        "new_action": (ActionPermissions,)
    }

    @action(methods=["GET"], detail=False)
    def new_action(self, request):
        return Response({"Permissions works with dynamic/new action routers?"})
    

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (ChainPermissions,)


class CommentsAPIView(ModelViewSet):
    # http-method: permission_list
    # to set permission for corrosponding method
    request_perms_map = {
        "GET": ["app.view_comments"]
    }
    # drf-action: permission_list
    # to set permission for corrosponding method
    action_perms_map = {
        "list": ["app.view_comments"]
    }
    # drf-action, http-method: permission_classes
    # to set permission classes for corrosponding method/action
    permissions_map = {
        "GET": (RequestPermissions,),
        ("PUT", "PATCH"): (RequestPermissions,),

        "list": (CustomPermissions, ActionPermissions),
        ("update", "partial_update"): (CustomPermissions, ActionPermissions),
    }

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ChainPermissions,)
