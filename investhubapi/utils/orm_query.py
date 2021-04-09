from django.db.models import Q


def construct_contain_query(q, field_name_query, value):
    if isinstance(field_name_query, list):
        # If filter field is list, loop all using OR operator
        for fnq in field_name_query:
            v_set = {fnq + "__icontains": value.strip()}
            q |= Q(**v_set)
    else:
        v_set = {field_name_query + "__icontains": value.strip()}
        q |= Q(**v_set)

    return q


def filter_field_contain(queryset, filters, field_name, field_name_query=None):
    q = Q()
    values = filters.get(field_name)
    if values is not None:

        if field_name_query is None:
            field_name_query = field_name

        if isinstance(values, list):
            # If filter value is list, loop all using OR operator
            for v in values:
                q = construct_contain_query(q, field_name_query, v)
        else:
            q = construct_contain_query(q, field_name_query, values)

    return queryset.filter(q)


def filter_select_field_contain(queryset, fields, value):
    q = construct_contain_query(Q(), fields, value)
    return queryset.filter(q)


def filter_field_equal(queryset, filters, field_name, field_name_query=None):
    q = Q()
    values = filters.get(field_name)
    if values is not None:

        if field_name_query is None:
            field_name_query = field_name

        if isinstance(values, list):
            # If filter value is list and len more than 0, get 1st value only
            if len(values) > 0:
                v_set = {field_name_query: values[0]}
                q = Q(**v_set)

        else:
            v_set = {field_name_query: values}
            q = Q(**v_set)

    return queryset.filter(q)
