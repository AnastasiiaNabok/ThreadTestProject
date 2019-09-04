from django.conf.urls import url

from tread import views

urlpatterns = [
    url(r'threads/', views.GetAllThreadsForUserApiView.as_view(),),
    url(r'create_thread/', views.CreateThreadView.as_view(),),
    url(r'delete_thread/(?P<pk>\d+)/$', views.DeleteThreadAPI.as_view(),),
    url(r'create_message/', views.CreateMessageView.as_view(),),
    url(r'update_message/(?P<pk>\d+)/$', views.MessageUpdateView.as_view(),),
]
