from django import forms
from django.contrib.auth import get_user_model, password_validation

UserModel = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password',max_length=20)


class SignUpForm(forms.ModelForm):
    username = forms.CharField(label="Username", required=True, min_length=8, max_length=20)
    email = forms.EmailField(label='Email',required=True)
    password1 = forms.CharField(label="Password", required=True, strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", required=True, strip=False, widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields =  ('username','email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user