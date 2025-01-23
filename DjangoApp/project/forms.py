from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit, Fieldset
from django.utils.safestring import mark_safe
from .models import addModle
from django.core.validators import FileExtensionValidator 
from django.core.exceptions import ValidationError
from PIL import Image

'''
Create the complaint form using Django forms. django-crispy-forms has 
been used to render the form automatically with the necessary labels, 
placeholders and validation information. The layout of the form has also 
been specified.
'''
class complaintform(forms.Form):
    firstname = forms.CharField(
        label='First Name',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    lastname = forms.CharField(
        label='Last Name',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        required=True,
    )
    phonenumber = forms.CharField(
        label='Phone Number',
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    message = forms.CharField(
        label='Complaint Information',
        max_length=500,
        widget=forms.Textarea(attrs={'placeholder': 'Complaint Details...'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Customer Information:',
                Div(
                    Div('firstname', css_class='form-group col-md-6'),
                    Div('lastname', css_class='form-group col-md-6'),
                    css_class='row',
                ),
                'email',
                'phonenumber'
            ),
            Fieldset(
                'Complaint Details:',
                'message',
            ),
        )
        self.helper.add_input(
            Submit('submit', 'Submit Complaint', css_class='btn btn-submit'))

class paymentForm(forms.Form):

    card_number = forms.CharField(
        label='Card Number',
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9123 4567'}),
    )
    name_on_card = forms.CharField(
        label='Name on card',
        max_length=45,
        widget=forms.TextInput(attrs={'placeholder': 'Mr John Doe'}),
        required=True,
    )
    expiration_date = forms.DateField(
        input_formats=['%Y-%M-%D'],
        widget=forms.TextInput(attrs={'type': 'date'}),
        required=True,
    )
    cvv_code = forms.CharField(
        label='CVV',
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={'placeholder': '123'}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(
            Submit('submit', 'Pay now', css_class='btn btn-submit')
        )

class addform(forms.ModelForm):
    class Meta():
        model = addModle
        fields = ['name', 'description', 'price', 'allergies', 'type', 'photo', 'calories']

    TYPES = [['starter', 'Starter'], ['main', 'Main'], ['desert', 'Desert'], ['drink', 'Drink'] ]
    
    name = forms.CharField(
        label='Dish Name',
        widget=forms.TextInput(attrs={'placeholder': 'Dish Name'}),
        required=True
    )

    description = forms.CharField(
        label='Dish Description',
        max_length=300,
        widget=forms.Textarea(attrs={'placeholder': 'Dish Description'}),
        required=True
    )

    price = forms.FloatField(
        label = 'Dish Price £',
        widget=forms.TextInput(attrs={'placeholder' : '00.00'}),
        required=True
    )

    allergies = forms.CharField(
        label='Allergies',
        widget=forms.Textarea(attrs={'placeholder': 'Allergies'}),
        required=True
    )

    type = forms.CharField(
        label = 'Type of dish',
        widget = forms.Select(choices=TYPES),
        required=True
    )
    
    photo = forms.ImageField(
        label = 'Photo',
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required= True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    
    calories = forms.IntegerField(
        label = 'Calories',
        widget = forms.TextInput(attrs={'placeholder' : '00'}),
        required=True
    )

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            image = Image.open(photo)
            width, height = image.size
            aspect_ratio = width / height
            if aspect_ratio < 1.0 / 1.1 or aspect_ratio > 16.0 / 9.0 * 1.1:
                raise ValidationError('Image aspect ratio must be between 1:1 and 16:9.')
            photo.seek(0)
        return photo
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-submit'))
        self.helper.encoding = 'multipart/form-data'

class changeform(forms.Form):

    name = forms.CharField(
        label='Dish Name',
        widget=forms.TextInput(),
        required=False
    )

    description = forms.CharField(
        label='Dish Description',
        max_length=300,
        widget=forms.Textarea(),
        required=False
        )

    price = forms.FloatField(
        label = 'Dish Price £',
        widget=forms.TextInput(),
        required=False    )

    allergies = forms.CharField(
        label='Allergies',
        widget=forms.Textarea(),
        required=False
    )

    calories = forms.IntegerField(
        label = 'Calories',
        widget = forms.TextInput(),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-submit'))

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        min_length=3,
        required=True,
    )
    password = forms.CharField(
        max_length=50,
        min_length=3,
        required=True,
        widget=forms.PasswordInput(),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('username', css_class='form-group col-10'),
                Div('password', css_class='form-group col-10'),
                css_class='form-row'
            ),
        )
        self.helper.add_input(
            Submit('submit', 'Login', css_class='btn SUBMIT')
        )

class customer_register(forms.Form):

    first_name = forms.CharField(
        label='First Name',
        max_length=45,
        widget=forms.TextInput(attrs={'placeholder': 'Your First Name'}),
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=45,
        widget=forms.TextInput(attrs={'placeholder': 'Your Last Name'}),
    )
    customer_phone = forms.CharField(
        label='Your Phone Number',
        max_length=11,
        widget=forms.TextInput(attrs={'placeholder': '07123456789'}),
        required=True,
    )
    customer_phone = forms.CharField(
        label='Username',
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        required=True,
    )
    customer_password = forms.CharField(
        label='Password',
        max_length=30,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=True,
    )
    password_repeat = forms.CharField(
        label='Repeat Password',
        max_length=30,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Repeat Your Password'}),
        required=True,
    )

    terms_and_conditions = forms.BooleanField(
        label=mark_safe('By signing up your agree to our <a href="/project/terms-of-service">terms of service</a>'),
        error_messages={"required": "You must accept our terms of service"},
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(
            Submit('submit', 'Join now', css_class='btn btn-submit')
        )

class select_change_form(forms.Form):
    
    change = forms.ChoiceField(
        label = 'Dish to be changed',
        required = True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('next', 'Next', css_class='btn btn-submit'))
        self.helper.add_input(Submit('delete', 'Delete', css_class='btn btn-warning'))
        self.helper.add_input(Submit('add', 'Add new', css_class='btn btn-submit' ))
