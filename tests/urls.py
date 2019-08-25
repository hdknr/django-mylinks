from django.urls import path, re_path, include


def article_detail(request, id):
    pass


urlpatterns = [
    path('mylinks/', include('mylinks.urls')),
    re_path(r'^article/(?P<id>\d+)', article_detail, name='article_detail'),
]
