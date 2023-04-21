from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post_detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post_update/<int:pk>/', views.PostUpdate.as_view(), name='post_update'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    # path('<int:post_id>/comment/', views.PostComment.as_view(), name='post_comment'),
    path('post_add', views.PostAdd.as_view(), name='post_add'),
    path('edit_page', views.edit_page, name='edit_page'),
    ]