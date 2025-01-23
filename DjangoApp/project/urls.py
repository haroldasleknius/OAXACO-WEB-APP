from django.urls import path

from . import views
import os

urlpatterns = [
    path('', views.index, name='index'),
    path('complaint/', views.complaintForm, name='complaint'), 
    path('error/', views.error, name='error'),
    path('my-tables/', views.tables, name='my-tables'),
    path('my-tables/change_table_clean_status/<str:waiter>/<str:table_num>/<str:current_status>', views.change_table_clean_status, name='change_table_clean_status'),
    path('my-tables/change_table_available_status/<str:waiter>/<str:table_num>/<str:current_status>', views.change_table_available_status, name='change_table_available_status'),
    path('my-tables/change_table_assistance_status/<str:waiter>/<str:table_num>/<str:current_status>', views.change_table_assistance_status, name='change_table_assistance_status'),
    path('manage-tables/', views.manageTables, name='manage-tables'),
    path('manage-tables/add_table_assignment/<str:waiter>/<str:table_num>/<str:current_status>', views.add_table_assignment, name='add_table_assignment'),
    path('manage-tables/remove_table_assignment/<str:waiter>/<str:table_num>/<str:current_status>', views.remove_table_assignment, name='remove_table_assignment'),
    path('welcome/', views.waiterLanding, name='welcome'),
    path('FAQ-page/', views.FAQ, name='FAQ'),
    path('about-us/', views.about, name='about'),
    path('Change-menu/', views.change, name='change'),
    path('Add-to-menu/', views.add, name='add'),
    path('payment/', views.payment_form_view, name='payment'),
    path('menu/', views.menu, name='menu'),
    path('view-complaints/', views.view_complaints, name='view_complaints'),
    path('login/', views.loginForm, name='login'),
    path('view-basket/', views.view_basket, name='view_basket'),
    path('increment-basket/<str:page_name>/<str:item_name>/<str:filter>', views.increment_item_basket_quantity, name='increment_item_basket_quantity'),
    path('decrement-basket/<str:page_name>/<str:item_name>/<str:filter>', views.decrement_item_basket_quantity, name='decrement_item_basket_quantity'),
    path('menu/<str:filter>', views.menu, name='change'),
    path('view-complaints/', views.view_complaints, name='view_complaints'),
    path('register/', views.register, name='register'),
    path('terms-of-service', views.terms_of_service, name="terms-of-service"),
    path("select-change/", views.select_change, name="select_change"),
    path('kitchen-dashboard/<str:filter>', views.kitchen_dashboard, name="kitchen-dashboard"),
    path('view-order/<str:sale_id>/<str:user_redirect>', views.view_order, name="view-order"),
    path('terms-of-service', views.terms_of_service, name="terms-of-service"),
    path('update_sale_status/<str:sale_id>/<str:current_status>', views.update_sale_status, name='update_sale_status'),
    path('waiter-orders', views.waiter_orders, name="waiter-orders"),
    path('cancel-order/<str:sale_id>', views.cancel_order, name='cancel-order'),
    path('update-delivery-status/<str:sale_id>', views.update_delivery_status, name="update-delivery-status"),
    path('customer-landing', views.customerLanding, name="customer-landing"),
    path('logout/',views.LogoutView, name="logout"),
    path('notify/', views.notify_waiter, name="notify"),
    path('view_bill/',views.view_bill,name="view_bill"),
    path('view-customer-order/<str:sale_id>',views.customer_view_order,name="view-customer-order"),
    path('customer-orders/',views.view_order_history,name="customer-orders"),
    path('manager/', views.manager, name="manager"),
    path('add-stock/manager/<int:item_id>/', views.add_stock, name="add_stock"),
    path('reduce-stock/manager/<int:item_id>/', views.reduce_stock, name="reduce_stock"),

]

os.environ['RUN_MAIN'] = "."