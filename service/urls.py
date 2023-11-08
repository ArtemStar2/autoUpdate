from django.urls import include, path
from rest_framework import routers
from .views import ServiceViewSet, SocialNetworkViewSet

router = routers.DefaultRouter()
router.register("services", ServiceViewSet, "services")
router.register("social", SocialNetworkViewSet, "social")

urlpatterns = [
    path('', include(router.urls)),
]