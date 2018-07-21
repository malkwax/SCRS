#Author:YHW
#Time:2018/7/21 13:31
from SCRS import models
enabled_admins = {}

class BaseAdmin(object):
    list_display = []
    list_per_page = 20
    list_filters = []
    search_fields=[]


class StudentAdmin(BaseAdmin):
    list_display = ('id','name','qq','source','school','status','date')
    list_per_page = 3
    list_filters = ['source','school', 'status']
    search_fields = ['qq', 'name', "source"]




def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}
    admin_class.model = model_class
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class










register(models.Student,StudentAdmin)



