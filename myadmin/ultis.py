#Author:YHW
#Time:2018/7/21 15:25
from django.db.models import Q

def table_filter(request, admin_class):
    filter_conditions = {}
    keywords = ['page', 'o', '_q']
    print(request.GET)
    for k, v in request.GET.items():
        if k in keywords:
            continue
        if v:
            filter_conditions[k] = v
    print(admin_class.model.objects.filter(**filter_conditions))

    return admin_class.model.objects.filter(**filter_conditions), filter_conditions


def table_search(request,admin_class,object_list):
    search_key = request.GET.get("_q","")
    q_obj = Q()
    q_obj.connector = "OR"
    for column in admin_class.search_fields:
        q_obj.children.append(("%s__contains"%column, search_key))

    res = object_list.filter(q_obj)
    return res