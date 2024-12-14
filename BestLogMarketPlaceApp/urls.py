from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.maintain, name='maintain'),
    path('p_about', views.about, name='p_about'),
    # path('products', views.products, name='products'),
    path('contact', views.contact, name='contact'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('profile_page', views.profile_page, name='profile_page'),
    path('payment_page',views.payment_page, name = 'payment_page'),
    path('pending',views.pending, name = "pending"),
    path('payment_history',views.payment_history, name = "payment_history"),
    path('orders',views.orders, name = "orders"),
    path('order_detail/<str:product_id>/',views.order_detail, name = "order_detail"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('category/<int:category_id>/products/', views.category_products_view, name='category_products'),
    path('privacy_page/', views.privacy_page, name='privacy_page'),
    path('terms_page/', views.terms_page, name='terms_page'),
    path('rules_page/', views.rules_page, name='rules_page'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='BestLogMarketPlaceApp/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='BestLogMarketPlaceApp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='BestLogMarketPlaceApp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='BestLogMarketPlaceApp/password_reset_complete.html'), name='password_reset_complete'),


 ]
