from django.conf.urls.defaults import *
from scandinavian_auction.admin.views import get_products, admin_login, admin_main, del_product, edit_product, get_product, get_users, del_user,\
    add_product, add_auction, get_auctions, del_auction, edit_auction
from scandinavian_auction.auth.views import login, registration, log_out
from scandinavian_auction.views import main
from scandinavian_auction.products.views import products_list, show_product
from scandinavian_auction.categories.views import categories_list_admin, category_show_admin, add_category
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^$',main),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT}),
    
    
    #authorisation views
    (r'^login/$',login),
    (r'^registration/$',registration),
    (r'^logout',log_out),
    #end authorisation views
    
    #products views
    (r'^products/$', products_list),
    (r'^products/(\d+)/$', show_product),
    #end products views
    
    #admin views
    (r'^admin/$',admin_main),
    (r'^admin/login/$',admin_login),
    (r'^admin/users/$',get_users),
    (r'^admin/users/del/(\d+)/$',del_user),
    (r'^admin/products/add/$',add_product),
    (r'^admin/products/$',get_products),
    (r'^admin/products/del/(\d+)/$',del_product),
    (r'^admin/products/edit/(\d+)/$',edit_product),
    (r'^admin/products/(\d+)/$',get_product),
    (r'^admin/auctions/add/$',add_auction),
    (r'^admin/auctions/$',get_auctions),
    (r'^admin/auctions/del/(\d+)/$',del_auction),
    (r'^admin/auctions/edit/(\d+)/$',edit_auction),
    (r'^admin/categories/$', categories_list_admin),
    (r'^admin/categories/(\d+)', category_show_admin),
    (r'^admin/categories/add/$',add_category),
    
    
    #end admin views
    
    # Example:
    # (r'^auction/', include('auction.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
