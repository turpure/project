from django import forms


class UserForm(forms.Form):
    user = forms.CharField(label='user', max_length=50)
    password1 = forms.CharField(label='password1', max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', max_length=30, widget=forms.PasswordInput)


class UserFormLogIN(forms.Form):
    user = forms.CharField(label='user', max_length=50)
    password = forms.CharField(label='password', max_length=30, widget=forms.PasswordInput)


class ShopForm(forms.Form):
    shopname = forms.CharField(label='shopname', max_length=50)
    feedbackscore = forms.CharField(label='feedbackscore')


