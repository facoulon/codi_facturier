"""codi_facturier URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from facturier.views import IndexView, CustomerCreateView, CustomerList, CustomerDetail, CustomerUpdateView, CustomerDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls,),

    url(r'^login/$', auth_views.LoginView.as_view(),  name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='index'),  name='logout'),
    url(r"^customer/create/$", CustomerCreateView.as_view(), name="customer-create"),
    url(r"^customer/list/$", CustomerList.as_view(), name="customer-list"),
    url(r"^customer/(?P<slug>[-\w]+)/detail$", CustomerDetail.as_view(), name="customer-detail"),
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r"^customer/(?P<slug>[-\w]+)/edit$", CustomerUpdateView.as_view(), name="customer-edit"),
    url(r"^customer/(?P<slug>[-\w]+)/delete$", CustomerDeleteView.as_view(), name="customer-delete"),
    
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
