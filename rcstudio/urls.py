"""rcstudio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include

import debug_toolbar

import event_management.urls

# ------- ADMIN PANNEL CUSTOMIZATION

admin.site.site_header = 'RC STUDIO'
admin.site.enable_nav_sidebar = True
admin.site.site_title = 'Admin • RC Studio'
admin.site.index_title = 'Welcome'
admin.site.name = 'RC Studio'
admin.site.site_url = '/admin'

urlpatterns = [
    path('studio/', include(event_management.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('__debug__/', include(debug_toolbar.urls))
]
