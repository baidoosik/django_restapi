from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', views.PostViewSet)


urlpatterns = [
    url(r'^api1/', include(router.urls)),
    # url(r'^posts/$', views.post_list, name='post_list'),
    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail')
]
