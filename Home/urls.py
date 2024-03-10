from django.urls import path
from Home.views import *
from . import views

urlpatterns = [
    path('home_page/', views.get_home, name='home'),
    # path('', login),
    path('', form, name = 'form'),
    path('queue/service/<str:service>/', views.queue_service, name='queue_service'),
    # path('', views.hien_thi_va_sua_thong_tin, name = 'patient_info'),
    # path('', views.user_login,),
    path('', views.user_login, name='logout'),
    path('Sign_in/', views.register, name='sign_in'),
    path('get_doctor_and_queue_number/', get_doctor_and_queue_number, name='get_doctor_and_queue_number'),
    path('save_queue/', save_queue, name='save_queue'),
    path('doctor_page/', benh_nhan_bac_si, name='danh_sach_benh_nhan'),
    path('register/', UserRegisterAPIView.as_view(), name = 'user-registration'),
    path('update_confirmation/<int:queue_id>/', xac_nhan, name='update_confirmation'),
    path('decode_qr/', decode_qr_content, name='decode_qr_content'),
    path('update_priority/<int:queue_id>/', uu_tien, name='update_priority'),
    path('login/', LoginAPIView.as_view() ,name = 'user-login'),
    path('api/thong-tin-benh-nhan/list/<int:user_id>/', ThongTinBenhNhanList.as_view(), name='thongtinbenhnhan-list'),
    path('api/thong-tin-benh-nhan/list', ThongTinBenhNhanDetail.as_view(), name='thongtinbenhnhan-detail'),
    path('api/thong-tin-bac-si/list/', DoctorList.as_view(), name='thongtinbacsi'),
    path('api/thong-tin-dich-vu/list/', ServiceList.as_view(), name='thongtindichvu'),
    path('api/thong-tin-hang-cho/list/', QueueList.as_view(), name='thongtinhangcho'),
    path('api/thong-tin-hang-cho/list2/', QueueList2.as_view(), name='thongtinhangcho'),
    path('api/thong-tin-hang-cho/create/', CreateQueue.as_view(), name='taohangcho'),
    path('get_csrf_token/', getcrsfToken, name = 'get_csrf_token'),
    path('get-doctor-name/', get_doctor_name_by_service_name, name='get_doctor_name_by_service_name'),
    path('emptyData/', empty, name ="emptyData")
]
