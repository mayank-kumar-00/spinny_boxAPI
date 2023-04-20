from django.urls import path
from .views import BoxView, TokenObtainPairViewset, RefreshTokenViewset
urlpatterns = [
    path('login/', TokenObtainPairViewset.as_view(), name='login'),
    path('token-regenerate/', RefreshTokenViewset.as_view(), name="token_regenerate"),
    path('box/', BoxView.as_view(), name="box_view"),
]
