from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganizationView, TeamView

router = DefaultRouter()
router.register('organization', OrganizationView, basename='organization')
router.register('team', TeamView, basename='team')

urlpatterns = [
    path('', include(router.urls))
]

app_name = 'organization'

