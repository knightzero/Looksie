from django.forms import Form, CharField, PasswordInput, URLField

class UserLoginForm(Form):
    username = CharField(required=True) 
    password = CharField(widget=PasswordInput, required=True, min_length=4)
    
class UrlForm(Form):
    url = URLField(required=True)