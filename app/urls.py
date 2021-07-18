from django.urls import path, include

from rest_framework.routers import SimpleRouter

from app.api.views.views import (
    BlogAPIView,
    CommentsAPIView,
)
from app.api.views.request_views import (
    BlogAPIView as RBlogAPIView,
    CommentsAPIView as RCommentsAPIView,
)
from app.api.views.action_views import (
    BlogAPIView as ABlogAPIView,
    CommentsAPIView as ACommentsAPIView,
)
from app.api.views.chain_views import (
    BlogAPIView as ChBlogAPIView,
    CommentsAPIView as ChCommentsAPIView,
)


router = SimpleRouter()

router.register("custom/blog", BlogAPIView, basename="custom_blog")
router.register("custom/comments", CommentsAPIView, basename="custom_comments")

router.register("request/blog", RBlogAPIView, basename="request_blog")
router.register("request/comments", RCommentsAPIView, basename="request_comments")

router.register("action/blog", ABlogAPIView, basename="action_blog")
router.register("action/comments", ACommentsAPIView, basename="action_comments")

router.register("chain/blog", ChBlogAPIView, basename="chain_blog")
router.register("chain/comments", ChCommentsAPIView, basename="chain_comments")

urlpatterns = [
    path("", include(router.urls), name="api_urls")
]
