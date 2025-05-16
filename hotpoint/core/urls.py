from django.urls import path
from . import views
from .views import instasend_callback
urlpatterns = [
    path('buy/', views.buy_voucher, name='buy'),
    path('redeem/', views.redeem_voucher, name='redeem'),
    path('success/', views.success_page, name='success'),
    path('generate-vouchers/', views.generate_vouchers, name='generate_vouchers'),
    # path('api/payment_callback/', views.payment_callback, name='payment_callback'),
    path('choose-plan/', views.choose_plan_view, name='choose_plan'),
    path('', views.choose_plan_view, name='choose_plan'),
    path('enter-phone/<int:amount>/', views.enter_phone_view, name='enter_phone'),
    path('pricing/', views.pricing_view, name='pricing'),
    # path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
    path('manage-devices/', views.manage_devices, name='manage_devices'),
    path('disconnect/<str:username>/', views.disconnect_device, name='disconnect_device'),
    path('set-bandwidth/<str:username>/<str:download_rate>/<str:upload_rate>/', views.set_bandwidth, name='set_bandwidth'),
    path('change-ip/<str:username>/<str:new_ip>/', views.change_ip, name='change_ip'),
    path('instasend/callback/', instasend_callback, name='instasend_callback'),



]
