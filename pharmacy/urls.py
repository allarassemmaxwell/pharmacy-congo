"""pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
# from dashboard.views import PasswordChangeView
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/password/change/', PasswordChangeView.as_view(), name="account_change_password"),
    path('accounts/', include('allauth.urls')),
    path('', include('landing_app.urls')),
    path('dashboard/', include('dashboard_app.urls')),
    # path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#Modify Site Header
admin.site.site_header = 'Pharmacie Administration'
#Modify Site Title
admin.site.site_title = 'Pharmacie'
#Modify Site Index Title
admin.site.index_title = 'Pharmacie Administration'
#Modify Site URL
