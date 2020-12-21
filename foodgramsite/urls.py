"""foodgramsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

from recipes import additional_views
from recipes.additional_views import get_ingredients

urlpatterns = [
    path("admin/", admin.site.urls),
    path("about/", include("django.contrib.flatpages.urls")),
    path("about-food/", views.flatpage, {"url": "/about-food/"}, name="about"),
    path("about-spec/", views.flatpage, {"url": "/about-spec/"}, name="about-spec"),
    path(
        "about-author/", views.flatpage, {"url": "/about-author/"}, name="about-author"
    ),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("ingredients/", additional_views.get_ingredients, name="ingredients"),
    path("", include("recipes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

handler404 = "recipes.views.page_not_found"
handler500 = "recipes.views.server_error"
