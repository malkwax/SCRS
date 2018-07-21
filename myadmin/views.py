from django.shortcuts import render,redirect
from myadmin import myadmin

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from myadmin.ultis import table_filter,table_search
from myadmin.forms import create_model_form

# Create your views here.


def index(request):
    return render(request, "myadmin/table_index.html", {'table_list': myadmin.enabled_admins})


def display_table_objs(request,app_name,table_name):
    admin_class = myadmin.enabled_admins[app_name][table_name]

    object_list, filter_condtions = table_filter(request, admin_class)

    object_list = table_search(request, admin_class, object_list)

    # paginator = Paginator(admin_class.model.objects.all(),admin_class.list_per_page)
    paginator = Paginator(object_list, admin_class.list_per_page)

    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)

    return render(request, "myadmin/table_objs.html", {"admin_class":admin_class,
                                                       "query_sets":query_sets,
                                                       "filter_condtions":filter_condtions

                                                          })
def table_obj_change(request,app_name,table_name,obj_id):

    admin_class = myadmin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    #
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "POST":
        form_obj = model_form_class(request.POST,instance=obj) #更新
        if form_obj.is_valid():
            form_obj.save()
    else:

        form_obj = model_form_class(instance=obj)



    return render(request,"myadmin/table_obj_change.html",{'form_obj':form_obj,
                                                              'admin_class':admin_class,
                                                              'app_name':app_name,
                                                              'table_name':table_name})



def table_obj_add(request,app_name,table_name):
    admin_class = myadmin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    if request.method == "POST":
        form_obj = model_form_class(request.POST)  #
        if form_obj.is_valid():
            form_obj.save()
            return  redirect(request.path.replace("/add/","/"))
    else:
        form_obj = model_form_class()

    return render(request, "myadmin/table_obj_add.html", {"form_obj": form_obj,
                                                          'admin_class': admin_class,
                                                          'app_name': app_name,
                                                          'table_name': table_name,

                                                             })
def table_obj_delete(request,app_name,table_name,obj_id):
    admin_class = myadmin.enabled_admins[app_name][table_name]

    obj = admin_class.model.objects.get(id=obj_id)
    print(obj)
    if request.method == "POST":
        obj.delete()
        return redirect("/myadmin/%s/%s/" %(app_name,table_name))

    return render(request,"myadmin/table_obj_delete.html",{"obj":obj,
                                                              "admin_class":admin_class,
                                                              "app_name": app_name,
                                                              "table_name": table_name,
                                                              })