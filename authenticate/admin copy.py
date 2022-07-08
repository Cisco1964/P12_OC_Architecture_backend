from django.contrib import admin
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    
    model = User
    add_form = CustomUserCreationForm

    # fieldsets = (('Rattachement',
    #                     {
    #                         'fields': (
    #                         'role',
    #                         )
    #                     }
    #                 ),)

#     staff_readonly_fields = ('role')

#     def get_readonly_fields(self, request, obj=None):
#         user = User.objects.get(username=obj)
#         if user.is_superuser is True:
#             return self.staff_readonly_fields
#         return super(CustomUserAdmin, self).get_readonly_fields(request, obj)


        # def get_form(self, request, obj=None, **kwargs):
        # user = User.objects.get(username=obj)
        # print("user.is_superuser", user.is_superuser)
        # if user.is_superuser is False:
        #     fieldsets = (
        #         *UserAdmin.fieldsets,
        #         (
        #              'Rattachement',
        #             {
        #                 'fields': (
        #                 'role',
        #                 )
        #             }
        #         )
        #     )
        #return super(CustomUserAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(User, CustomUserAdmin)
#admin.site.register(User, UserAdmin)
