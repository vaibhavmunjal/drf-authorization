from django.db import models
from django.contrib.auth import get_user_model

class Blog(models.Model):
    title = models.SlugField(max_length=500)
    sub_title = models.CharField(max_length=2000)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Create Custom permission
        permissions = (
            ("can_add_blog", "Can Add Blog"),
            ("can_view_blog", "Can View Blog"),
            ("can_change_blog", "Can Change Blog"),
            ("can_delete_blog", "Can Delete Blog"),
        )


class Comments(models.Model):
    Comment = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        # Create Custom permission
        permissions = (
            ("can_add_comments", "Can Add Comments"),
            ("can_view_comments", "Can View Comments"),
            ("can_change_comments", "Can Change Comments"),
            ("can_delete_comments", "Can Delete Comments"),
        )
