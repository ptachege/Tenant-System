from django.db.models.query_utils import PathInfo
from django.urls import path
from . import views
app_name = 'Tenants'

urlpatterns = [

    path('', views.index, name='index'),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path('register_caretaker/', views.register_caretaker, name='register_caretaker'),
    path("caretaker_list/", views.caretaker_list, name="caretaker_list"),
    path("delete_caretaker/<int:pk>/", views.delete_caretaker, name="delete_caretaker"),

    path('load_houses', views.load_houses, name='load_houses'),
    path('payment_houses', views.payment_houses, name='payment_houses'),
    path('invoice_list/<int:pk>/', views.invoice_list, name='invoice_list'),
    # current pattern start here
    path('register_apartments/', views.register_apartments,
         name='register_apartments'),
    path('apartment_list/', views.apartment_list, name='apartment_list'),
    path('register_tenant/', views.register_tenant, name='register_tenant'),
    path('tenants_list/', views.tenants_list, name='tenants_list'),
    path('apartment_detail/<int:pk>/',
         views.apartment_detail, name='apartment_detail'),
    path('tenant_details/<int:pk>/',
         views.tenant_details, name='tenant_details'),
    path('register_lease/', views.register_lease, name='register_lease'),
    path('rent_payment/', views.rent_payment, name='rent_payment'),
    path('leases_list/', views.leases_list, name='leases_list'),
    path('terminate_lease/<int:pk>/', views.terminate_lease, name='terminate_lease'),
    path('house_list/', views.all_houses, name='all_houses'),
    path('house_details/<int:pk>/',
         views.house_details, name='house_details'),
    path('invoice_template/<int:my_lease_pk>/<int:pk>/', views.invoice_template, name='invoice_template'),
    path('generate_invoices/', views.generate_invoices, name='generate_invoices'),
    path('pay_invoice/<int:pk>/', views.pay_invoice, name='pay_invoice'),
    path('active_leases/', views.active_lease, name='active_leases'),

    # api url patterns
    path('apartment_list_view/', views.apartment_list_view,
         name='apartment_list_view'),
]
