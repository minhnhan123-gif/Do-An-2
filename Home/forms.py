from django import forms
import re
from django.contrib.auth.models import User
from .models import ThongTinBenhNhan
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
        ThongTinBenhNhan.objects.create(user = User)




class ThongTinBenhNhanForm(forms.ModelForm):
    required_css_class = 'required-field'
    error_css_class = 'error-field'
    ho_ten = forms.CharField(widget = forms.TextInput(attrs= {"class" : "form__control"}))
    so = forms.CharField(widget = forms.TextInput(attrs= {"class" : "form__control"}))
    ngay_sinh = forms.CharField(widget = forms.TextInput(attrs= {"class" : "form__control"}))
    gioi_tinh = forms.CharField(widget = forms.TextInput(attrs= {"class" : "form__control"}))
    quoc_tich = forms.CharField(widget = forms.TextInput(attrs= {"class" : "form__control"}))
    noi_sinh = forms.CharField(widget = forms.TextInput(attrs= {"class" : "form__control"}))
    ngay_cap = forms.CharField(widget = forms.TextInput(attrs= {"class" : "form__control"}))
    class Meta:
        model = ThongTinBenhNhan  # Sử dụng model ThongTinBenhNhan
        fields = '__all__'  # Sử dụng tất cả các trường từ model
        exclude = ['user']

        


