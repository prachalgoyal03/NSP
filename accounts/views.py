from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm use this for not custom
from accounts.forms import (
    EditProfileForm,
    ProjectForm,
    SignUpForm,
    SkillForm,
)
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from accounts.models import User, project_details


@login_required
def project_home(request):
    args = {}
    return render(request, 'accounts/project_home.html', args)


@login_required
def describe(request):
    project_registered = False

    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            project_details = project_form.save()
            project_details = project_form.save(commit=False)
            project_registered = True
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        project_form = ProjectForm()
    return render(request, 'accounts/describe.html', {'project_form': project_form, 'project_registered': project_registered})


def home(request):
    name = "ideate 2018"
    args = {'name': name}
    return render(request, 'accounts/index.html', args)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/account/')
            else:
                return HttpResponse("Your NSP account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'accounts/login.html', {})


def search(request):
    if request.method=='POST':
        srch = request.POST['srh']

        if srch:
            match1 = User.objects.filter(first_name__icontains=srch)
            #TODO skill name search functionlity to be added
            match2 = project_details.objects.filter(project_name__icontains=srch)
            match3 = project_details.objects.filter(branch__icontains=srch)
            match4 = project_details.objects.filter(mentor_name__icontains=srch)
            if match1:
                print("match1")
                return render(request, 'accounts/search.html', {'sr': match1, 'condition': 'person'})
            elif match2:
                print("match2")
                return render(request, 'accounts/search.html', {'sr': match2, 'condition': 'project'})
            elif match3:
                print("match3")
                return render(request, 'accounts/search.html', {'sr': match3, 'condition': 'branch'})
            elif match4:
                print("match4")
                return render(request, 'accounts/search.html', {'sr': match4, 'condition': 'mentor'})
            else:
                return render(request, 'accounts/search.html', {'sr': 'search_fail', 'condition': 'search_fail'})

        else:
            return HttpResponse('/account/search/')
    return render(request, 'accounts/search.html')


@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


def about(request):
    return HttpResponse("<h1>About Us</h1>")


# pass, if you don't want to write the method yet

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            # so that user does not get logged out, not working as of now.
            # TODO
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('/account/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

# Go through this, this is important


def signup(request):
    registered = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.branch = form.cleaned_data.get('branch')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.year = form.cleaned_data.get('year')
            # user.proifle.image = form.cleaned_data.get('image')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/account/registersuccess')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'registered': registered})


@login_required
def addskill(request):
    skill_added = False

    if request.method == 'POST':
        skill_form = SkillForm(data=request.POST)

        if skill_form.is_valid():
            skill_detail = skill_form.save()
            skill_detail = skill_form.save(commit=False)
            skill_added = True
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        skill_form = ProjectForm()
    return render(request, 'accounts/addskill.html', {'skill_form': skill_form, 'skill_added': skill_added})


def skills(request):
    pass


def registersuccess(request):
    return render(request, 'accounts/registersuccess.html')