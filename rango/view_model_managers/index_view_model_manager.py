from rango.models import Category, Page


class IndexViewModelManager:
    context_dict = {}

    def __init__(self):
        pass

    def populate_category_view_context(self, category_name_url):
        try:
            # try to find a category name from the slug
            # adds our results list to the template context
            category = Category.objects.get(slug=category_name_url)
            self.context_dict['category_name'] = category.name
            self.context_dict['category_name_url'] = category.slug
            self.context_dict['pages'] = self.associated_pages(category)
            self.context_dict['category'] = category
        except Category.DoesNotExist:
            pass

        return self.context_dict

    def associated_pages(self, category):
        pages = Page.objects.filter(category=category)
        return pages