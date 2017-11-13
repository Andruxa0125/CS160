"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from django.conf.urls.static import static
from django.conf import settings

# My imports
from facefinder.forms import LoginForm
from facefinder import views as my_views



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', my_views.signup, name='signup'),
    url(r'^(?P<username>[\w.@+-]+)/main/encryptedSessionToken&=int(?P<session_ID>\d+)/$', my_views.main, name='main'),
    url(r'^$', my_views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
