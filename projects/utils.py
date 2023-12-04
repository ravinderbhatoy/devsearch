from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def project_search(request):
    search = request.GET.get('search_query') if request.GET.get('search_query') else ""
    tags = Tag.objects.filter(name__icontains=search)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search) |
        Q(owner__name__icontains=search) |
        Q(tags__in=tags)
    )
    return search, projects

def custom_paginator(request, projects, result):
    page = request.GET.get('page')
    result = result
    paginator = Paginator(projects,result)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = (int(page)-5)
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page)+5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return projects, custom_range