"""
URL configuration for goyang_lidah_jogja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main app (landing page and other main features)
    path('', include('main.urls', namespace='main')),
    
    # Event manager app
    path('event_manager/', include('managerDashboard.urls')),
    path('wishlist/', include('goyangNanti.urls', namespace='wishlist')),
    
    # UlasGoyangan app (for reviews)
    path('ulasGoyangan/', include('ulasGoyangan.urls', namespace='ulasGoyangan')),
    
    # userPreferences app (for editing user preferences)
    path('userPreferences/', include('userPreferences.urls', namespace='userPreferences')),
]
