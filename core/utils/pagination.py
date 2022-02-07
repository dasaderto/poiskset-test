from typing import List

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError


def paginate(resource, data: QuerySet, page, per_page=15, sorting: List[str] = ()):
    if sorting:
        try:
            data = data.order_by(*sorting)
        except:
            pass
    try:
        paginator = Paginator(data, per_page)
    except:
        raise ValidationError("Something wrong")
    if not page:
        return {
            'data': resource(data, many=True).data
        }
    try:
        output = paginator.page(page)
    except PageNotAnInteger:
        output = paginator.page(1)
    except EmptyPage:
        output = paginator.page(paginator.num_pages)
    try:
        cur_page = int(page)
    except:
        raise ValidationError('Invalid page')

    try:
        objects_count = data.count()
    except TypeError:
        objects_count = len(data)

    return {
        'data': resource(output, many=True).data,
        'links': {
            'current_page': cur_page,
            'next_page': output.next_page_number() if output.has_next() else None,
            'prev_page': output.previous_page_number() if output.has_previous() else 1,
            'last_page': paginator.num_pages,
            'objects_count': objects_count
        }
    }
