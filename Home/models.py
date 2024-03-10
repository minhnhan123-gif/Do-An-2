from django.db import models
from django import forms
from django.contrib.auth.models import User
from dateutil import parser
from django.utils import timezone
from datetime import datetime
from django.db import IntegrityError


class ThongTinBenhNhan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_info', null=False)
    id = models.AutoField(primary_key=True)
    ho_ten = models.CharField(max_length=255, null=True, blank=True)
    so = models.CharField(max_length=15, null=True, blank=True)
    ngay_sinh = models.CharField(max_length=10, null=True, blank=True)
    gioi_tinh = models.CharField(max_length=10, null=True, blank=True)
    quoc_tich = models.CharField(max_length=50, null=True, blank=True)
    noi_sinh = models.CharField(max_length=255, null=True, blank=True)
    ngay_cap = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.ho_ten + '' + self.ngay_cap

    def save_info_from_qr(self, qr_content):
        info_list = qr_content.split('|')
        ngay_sinh = datetime.strptime(info_list[3], '%d%m%Y').date()
        ngay_cap = datetime.strptime(info_list[6], '%d%m%Y').date()


        ngay_sinh_formatted = ngay_sinh.strftime('%d-%m-%Y')
        ngay_cap_formatted = ngay_cap.strftime('%d-%m-%Y')
        try:
            # Thử lấy thông tin bệnh nhân có user_id là user_id của người dùng hiện tại
            patient_info = ThongTinBenhNhan.objects.get(user_id=self.user.id)
            
            # Nếu tìm thấy, cập nhật thông tin
            patient_info.ho_ten = info_list[2]
            patient_info.so = info_list[0]
            patient_info.ngay_sinh = ngay_sinh_formatted
            patient_info.gioi_tinh = info_list[4]
            patient_info.noi_sinh = info_list[5]
            patient_info.ngay_cap = ngay_cap_formatted
            patient_info.quoc_tich =  'Việt Nam'
            patient_info.save()
            return patient_info
        except ThongTinBenhNhan.DoesNotExist:
            # Nếu không tìm thấy, tạo mới và lưu thông tin
            self.ho_ten = info_list[1]
            self.so = info_list[0]
            self.ngay_sinh = ngay_sinh
            self.gioi_tinh = info_list[4]
            self.noi_sinh = info_list[5]
            self.ngay_cap = ngay_cap
            self.quoc_tich = 'Việt Nam'
            self.save()
            return self
        except IntegrityError:
            # Xử lý trường hợp lỗi IntegrityError (nếu có)
            return None
        
class ThongTinBenhNhanForm(forms.ModelForm):
    class Meta:
        model = ThongTinBenhNhan
        fields = '__all__'
        widgets = {
            'ngay_sinh': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
            'ngay_cap': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),

        }

    def __init__(self, *args, **kwargs):
        super(ThongTinBenhNhanForm, self).__init__(*args, **kwargs)
        # Thêm class 'datepicker' cho trường ngày_sinh
        self.fields['ngay_sinh'].widget.attrs.update({'class': 'datepicker'})
        self.fields['ngay_cap'].widget.attrs.update({'class': 'datepicker'})

class Doctor(models.Model):
    name = models.CharField(max_length=100)

class Service(models.Model):
    name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)

    def get_service_name_by_doctor_id(doctor_id):
        try:
            service = Service.objects.get(doctor_id=doctor_id)
            return service.name
        except Service.DoesNotExist:
            return None

class Queue(models.Model):
    id = models.AutoField(primary_key=True)
    queue_number = models.IntegerField(default=0)
    patient = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    registration_time = models.DateTimeField(default=timezone.now)
    is_examined = models.BooleanField(default=False)
    priority = models.BooleanField(default=False) 
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_year = models.CharField(max_length=10, null=True, blank=True)
    @classmethod
    def save_queue(cls, patient, service, doctor, queue_number, registration_time_str, gender, birth_year):
        # Phân tích chuỗi ngày giờ thành đối tượng datetime
        registration_time = parser.parse(registration_time_str)

        # Tạo và lưu đối tượng Queue vào CSDL
        queue = cls.objects.create(
            patient=patient,
            service=service,
            doctor=doctor,
            queue_number=queue_number,
            registration_time=registration_time,
            gender=gender,
            birth_year=birth_year
        )
        return queue
    
    @property
    def formatted_registration_time(self):
        return self.registration_time.strftime('%d-%m-%Y, %I:%M %p')
    
    def mark_as_examined(self):
        self.is_examined = True
        self.save()
    
