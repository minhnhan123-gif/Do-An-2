from django.contrib import admin
from .models import ThongTinBenhNhan,  Doctor, Service, Queue
from django.utils.safestring import mark_safe
from django.urls import reverse, path
from django.http import JsonResponse
from .models import User

class ServiceFilter(admin.SimpleListFilter):
    title = 'Dịch vụ'
    parameter_name = 'service'

    def lookups(self, request, model_admin):
        return [(service, service) for service in Queue.objects.values_list('service', flat=True).distinct()]

    def queryset(self, request, queryset):
        value = self.value()
        if value: 
            return queryset.filter(service = value)
        return queryset

class ThongTinBenhNhanAdmin(admin.ModelAdmin):
    list_display = ('ho_ten', 'so', 'ngay_sinh', 'gioi_tinh', 'quoc_tich', 'noi_sinh', 'ngay_cap')
    actions = ['thong_ke_benh_nhan']

    def thong_ke_benh_nhan(self, request, queryset):
        # Thống kê số lượng bệnh nhân
        count = queryset.count()
        self.message_user(request, f'Tổng số bệnh nhân: {count}')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'edit_link', 'delete_link')

    def edit_link(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label,  obj._meta.model_name),  args=[obj.id])
        return mark_safe(f'<a href="{change_url}">Edit</a>')
    edit_link.short_description = 'Edit'

    def delete_link(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label,  obj._meta.model_name),  args=[obj.id])
        return mark_safe(f'<a href="{delete_url}">Delete</a>')
    delete_link.short_description = 'Delete'

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'doctor_id', 'edit_link', 'delete_link')

    def edit_link(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return mark_safe(f'<a href="{change_url}">Edit</a>')
    edit_link.short_description = 'Edit'

    def delete_link(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return mark_safe(f'<a href="{delete_url}">Delete</a>')
    delete_link.short_description = 'Delete'

class QueueAdmin(admin.ModelAdmin):
    list_display = ('id','patient', 'service', 'doctor', 'registration_time', 'is_examined', 'priority')       
    list_filter = (ServiceFilter,)
    actions = ['Tong_so_benh_nhan_dang_ky']
    list_editable = ('is_examined','priority') 

    def Tong_so_benh_nhan_dang_ky(self, request, queryset):
        count = queryset.count()
        self.message_user(request, f'Tổng số người đã đăng ký: {count}')

    Tong_so_benh_nhan_dang_ky.short_description = "Tổng số bệnh nhân đã đăng ký"

    def get_search_result(self, request, queyset, search_term):
        queryset, use_distinct = super().get_search_results(request, queyset, search_term)
        queryset = queryset.filter(Service = request.GET.get('service'))
        return queryset, use_distinct
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_priority/', self.update_priority, name = 'update_priority'),
        ]
        return my_urls + urls
    
    def update_priority(self, request):
        if request.method == 'POST':
            patient_id = request.PORT.get('patient_id')
            priority_value = request.PORT.GET('priority_value')

            try:
                patient = Queue.objects.get(id = patient_id)
                patient.priority = priority_value
                patient.save()
                return JsonResponse ({'status':'success'})
            except Exception as e:
                return JsonResponse ({'status': 'error','message': str(e)})
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

class UserAdmin (admin.ModelAdmin):
    list_display = ['username','email']
    search_diplay = ['username','email']

    def save_model (self,request,obj,form,change):
        if not change:

            pass
        super().save_model(request, obj, form, change)



# Đăng ký model và lớp admin tương ứng
admin.site.register(ThongTinBenhNhan, ThongTinBenhNhanAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Queue,QueueAdmin)