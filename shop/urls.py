from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>', views.product_detail, name='product_detail'),
    path('customers/', views.customers_list, name='customers'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-list/category/<category_name>', views.product_list, name='products_by_category'),

    path('comment/add/<int:pk>', views.add_comment, name='add_comment'),
    #customers
    path('customers/', views.customers_list, name='customers'),
    path('customer-details/<int:pk>', views.customer_detail, name='customer_detail'),
    path('customer/create/', views.customer_create, name='customer_create'),
    path('customer/edit/<int:pk>', views.customer_edit, name='customer_edit'),
    path('customer/delete/<int:pk>', views.customer_delete, name='customer_delete'),
]