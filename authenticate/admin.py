from django.contrib import admin
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Rattachement',
            {
                'fields': (
                    'role',
                )
            }
        )
    )

    staff_readonly_fields = ('role')

    def get_readonly_fields(self, request, obj=None):
        try:
            user = User.objects.get(username=obj)
            if user.is_superuser is True:
                return self.staff_readonly_fields
            else:
                return []
        except User.DoesNotExist:
                return []


admin.site.register(User, CustomUserAdmin)
