from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def profile_search(request):
    search = request.GET.get("search_query") if request.GET.get("search_query") else ""
    skills = Skill.objects.filter(name__icontains=search)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search)
        | Q(short_intro__icontains=search)
        | Q(skill__in=skills)
    )

    return search, profiles


def custom_paginator(request, profiles, result):
    page = request.GET.get('page')
    result = result
    paginator = Paginator(profiles,result)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page)-5)
    if left_index < 1:
        left_index = 1
    
    right_index = (int(page)+5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return profiles, custom_range