from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'customers'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='customers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='customers/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             success_url='/portal/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='customers/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='customers/password_reset_confirm.html',
             success_url='/portal/reset/done/'
         ),
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='customers/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Customer Portal
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Bookings
    path('bookings/', views.bookings, name='bookings'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('quick-booking/', views.quick_booking, name='quick_booking'),
    
    # Quotes
    path('quotes/', views.quotes, name='quotes'),
    path('quotes/<int:quote_id>/', views.quote_detail, name='quote_detail'),
    path('quotes/<int:quote_id>/accept/', views.accept_quote, name='accept_quote'),
    path('quotes/<int:quote_id>/book/', views.book_from_quote, name='book_from_quote'),
    
    # Service History
    path('service-history/', views.service_history, name='service_history'),
]
