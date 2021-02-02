from django.conf.urls import url
from django.urls import path, include, re_path
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'accounts', ListAccountsViewSet)
router.register(r'admin_store', AdminStoreViewSet)

urlpatterns = [
      # path for logout
      path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
      # path for registration
      path('register', RegisterApi.as_view()),
      # path for the cart list
      path('order_list/', Cart.as_view(),name="cart"),
      # path for updating the cart items
      path('update_list/', UpdateItem.as_view()),
      # path for the list api
      path('store/', StoreViewSet.as_view()),
]

urlpatterns += router.urls
