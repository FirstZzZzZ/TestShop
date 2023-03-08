from dataclasses import field
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import forms as auth_forms
from .models import BankTransfer
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
from django.contrib.auth import password_validation


class SignUpForm(UserCreationForm):
    first_name=forms.CharField(max_length=100,required=True,label='ชื่อ')
    last_name=forms.CharField(max_length=100,required=True,label='นามสกุล')
    email=forms.EmailField(max_length=100,label='ที่อยู่อีเมล(E-mail)',)
    phone_number=forms.CharField(max_length=10,label='เบอร์โทร',)
    # password1=forms.Field(error_messages={'required': 'Please enter your name'})
    # password2=forms.Field(error_messages={'required': 'Please enter your name'})

    # is_staff=forms.CheckboxInput()

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta :
        model=User
        fields=('first_name','last_name','username','email','password1','password2',)
        

class UserEdit(UserChangeForm):
    # first_name=forms.CharField(max_length=100,required=True)
    # last_name=forms.CharField(max_length=100,required=True)
    # email=forms.EmailField(max_length=250,)  
    username=forms.CharField(max_length=100,required=True,label='ชื่อผู้ใช้')
    phone_number=forms.CharField(max_length=10,label='เบอร์โทร',)
    password = auth_forms.ReadOnlyPasswordHashField(label="รหัสผ่าน",
        help_text="คลิกที่ 'เปลี่ยนรหัส' เพื่อเปลี่ยนรหัสผ่าน")
    class Meta:
        model = User
        fields = ('first_name','last_name','username',)
    
class MyChangeFormPassword(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    pass

# class BankTransferForm(forms.Form):
#     moneytransferslip = forms.FileField(label='สลิปโอนเงิน')

class BankTransferForm(forms.ModelForm):
    class Meta:
        model = BankTransfer
        fields = ['name', 'address', 'city', 'postcode', 'email', 'money_transfer_slip']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = self.request.session.get('email')

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.username
        return initial

class PasswordChangeForm(BasePasswordChangeForm):
    error_messages = {
        'password_mismatch': "รหัสผ่านใหม่ไม่ตรงกัน โปรดตรวจสอบ",
    }
    
    new_password1 = forms.CharField(
        label="รหัสผ่านใหม่",
        widget=forms.PasswordInput,
        strip=False,
        
    )
    new_password2 = forms.CharField(
        label="ยืนยันรหัสผ่านใหม่",
        strip=False,
        widget=forms.PasswordInput,
    )
    
