#Author:YHW
#Time:2018/7/21 14:05

from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    print(admin_class.model.objects.all())
    return admin_class.model.objects.all()



@register.simple_tag
def build_table_header_column(column):
    ele='''<th>%s</th>'''%(column)

    return mark_safe(ele)



@register.simple_tag
def build_table_row(request,obj,admin_class):
    row_ele = ""
    for index,column in enumerate(admin_class.list_display):
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:#choices type
            column_data = getattr(obj,"get_%s_display" % column)()
        else:
            column_data = getattr(obj,column)

        if type(column_data).__name__ == 'datetime':
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

        if index==0:
            column_data = "<a href='%s%s/change/'>%s</a>"%(request.path,obj.id,column_data)


        row_ele += "<td>%s</td>" % column_data

    return mark_safe(row_ele)


@register.simple_tag
def  build_paginators(query_sets):
    '''返回整个分页元素'''
    page_btns = ''

    added_dot_ele = False #
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages -2 \
                or abs(query_sets.number - page_num) <= 1:
            ele_class = ""
            if query_sets.number == page_num:
                added_dot_ele = False
                ele_class = "active"
            page_btns += '''<li class="%s"><a href="?page=%s">%s</a></li>''' % (
            ele_class, page_num, page_num)

        else:
            if added_dot_ele == False:
                page_btns += '<li><a>...</a></li>'
                added_dot_ele = True


    return mark_safe(page_btns)

@register.simple_tag
def render_filter_ele(condtion,admin_class,filter_condtions):
    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' %condtion
    field_obj = admin_class.model._meta.get_field(condtion)
    print(field_obj)
    if field_obj.choices:
        selected = ''

        for choice_item in field_obj.choices:
            print(choice_item)

            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected ="selected"
        #
            select_ele += '''<option value='%s'%s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected =''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            print(choice_item)

            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s'%s >%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''
    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def get_model_name(admin_class):

    return admin_class.model._meta.verbose_name




def recursive_related_objs_lookup(objs):

    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li> %s: %s </li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele += li_ele

        for m2m_field in obj._meta.local_many_to_many:
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj,m2m_field.name)
            for o in m2m_field_obj.select_related():
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele +=li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele


        for related_obj in obj._meta.related_objects:
            if 'ManyToManyRel' in related_obj.__repr__():

                if hasattr(obj, related_obj.get_accessor_name()):
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    print("-------ManyToManyRel",accessor_obj,related_obj.get_accessor_name())

                    if hasattr(accessor_obj, 'select_related'):
                        target_objs = accessor_obj.select_related()


                        sub_ul_ele ="<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> %s: %s </li>''' % (o._meta.verbose_name, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj,related_obj.get_accessor_name()):
                accessor_obj = getattr(obj,related_obj.get_accessor_name())

                if hasattr(accessor_obj,'select_related'):
                    target_objs = accessor_obj.select_related()

                else:
                    print("one to one i guess:",accessor_obj)
                    target_objs = accessor_obj

                if len(target_objs) >0:

                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele +="</ul>"
    return ul_ele

@register.simple_tag
def display_obj_related(objs):

    objs = [objs,]
    if objs:
        return mark_safe(recursive_related_objs_lookup(objs))





