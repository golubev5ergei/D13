from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post_detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post_update/<int:pk>/', views.PostUpdate.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', views.PostDelete.as_view(), name='post_delete'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    # path('<int:post_id>/comment/', views.PostComment.as_view(), name='post_comment'),
    path('post_add', views.PostAdd.as_view(), name='post_add'),
    path('edit_page', views.edit_page, name='edit_page'),
    path('email-confirmation-sent/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', views.UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', views.EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', views.EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)