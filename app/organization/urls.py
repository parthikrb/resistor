from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganizationView, TeamView, SprintView

router = DefaultRouter()
router.register('organization', OrganizationView, basename='organization')
router.register('team', TeamView, basename='team')
router.register('sprint', SprintView, basename='sprint')

urlpatterns = [
    path('', include(router.urls))
]

app_name = 'organization'

