from django.contrib import admin
from account.models import User, Profile, Bookmarks
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name', 'birthday', 'tc', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name', 'tc', 'birthday')}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'birthday', 'tc', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
# admin.site.register(Profile)
# admin.site.register(Bookmarks)



@admin.register(Bookmarks)
class BookmarksAdmin(admin.ModelAdmin):
    list_display = ['id','bookmarks', 'profile']
    ordering = ['id']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'image', 'created_at']
    ordering = ['id']