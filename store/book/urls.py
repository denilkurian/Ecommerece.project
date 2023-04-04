from django.urls import path
from . import views
from .views import list1, detail1, BookCheckoutView, SearchResultView, Filter, add_review, delete_review

urlpatterns =[
    path('',views.homepage,name='homepage'),
    path('list1/',list1.as_view(),name='list1'),
############
    path("signup/", views.signup, name='signup'),
    path("signin/", views.signin, name='signin'),
    path("signout/", views.signout, name='signout'),
    path('detail1/<int:pk>/',detail1.as_view(),name='detail1'),
##############
    path('checkout/<int:pk>/', BookCheckoutView.as_view(), name='checkout-view'),
    ###########
path('search/',SearchResultView.as_view(),name='search'),
    ###########3
path('filter/',Filter.as_view(),name='filter'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
##############
    path('product/<int:pk>/', add_review, name='add_review'),
path('delete/<int:review_id>/', delete_review, name='delete_review'),
###############







]

