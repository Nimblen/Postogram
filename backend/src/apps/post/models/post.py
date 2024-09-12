from django.db import models
from django.contrib.auth.models import User




class Post(models.Model):
    post_types = (
        ("image", "image"),
        ("video", "video"),
        ("story", "story"),
    )
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    post_type = models.CharField(max_length=10, choices=post_types)
    hashtags = models.ManyToManyField('post.Hashtag', related_name="posts", blank=True)

    def __str__(self):
        return self.name

def path_to_uploaded_file(instance, filename):
    return f"posts/{instance.post.pk}/{filename}"

class PostFile(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=path_to_uploaded_file)
    def __str__(self):
        return f"{self.post.name} - {self.name}"
    

    def save(self, **kwargs) -> None:
        if not self.name:
            self.name = f'{self.post.name} - {self.file.name}'
        return super().save(**kwargs)
    



class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post.name} - {self.author.username}"

    class Meta:
        unique_together = ("post", "author")


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_comments"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post.name} - {self.author.username}"


class PostCommentLike(models.Model):
    comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="likes"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment.author.username} - {self.author.username}"

    class Meta:
        unique_together = ("comment", "author")