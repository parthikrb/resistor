from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganizationView

router = DefaultRouter()
router.register('organization', OrganizationView, basename='organization')

urlpatterns = [
    path('', include(router.urls))
]

app_name = 'organization'

