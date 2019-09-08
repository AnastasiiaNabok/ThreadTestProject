from django.conf.urls import url

from thread import views

urlpatterns = [
    url(r'threads', views.GetAllThreadsForUserApiView.as_view(),),
    url(r'create_thread/', views.CreateThreadView.as_view(),),
    url(r'^thread/$', views.ThreadMessagesAPIView.as_view(),),
    url(r'^delete_thread/$', views.DeleteThreadAPI.as_view(),),
    url(r'^create_message/', views.CreateMessageView.as_view(),),
    url(r'^read_messages/', views.MessageUpdateView.as_view(),),
    url(r'^unread_messages/', views.UnreadMessagesAPIView.as_view(),),
]
