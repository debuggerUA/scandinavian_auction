from django.conf.urls.defaults import *
from scandinavian_auction.admin.views import get_products, admin_login, admin_main, del_product, edit_product, get_product, get_users, del_user,\
    add_product, add_auction, get_auctions, del_auction, edit_auction, user_page, buy_it, add_user
from scandinavian_auction.auth.views import login, registration, log_out
from scandinavian_auction.views import main
from scandinavian_auction.auction.views import show_auction, show_auctions
from scandinavian_auction.products.views import products_list, show_product, make_bid
from scandinavian_auction.categories.views import categories_list_admin, category_show_admin, add_category, show_category, show_categories, del_category
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^$',main), #covered by test (simp)
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT}),
    
    
    #authorisation views
    (r'^login/$',login), #covered by test (simp)
    (r'^registration/$',registration), #covered by test (simp)
    (r'^logout/$',log_out), #covered by test (simp)
    (r'^accounts/login/$',login), #covered by test (simp)
    #end authorisation views
    
    #products views
    (r'^products/$', products_list), #covered by test (simp)
    (r'^products/(\d+)/$', show_product), #covered by test (simp)
    #end products views
    
    #categories
    (r'^categories/$', show_categories), #covered by test (simp)
    (r'^categories/(\d+)/$', show_category), #covered by test (simp)
    #end categories
    
    #auctions
    (r'^auctions/$', show_auctions), #covered by test (simp)
    (r'^auctions/(\d+)/$', show_auction), #covered by test (simp)
    #end auctions
    
    #admin views
    (r'^admin/$',admin_main), #covered by test (simp)
    (r'^admin/login/$',admin_login), #covered by test (simp)
    (r'^admin/users/$',get_users), #covered by test (simp)
    (r'^admin/users/add/$',add_user), #covered by test (simp)
    (r'^admin/users/del/(\d+)/$',del_user), #covered by test (simp)
    (r'^admin/products/add/$',add_product), #covered by test (simp)
    (r'^admin/products/$',get_products), #covered by test (simp)
    (r'^admin/products/del/(\d+)/$',del_product), #covered by test (simp)
    (r'^admin/products/edit/(\d+)/$',edit_product),
    (r'^admin/products/(\d+)/$',get_product),
    (r'^admin/auctions/add/$',add_auction), #covered by test (simp)
    (r'^admin/auctions/$',get_auctions), #covered by test (simp)
    (r'^admin/auctions/del/(\d+)/$',del_auction), #covered by test (simp)
    (r'^admin/auctions/edit/(\d+)/$',edit_auction),
    (r'^admin/categories/$', categories_list_admin), #covered by test (simp)
    (r'^admin/categories/(\d+)/$', category_show_admin), #covered by test (simp)
    (r'^admin/categories/add/$',add_category), #covered by test (simp)
    (r'^admin/categories/del/(\d+)/$',del_category), #covered by test (simp)
    #end admin views
    
    #buy product
    (r'^buy/(\d+)/$', buy_it),
    #end buy
    
    #user pages
    (r'^user/$', user_page),
    #end user pages
    
    #bid urls
    (r'^makebid/(\d+)/$', make_bid),
    #end bid urls
    
    #json update
    #aj_update_main/$', aj_update_main),
    #end json update
    
    # Example:
    # (r'^auction/', include('auction.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
