from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page


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

        # retrieve associated pages
        pages = Page.objects.filter(category=category)

        # adds our results list to the template context
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


