from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def index(request):
    # order by num. of likes in desc order, get top 5 or all if less
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)


def about(request):
    return HttpResponse("Rango says here is the about page.")


def category(request, category_name_slug):
    context_dict = {}

    try:
        # try to find a category name from the slug
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category_name_url'] = category.slug

        # retrieve associated pages
        pages = Page.objects.filter(category=category)

        # adds our results list to the template context
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


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


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
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

                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)



