from django.conf.urls import url

from tread import views

urlpatterns = [
    url(r'thread/', views.CreateThreadView.as_view(),),
    url(r'message/', views.CreateMessageView.as_view(),),
]
