from django.contrib import admin
from .models import Post, PostFile, Hashtag, PostComment, PostCommentLike, PostLike

# Register your models here.



admin.site.register(Post)
admin.site.register(PostFile)
admin.site.register(Hashtag)
admin.site.register(PostComment)
admin.site.register(PostCommentLike)
admin.site.register(PostLike)