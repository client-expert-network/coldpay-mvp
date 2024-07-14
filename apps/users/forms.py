from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "password",
                "class": "form-control",
                "name": "password",
                "placeholder": "••••••••••••",
                "aria-describedby": "password",
            }
        )
    )

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "email",
                    "name": "email",
                    "placeholder": "이메일",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "username",
                    "name": "username",
                    "placeholder": "닉네임",
                    "autofocus": True,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "last_name",
                    "name": "last_name",
                    "placeholder": "성",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "first_name",
                    "name": "first_name",
                    "placeholder": "이름",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):

    email = forms.EmailField(
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "id": "email",
                "name": "email-username",
                "placeholder": "이메일",
                "autofocus": True,
            },
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "password",
                "class": "form-control",
                "name": "password",
                "placeholder": "••••••••••••",
                "aria-describedby": "password",
            }
        )
    )
