from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'agents', views.AgentViewSet)
router.register(r'scripts', views.ScriptViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'checks', views.CheckViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
