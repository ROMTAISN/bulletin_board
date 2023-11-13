from django.urls import path

from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('create', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('response/<post_id>/', add_response, name='add_response'),
    path('responses', ResponsePost.as_view(), name='responses'),
    path('post_list/<int:pk>', PostListView.as_view(), name='post_list'),
    path('responses/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('response/<int:pk>/accept/', response_accept, name='response_accept'),
]
