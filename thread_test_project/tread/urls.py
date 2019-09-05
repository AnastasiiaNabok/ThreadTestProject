from django.conf.urls import url

from tread import views

urlpatterns = [
    url('threads', views.GetAllThreadsForUserApiView.as_view(),),
    url('create_thread/', views.CreateThreadView.as_view(),),
    url(r'delete_thread/$', views.DeleteThreadAPI.as_view(),),
    url('create_message/', views.CreateMessageView.as_view(),),
    url(r'^read_messages/', views.MessageUpdateView.as_view(),),
    url(r'^unread_messages/', views.UnreadMessagesAPIView.as_view(),),
]
