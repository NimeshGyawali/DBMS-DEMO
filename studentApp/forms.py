from django import forms

class StudentForm(forms.Form):
    roll_no = forms.IntegerField(label='Roll No')
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(max_length=100, label='Email')
    phone_no = forms.CharField(max_length=15, label='Phone No')
