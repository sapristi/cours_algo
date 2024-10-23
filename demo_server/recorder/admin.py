from django.contrib import admin
from recorder.models import Record

# Register your models here.


class RecordAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Record._meta.get_fields()]
    list_display = ["id", "method", "path"]
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Record, RecordAdmin)
from django.contrib import admin
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)
