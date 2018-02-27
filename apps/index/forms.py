from django import forms
from apps.user_auth.models import User


class SettingsForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username',
				  'first_name',
				  'last_name',
				  'email',
				  'birth_date',
				  'locality',
				  'phone',
                  'avatar')

