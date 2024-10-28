from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feedback, Payment

# Create your forms here.

class RegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'This email address is already in use.')

        return cleaned_data
    # def save(self, commit=True):
    # 	user = super(RegForm, self).save(commit=False)
    # 	user.email = self.cleaned_data['email']
    # 	if commit:
    # 		user.save() 
    # 	return user



class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Feedback
        fields = "__all__"

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("amount","email","username","address","phone",)

    def save(self, commit=True):
        if not self.instance.image:  # Check if image field is empty
            self.instance.image = 'proof/succ.jpg'  # Set default image path
        return super().save(commit)
    
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()
        # self.fields['image'].widget.attrs['style'] = 'display:none'
        self.fields['amount'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        # self.fields['username'].widget.attrs['disabled'] = True
        
  