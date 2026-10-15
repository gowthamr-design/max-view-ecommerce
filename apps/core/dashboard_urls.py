from django.urls import path
from . import dashboard_views as views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Overview
    path('', views.DashboardHomeView.as_view(), name='home'),

    # Products Management CRUD
    path('products/', views.AdminProductListView.as_view(), name='products_list'),
    path('products/add/', views.AdminProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.AdminProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.AdminProductDeleteView.as_view(), name='product_delete'),

    # Categories Management CRUD
    path('categories/', views.AdminCategoryListView.as_view(), name='categories_list'),
    path('categories/add/', views.AdminCategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.AdminCategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.AdminCategoryDeleteView.as_view(), name='category_delete'),

    # Orders Management
    path('orders/', views.AdminOrderListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', views.AdminOrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/delete/', views.AdminOrderDeleteView.as_view(), name='order_delete'),

    # Customer Accounts
    path('customers/', views.AdminCustomerListView.as_view(), name='customers_list'),
    path('customers/<int:pk>/', views.AdminCustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/toggle-status/', views.AdminCustomerToggleStatusView.as_view(), name='customer_toggle_status'),
    path('customers/<int:pk>/delete/', views.AdminCustomerDeleteView.as_view(), name='customer_delete'),

    # Website Content
    path('content/', views.AdminContentManagementView.as_view(), name='content_management'),
    path('content/slide/add/', views.AdminSlideCreateView.as_view(), name='slide_create'),
    path('content/slide/<int:pk>/delete/', views.AdminSlideDeleteView.as_view(), name='slide_delete'),
    path('content/contact/<int:pk>/resolve/', views.AdminContactResolveView.as_view(), name='contact_resolve'),
]
