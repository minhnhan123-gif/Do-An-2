from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ThongTinBenhNhan, Doctor, Service, Queue
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegistrationForm, ThongTinBenhNhanForm, LoginForm
from django.db import models
from django.db.models import Max, F, Case, When, Value, ExpressionWrapper, fields, IntegerField
from pyzbar.pyzbar import decode
from PIL import Image
import pytesseract
from datetime import date, datetime
from .serializers import ThongTinBenhNhanSerializer, DoctorSerializer, ServiceSerializer, QueueSerializer
from rest_framework import generics, mixins
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer
from itertools import chain
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify, current_app
from flask_wtf.csrf import CSRFProtect
from django.middleware.csrf import get_token
import jwt
import qrcode
import json


def login_page(request):
  return render(request,'login_page.html')

def form(request):  
  return render(request,'form_page.html')

def queue_service(request, service):
    print(f'Selected service: {service}')  # In ra giá trị dịch vụ để kiểm tra
    queue_data = Queue.objects.filter(service=service, is_examined=False).annotate(
        priority_value=Case(
            When(priority=True, then=Value(0)),
            default=Value(1),
            output_field=fields.IntegerField(),
        ),

    ).order_by('priority_value', 'registration_time')

    print(f'Queue data: {queue_data}')  # In ra dữ liệu hàng đợi để kiểm tra

    return render(request, 'queue_page.html', {'service': service, 'queue_data': queue_data})

def admin(request):
  return render(request,'admin_page.html')

def user_login(request):
  form = LoginForm()
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']

      #xac nhan user dang nhap
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect('patient_info')
      else:
        return render(request, 'login_page.html', {'error_message': 'Tên đăng nhập hoặc mật khẩu không đúng.'})
      
  return render(request, 'login_page.html', {'form': form})

def register(request):  
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            User.objects.create_user(username=username, password=password1, email=email)
        return redirect('/')
    else:
       form = RegistrationForm()
    return render(request, 'Register.html', {'form': form}) 
    
def hien_thi_va_sua_thong_tin(request):
    user_id = 1
    user = get_object_or_404(User, id=user_id)
    benh_nhan, created = ThongTinBenhNhan.objects.get_or_create(user=user)
  
    if request.method == 'POST':
        form = ThongTinBenhNhanForm(request.POST, instance=benh_nhan)
        if form.is_valid():
            benh_nhan = form.save(commit=False)
            benh_nhan.user = user
            benh_nhan.save()
            return redirect('home')
    else:
        form = ThongTinBenhNhanForm(instance=benh_nhan)

    return render(request, 'form_page.html', {'form': form, 'benh_nhan': benh_nhan})

def activate_user(request, username):
    user = get_object_or_404(User, username=username)
    user.is_active = True

    user.save()

    return redirect('home')

def create_benh_nhan(request):
    if request.method == 'POST':
        form = ThongTinBenhNhanForm(request.POST)
        if form.is_valid():
            benh_nhan = form.save()
            return redirect('success_page') 
    else:
        form = ThongTinBenhNhanForm()

    return render(request, 'create_benh_nhan.html', {'form': form})

def get_doctor_and_queue_number(request):
    if request.method == 'GET':
        service_name = request.GET.get('service_name', '')
        patient_name = request.GET.get('patient_name', '') 
        # Lấy tên bác sĩ
        service, created = Service.objects.get_or_create(name=service_name)

        # Kiểm tra xem bác sĩ đã được gán cho dịch vụ chưa
        if service.doctor:
            doctor_name = service.doctor.name
        else:
            doctor_name = "No Doctor Assigned"

        # Lấy số thứ tự gần nhất
        max_queue_number = Queue.objects.filter(service=service_name).aggregate(Max('queue_number'))['queue_number__max']
        # Tăng số thứ tự
        if max_queue_number:
            queue_number = max_queue_number + 1 if max_queue_number is not None else 1
        else:
            queue_number = 1
        return JsonResponse({'doctor_name': doctor_name, 'queue_number': queue_number})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
def save_queue(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name', '')
        patient_name = request.POST.get('patient_name', '')
        doctor_name = request.POST.get('doctor_name', '')
        queue_number = request.POST.get('queue_number', '')
        registration_time = request.POST.get('registration_time', '')
        gender = request.POST.get('gender', '')
        birth_year = request.POST.get('birth_year', '')
        # Tìm hoặc tạo bác sĩ
        # doctor, created = Doctor.objects.get_or_create(name=doctor_name)

        # Tạo một đối tượng Queue và lưu vào CSDL
        try:
            queue = Queue.save_queue(patient_name, service_name, doctor_name, queue_number, registration_time, gender, birth_year)
            return JsonResponse({'success': True, 'queue_number': queue.queue_number})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    else:
        return JsonResponse({'error': 'Invalid request method'})   

def empty(request):
    temp_storage_data = {
        'ho_ten': '',
        'so': '',
        'ngay_sinh': '',
        'gioi_tinh': '',
        'quoc_tich': '',
        'noi_sinh': '',
        'ngay_cap': ''
    }
    request.session['temp_storage'] = temp_storage_data
    print('Thong tin trong storage: ', temp_storage_data)
    return redirect('form')


def decode_qr_content(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            qr_content = data['content']

            info_list = qr_content.split('|')
            ngay_sinh = datetime.strptime(info_list[3], '%d%m%Y').date()
            ngay_cap = datetime.strptime(info_list[6], '%d%m%Y').date()

            ngay_sinh_formatted = ngay_sinh.strftime('%d-%m-%Y')
            ngay_cap_formatted = ngay_cap.strftime('%d-%m-%Y')

            # Lưu thông tin vào session
            temp_storage_data = {
                'ho_ten': info_list[2],
                'so': info_list[0],
                'ngay_sinh': ngay_sinh_formatted,
                'gioi_tinh': info_list[4],
                'quoc_tich': 'Việt Nam',
                'noi_sinh': info_list[5],
                'ngay_cap': ngay_cap_formatted
            }
            request.session['temp_storage'] = temp_storage_data
            print('Thong tin', temp_storage_data)
            return render(request, 'form_page.html', {'temp_storage': temp_storage_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def get_home(request):
    # Lấy dữ liệu từ session
    temp_storage_data = request.session.get('temp_storage', {})

    # In giá trị dữ liệu vào terminal hoặc log
    print('Dữ liệu từ session:', temp_storage_data)

    # Hiển thị trang other_page.html với dữ liệu
    return render(request, 'home_page_3.html', {'temp_storage': temp_storage_data})

def save_info_mobile(request):
     if request.method == 'POST':
        data = request.POST  # Hoặc sử dụng request.data nếu bạn đang gửi dữ liệu JSON
        serializer = ThongTinBenhNhanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'message': 'Thông tin bệnh nhân đã được lưu.'})
        else:
            return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)
     else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def calculate_age_and_priority(birthdate):
    today = date.today()
    age = today.year - birthdate
    is_over_80 = age >= 80
    return age, is_over_80

def benh_nhan_bac_si(request):

    # Lấy thông tin từ Queue và sử dụng select_related để giảm số lượng truy vấn SQL
    queue = Queue.objects.all()

    return render(request, 'admin_page.html', {'queue': queue})

def xac_nhan (request, queue_id):
  queue = get_object_or_404(Queue, id=queue_id)
  queue.is_examined = True
  queue.save()
  return redirect('danh_sach_benh_nhan')
   
def uu_tien(request, queue_id):
   queue = get_object_or_404(Queue, id=queue_id)
   queue.priority = True
   queue.save()
   return redirect('danh_sach_benh_nhan')

def getcrsfToken(request):
   csrf_token = get_token(request)
   return JsonResponse({'csrfToken': csrf_token})

def get_doctor_name_by_service_name(request):
   service_name = request.GET.get('service_name', '')

   try:
      service = Service.objects.get(name = service_name)
      doctor_name = service.doctor.name if service.doctor else None
      return JsonResponse({'doctor_name': doctor_name})
   except Service.DoesNotExist:
      return JsonResponse({'error': 'Dich vu khong ton tai'}, status=404)
   except Exception as e:
      return JsonResponse({'error':str(e)}, status=500)

# KET NOI VOI APP

class ThongTinBenhNhanList(generics.ListCreateAPIView):
    queryset = ThongTinBenhNhan.objects.all()
    serializer_class = ThongTinBenhNhanSerializer
    lookup_field = 'user_id'  # hoặc 'id' tùy thuộc vào trường primary key của model

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def create_or_update(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id:
            try:
                instance = self.get_queryset().get(user_id=user_id)
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            except ThongTinBenhNhan.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"Lỗi": "Không tìm thấy user_id"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.create_or_update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        response = self.create_or_update(request, *args, **kwargs)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return self.post(request, *args, **kwargs)
        return response
        

class ThongTinBenhNhanDetail(generics.ListCreateAPIView):
    queryset = ThongTinBenhNhan.objects.all()
    serializer_class = ThongTinBenhNhanSerializer  # hoặc 'id' tùy thuộc vào trường primary key của model

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class DoctorList (generics.ListAPIView):
  queryset = Doctor.objects.all()
  serializer_class = DoctorSerializer

class ServiceList(generics.ListAPIView):
   queryset = Service.objects.all()
   serializer_class = ServiceSerializer

class QueueList(generics.ListAPIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

    def get_max_queue_number(self, selected_service):
        print("Selected Service:", selected_service)
        max_queue_number = Queue.objects.filter(service=selected_service).aggregate(Max('queue_number')).get('queue_number__max')
        print("Max Queue Number:", max_queue_number)
        return max_queue_number or 0

    def list(self, request, *args, **kwargs):
        selected_service = request.query_params.get('service_name')

        if not selected_service:
            return Response({"error": "Missing 'serviceName' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        max_queue_number = self.get_max_queue_number(selected_service)
        return Response({"max_queue_number": max_queue_number})

class QueueList2(generics.ListAPIView):
    serializer_class = QueueSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['service']

    def get_queryset(self):
        service= self.request.query_params.get('service', None)
        if service is not None:
            # Nếu có tham số truy vấn 'service_name', lọc theo nó
            return Queue.objects.filter(service__icontains=service)
        else:
            # Nếu không có tham số truy vấn, trả về toàn bộ danh sách
            return Queue.objects.all()

class CreateQueue(generics.CreateAPIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        data['queue_number'] = int(data.get('queue_number', 0))

        serializer = self.get_serializer(data=data)
        print("Data received:", data)
        print("Formatted time:", data.get('registration_time', ''))
        print("Patient Name:",  data.get('patient', ''))
        print("Doctor Name:",  data.get('doctor', ''))
        print("Queue Number:",  data.get('queue_number', ''))
        print("Service Name:",  data.get('service', ''))
        if serializer.is_valid():
            # Tiếp tục xử lý nếu dữ liệu hợp lệ
            patient = data.get('patient', '')
            service = data.get('service', '')
            doctor = data.get('doctor', '')
            queue_number = data.get('queue_number', '')
            registration_time = data.get('registration_time', '')
            gender = data.get('gender', '')
            birth_year = data.get('birth_year', '')
            instance = serializer.save(patient=patient, service=service, doctor=doctor, queue_number=queue_number, registration_time=registration_time, gender=gender, birth_year=birth_year)

            response_data = {
                'message': 'Queue created successfully',
                'data': serializer.data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # Xử lý lỗi nếu dữ liệu không hợp lệ
            print("Validation errors:", serializer.error)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DANG KY USER CHO APP

class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # Chỉnh sửa: raise_exception thay vì raise_exceoption
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
class LoginAPIView(APIView):
  def post(self, request, *args, **kwargs):
     username = request.data.get('username')
     password = request.data.get('password')
     user = authenticate(username=username, password=password)
     user_id = request.data.get('id')

     if user:
        token, created = Token.objects.get_or_create(user = user)
        user_id = user.id

        return Response({'token': token.key, 'user_id': user_id}, status=status.HTTP_200_OK)
     else:
        return Response({'error': 'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)
     

     


