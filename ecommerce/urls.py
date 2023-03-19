from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dataApi/', include("dataApi.urls")),
    path('', include("dataApi.urls")),
]
