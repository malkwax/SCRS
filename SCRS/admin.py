from django.contrib import admin

# Register your models here.
from django.contrib import admin
from SCRS import models

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','qq','source','school','status','date')
    # list_filter = ('source','consultant','date')
    # search_fields = ('qq','name')
    # raw_id_fields = ('consult_course',)
    # filter_horizontal = ('tags',)
    # list_editable = ('status',)
    # readonly_fields = ("qq","name",)

admin.site.register(models.Exam)
admin.site.register(models.School)
admin.site.register(models.Student,StudentAdmin)
