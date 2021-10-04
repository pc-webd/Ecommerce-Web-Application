from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email=forms.CharField(required=True,help_text="Enter an valid email")
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password= self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError("Your password should be at least 8 Characters")
        return password

class CheckoutForm(forms.Form):
    shipping_customername=forms.CharField(required=False)
    shipping_address1 = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_landmark=forms.CharField(required=False)
    shipping_city=forms.CharField(required=False)
    shipping_state= forms.CharField(required=False)
    shipping_zip = forms.CharField(required=False)
    shipping_phone = forms.CharField(required=False)

    billing_customername = forms.CharField(required=False)
    billing_address1 = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_landmark = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)
    billing_state = forms.CharField(required=False)
    billing_zip = forms.CharField(required=False)
    billing_phone = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class ContactForm(forms.Form):
    name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    phone=forms.IntegerField()
    subject=forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))