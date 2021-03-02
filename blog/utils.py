from django.core.paginator import Paginator


def paginator(request, posts):
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    return page, is_paginated
