from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('folders/', views.folder_list, name='folder_list'),
    path('folders/create/', views.folder_create, name='folder_create'),
    path('folders/<int:pk>/edit/', views.folder_edit, name='folder_edit'),
    path('folders/<int:pk>/delete/', views.folder_delete, name='folder_delete'),
    path('storedfiles/', views.storedfile_list, name='storedfile_list'),
    path('storedfiles/create/', views.storedfile_create, name='storedfile_create'),
    path('storedfiles/<int:pk>/edit/', views.storedfile_edit, name='storedfile_edit'),
    path('storedfiles/<int:pk>/delete/', views.storedfile_delete, name='storedfile_delete'),
    path('sharelinks/', views.sharelink_list, name='sharelink_list'),
    path('sharelinks/create/', views.sharelink_create, name='sharelink_create'),
    path('sharelinks/<int:pk>/edit/', views.sharelink_edit, name='sharelink_edit'),
    path('sharelinks/<int:pk>/delete/', views.sharelink_delete, name='sharelink_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
