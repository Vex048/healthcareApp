from django.contrib.auth.forms import SetPasswordForm

class MySetPasswordForm(SetPasswordForm):
    def save(self, commit=True):
        # Add debugging
        print(f"Setting new password for user: {self.user.username}")
        user = super().save(commit=False)
        password = self.cleaned_data["new_password1"]
        print(f"New password length: {len(password)}")
        
        if commit:
            user.save()
        return user