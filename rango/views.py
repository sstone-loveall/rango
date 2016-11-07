from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from rango.core import session_data
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page
from rango.utils import format_date
from rango.view_model_managers import category_view_model_manager


def index(request):
    # order by num. of likes and views, both in desc order, get top 5 or all if less
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    visit_data = session_data.Visits(request)
    visit_count = visit_data.get_visits_count()
    last_visit = visit_data.get_last_visit_date()

    context_dict['visits'] = visit_count
    context_dict['last_visit_on'] = format_date.weekday_month_day_year(last_visit)

    visit_data.update_visits_session(visit_count, last_visit)

    response = render(request, 'rango/index.html', context_dict)

    return response


def about(request):
    visit_data = session_data.Visits(request)
    visit_count = visit_data.get_visits_count()
    last_visit = format_date.weekday_month_day_year(visit_data.get_last_visit_date)
    context_dict = {'visits': visit_count, 'last_visit_on': last_visit}

    return render(request, 'rango/about.html', context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_url):
    try:
        cat = Category.objects.get(slug=category_name_url)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


def category(request, category_name_url):
    manager = category_view_model_manager.CategoryViewModelManager()
    context_dict = manager.populate_category_view_context(category_name_url)
    return render(request, 'rango/category.html', context_dict)


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save the user form data to the database
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # save the profile form data to the database
            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        # not a POST, so render blank forms
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # use Django's machinery to see if the username/password combo is valid
        user = authenticate(username=username, password=password)

        if user:
            # if user object exists, the details are correct. Now check if active.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # bad login
            print "Invalid login details {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        # request is not a post, so display the form
        # no context variables to pass, so blank dict used
        return render(request, 'rango/login.html', {})


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')
