from django.urls import path
from .import views

urlpatterns = [
    #public views
    path('', views.home, name='home'),
    path('enroll/', views.enroll, name='enroll'),
    path('exit/', views.exit_view, name='exit'),
    path('rules/', views.rules, name='rules'),
    path('buses/', views.buses_view, name='buses'),
    path('test-email/', views.test_email, name='test_email'),

 

    #admin views
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # bus management
    path('bus/add/', views.add_bus, name='add_bus'),
    path('bus/edit/<int:bus_id>/', views.edit_bus, name='edit_bus'),  
    path('bus/delete/<int:bus_id>/', views.delete_bus, name='delete_bus'),
    path('admin/edit-bus/<int:bus_id>/', views.edit_bus, name='edit_bus'),

    #logs
    path('logs/', views.view_logs, name='view_logs'),

    
    # Actions (use POST forms from templates)
    path('enrollment/update/<int:pk>/', views.update_enrollment_status, name='update_enrollment_status'),
    path('exit/update/<int:pk>/', views.update_exit_status, name='update_exit_status'),

    # stops
path('stop/add/', views.add_stop, name='add_stop'),
path('stop/edit/<int:pk>/', views.edit_stop, name='edit_stop'),
path('stop/delete/<int:pk>/', views.delete_stop, name='delete_stop'),


# logins (admin accounts)
path('manage-logins/', views.manage_logins, name='manage_logins'),
path('manage-logins/add/', views.add_admin, name='add_admin'),
path('manage-logins/delete/<int:pk>/', views.delete_admin, name='delete_admin'),


path('admin/enrollment/<int:pk>/update/', views.update_enrollment_status, name='update_enrollment_status'),
path('admin/exit/<int:pk>/update/', views.update_exit_status, name='update_exit_status'),

 path('dashboard/', views.dashboard, name='dashboard'),
    
   
   

]