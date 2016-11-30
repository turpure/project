"""james_login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
import login.views as login_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', login_views.home, name='home'),
    url(r'^home/register/', login_views.register, name='register'),
    url(r'^home/logout', login_views.logout, name='logout'),
    url(r'^home/login', login_views.login, name='login'),
    url(r'^home/dashboard', login_views.dashboard, name='dashboard'),
    url(r'^home/shops', login_views.shops, name='shops'),
    url(r'^home/remove_all_shops', login_views.remove_all_shops, name='remove_all_shops'),
    url(r'^home/get_shops', login_views.get_shops, name='get_shops'),
    url(r'^home/add_shops', login_views.add_shops, name='add_shops'),
    url(r'^home/edit_shops', login_views.edit_shops, name='edit_shops'),
    url(r'^home/delete_shops', login_views.delete_shops, name='delete_shops'),
    url(r'^home/product', login_views.product, name='product'),
    url(r'^home/kwproduct', login_views.kwproduct, name='kwproduct'),
    url(r'^home/keywords$', login_views.keywords, name='keywords'),
    url(r'^home/show_product$', login_views.show_product, name='show_product'),
    url(r'^home/update_shops', login_views.update_shops, name='update_shops'),
    url(r'^home/delete_product', login_views.delete_product, name='delete_product'),
    url(r'^home/like_product$', login_views.like_product, name='like_product'),
    url(r'^home/delete_kw_product$', login_views.delete_kw_product, name='delete_kw_product'),
    url(r'^home/like_kw_product$', login_views.like_kw_product, name='like_kw_product'),
    url(r'^home/like$', login_views.like, name='like'),
    url(r'^home/wanted_product$', login_views.product_liked, name='product_liked'),
    url(r'^home/editsku$', login_views.editsku, name='editsku'),
    url(r'^home/add_keywords$', login_views.add_keywords, name='add_keywords'),
    url(r'^home/get_keywords$', login_views.get_keywords, name='get_keywords'),
    url(r'^home/delete_keywords$', login_views.delete_keywords, name='delete_keywords'),
    url(r'^home/edit_keywords$', login_views.edit_keywords, name='edit_keywords'),
    url(r'^home/sync_keywords$', login_views.sync_keywords, name='sync_keywords'),
    url(r'^home/show_kw_product$', login_views.show_kw_product, name='show_kw_product'),
    url(r'^home/watch_kw_shop$', login_views.watch_kw_shop, name='watch_kw_shop'),
    url(r'home/remove_liked', login_views.remove_liked, name='remove_liked'),
]
