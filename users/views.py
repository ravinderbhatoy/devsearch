from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Profile, Message
from .forms import UserForm, ProfileForm, SkillForm, MessageForm
from .utils import profile_search, custom_paginator

def register_user(request):
    page = "register"
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You are successfully registered")
            login(request, user)
            return redirect("edit-profile")
        else:
            messages.error(request, "An error occurred during registration")
    context = {"page": page, "form": form}
    return render(request, "users/login.html", context)


def login_user(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else "account")
        else:
            messages.error(request, "Username OR Password is incorrect")
    context = {}
    return render(request, "users/login.html", context)


def logout_user(request):
    logout(request)
    messages.success(request, "User was successfully logout")
    return redirect("profiles")


def profiles(request):
    search, profiles = profile_search(request)
    profiles, custom_range = custom_paginator(request, profiles, 6)
    context = {"profiles": profiles, "search": search, 'custom_range': custom_range}
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    context = {
        "profile": profile,
        "top_skills": top_skills,
        "other_skills": other_skills,
    }
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    context = {"profile": profile}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        form.save()
        return redirect("account")
    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")
    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect("account")
    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    obj = skill.name
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully.")
        return redirect("account")
    return render(request, "delete_form.html", {"obj": obj})

@login_required(login_url="login")
def all_messages(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {'message_requests': message_requests, 'unread_count': unread_count}
    return render(request, 'users/inbox.html', context)

@login_required(login_url="login")
def view_message(request, pk):
    profile = request.user.profile
    request_message = profile.messages.get(id=pk)
    if request_message.is_read == False:
        request_message.is_read = True
        request_message.save()
    context = {'request_message': request_message}
    return render(request, 'users/message.html', context)


def add_message(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = sender
            new_message.recipient = recipient

            if sender:
                new_message.name = sender.name
                new_message.email = sender.email
            new_message.save()

            messages.success(request, 'Your message was sent successfully!')
            return redirect('user-profile', pk=recipient.id)
    context = {'form': form, 'recipient': recipient}
    return render(request, 'users/message_form.html', context)