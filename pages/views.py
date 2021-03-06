from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate, logout
import json
from microsite.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from pages.models import *
from django.views.decorators.csrf import csrf_exempt
from pages.forms import *
from django.db.models.aggregates import Max


@login_required
def pages(request):
    pagelist=Page.objects.all()
    return render_to_response('admin/content/page/page-list.html',{'pages': pagelist})


@login_required
def new_page(request):
    if request.method=='POST':
        validate_page = PageForm(request.POST)
        if validate_page.is_valid():
            validate_page.save()
            data={"error":False,'response':'Page created successfully'}
        else:
            data={"error":True,'response':validate_page.errors}
        return HttpResponse(json.dumps(data))

    c = {}
    c.update(csrf(request))
    return render_to_response('admin/content/page/new-page.html',{'csrf_token':c['csrf_token']})


@login_required
def delete_page(request, pk):
    Page.objects.get(pk = pk).delete()
    return HttpResponseRedirect('/portal/content/page/')


@login_required
def edit_page(request, pk):
    if request.method=='POST':
        page_instance = Page.objects.get(pk=pk)
        validate_page = PageForm(request.POST, instance=page_instance)
        if validate_page.is_valid():
            validate_page.save()
            data={"error":False,'response':'Page updated successfully'}
        else:
            data={"error":True,'response':validate_page.errors}
        return HttpResponse(json.dumps(data))

    c = {}
    c.update(csrf(request))
    current_page = Page.objects.get(pk=pk)
    return render_to_response('admin/content/page/edit-page.html',{'page':current_page,'csrf_token':c['csrf_token']})


@login_required
def delete_menu(request, pk):
    Menu.objects.get(pk = pk).delete()
    return HttpResponseRedirect('/portal/content/menu/')


@login_required
def change_menu_status(request, pk):
    menu=Menu.objects.get(pk = pk)
    if menu.status=="on":
        menu.status="off"
    else:
        menu.status="on"
    menu.save()
    return HttpResponseRedirect('/portal/content/menu/')


@login_required
def menu(request):
    menu_list=Menu.objects.all()
    return render_to_response('admin/content/menu/menu-list.html',{'menu_list':menu_list})


@login_required
def add_menu(request):
    if request.method=='POST':
        validate_menu = MenuForm(request.POST)
        if validate_menu.is_valid():
            new_menu = validate_menu.save(commit = False)
            if request.POST.get('status',''):
                new_menu.status = 'on'

            menu_count = Menu.objects.filter(parent=new_menu.parent).count()
            new_menu.lvl = menu_count + 1
            if new_menu.url[-1]!='/':
                new_menu.url = new_menu.url+'/'

            new_menu.save()
            data={"error":False,'response':'Menu created successfully'}
        else:
            data={"error":True,'response':validate_menu.errors}
        return HttpResponse(json.dumps(data))

    c = {}
    c.update(csrf(request))
    parent = Menu.objects.filter(parent=None).order_by('lvl')
    return render_to_response('admin/content/menu/new-menu-item.html',{'parent':parent,'csrf_token':c['csrf_token']})


@login_required
def edit_menu(request, pk):
    if request.method == 'POST':
        menu_instance = Menu.objects.get(pk = pk)
        current_parent = menu_instance.parent
        current_lvl = menu_instance.lvl
        validate_menu = MenuForm(request.POST,instance=menu_instance)

        if validate_menu.is_valid():
            updated_menu = validate_menu.save(commit = False)
            if updated_menu.parent != current_parent:
                try:
                    if updated_menu.parent.id == updated_menu.id:
                        data = {'error':True, 'response':{'parent':'you can not choose the same as parent'}}
                        return HttpResponse(json.dumps(data))
                except:
                    pass

                lnk_count = Menu.objects.filter(parent=updated_menu.parent).count()
                updated_menu.lvl = lnk_count + 1
                lvlmax = Menu.objects.filter(parent=current_parent).aggregate(Max('lvl'))['lvl__max']
                if lvlmax != 1:
                    for i in Menu.objects.filter(parent=current_parent,lvl__gt=current_lvl,lvl__lte=lvlmax):
                        i.lvl = i.lvl-1
                        i.save()
            if updated_menu.url[-1]!='/':
                updated_menu.url = updated_menu.url+'/'

            if request.POST.get('status',''):
                updated_menu.status = 'on'

            updated_menu.save()

            data = {'error':False, 'response':'updated successfully'}
        else:
            data = {'error':True, 'response':validate_menu.errors}
        return HttpResponse(json.dumps(data))

    parent = Menu.objects.filter(parent=None).order_by('lvl')
    current_menu = Menu.objects.get(pk = pk)
    c = {}
    c.update(csrf(request))
    return render_to_response('admin/content/menu/edit-menu-item.html',{'csrf_token':c['csrf_token'],'current_menu':current_menu,'parent':parent})

