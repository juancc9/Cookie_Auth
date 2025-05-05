from django.urls import path
from .views import LoginConCookieView, LogoutConCookieView, CustomLoginView

urlpatterns = [
    path('loginer/', LoginConCookieView.as_view(), name='auth'),
    path('logout/', LogoutConCookieView.as_view(), name='logout'),
    path('auth/login/', CustomLoginView.as_view(), name='auth')

]
