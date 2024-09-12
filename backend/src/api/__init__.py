from . import post, user


urlpatterns = post.urlpatterns
urlpatterns += user.urlpatterns     