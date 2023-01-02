from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganizationView, TeamView, ReleaseView, SprintView, InvitationView, EmployeeSignUpView

router = DefaultRouter()
router.register('organization', OrganizationView, basename='organization')
router.register('team', TeamView, basename='team')
router.register('release', ReleaseView, basename='release')
router.register('sprint', SprintView, basename='sprint')

urlpatterns = [
    path('', include(router.urls)),
     path('invitation/', InvitationView.as_view(), name='invitation'),
     path('join/', EmployeeSignUpView.as_view(), name='join'),
]

app_name = 'organization'

