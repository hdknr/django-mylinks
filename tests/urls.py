from django.conf.urls import url, include


def article_detail(request, id):
    pass


urlpatterns = [
    url(r'^oembed/', include('mylinks.oembed.urls')),
    url(r'^article/(?P<id>\d+)', article_detail, name='article_detail'),
]
