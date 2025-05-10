from django.urls import path
from accounts.views import SignUpView, LoginView, LogoutView, GetCSRFToken, UploadProfileView

urlpatterns = [
    # path('csrf_cookie/', GetCSRFToken.as_view(), name='csrf_cookie'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UploadProfileView.as_view(), name='profile'),
    path('profile/<int:bot_id>/', UploadProfileView.as_view(), name='get_profile'),
] 