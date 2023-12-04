from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Project, Tag
from django.contrib import messages
from .forms import ProjectForm, ReviewForm
from .utils import project_search, custom_paginator

def projects(request):
    search, projects = project_search(request)
    projects, custom_range = custom_paginator(request, projects, 6)
    context = {'projects': projects, 'search': search, 'custom_range': custom_range}
    return render(request,'projects/projects.html', context)

def single_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    project.reviewers
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.owner = request.user.profile
        review.project = project
        review.save()
        project.get_vote_count  # this is a property

        messages.success(request, 'Comment saved!')
        return redirect('single-project', pk=project.id)
    context = {'project': project, 'form': ReviewForm}
    return render(request, 'projects/single-project.html', context)   

@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        new_tags = request.POST.get('new_tags').replace(",", ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner=profile
            project.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        new_tags = request.POST.get('new_tags').replace(",", ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')
    context = {'form': form, 'project': project}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    obj = project.name
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    return render(request, 'delete_form.html', {'obj': obj})

@login_required(login_url='login')
def remove_tag(request, project_id, tag_id):
    project = Project.objects.get(id=project_id)
    tag = Tag.objects.get(id=tag_id)
    project.tags.remove(tag_id)
    return redirect('update-project', pk=project.id)