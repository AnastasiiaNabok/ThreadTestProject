from django.conf.urls import url

from tread import views

urlpatterns = [
    url(r'threads/', views.TreadCreateAPIView.as_view(),),
]
