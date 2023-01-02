from .views import RegisterView, LoginView, RefreshView, MeView

from django.urls import path


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', RefreshView.as_view(), name='token_refresh'),
    # path('auth/register/', RegisterView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me')
]
