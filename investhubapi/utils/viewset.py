import json

from rest_framework import viewsets, status
from rest_framework.response import Response

from investhubapi.utils.orm_query import filter_field_contain, filter_field_equal, filter_select_field_contain

"""
# override
filter_field_contain_list (list of tuple) : filter the query using LIKE '%keyword%' operator by chaining AND operator
filter_field_equal_list (list of tuple)   : filter the query using = operator by chaining AND operator

# additional request param
size                            : provided by drf pagination class, use to limit result for non select
filter                          : filter queryset using above override values
sorter                          : sort queryset
fields[]                        : return only selected fields (pass to serializer to perform the action)
exclude_fields[]                : return without selected fields (pass to serializer to perform the action)
select                          : if not none, remove pagination
select.size                     : if not none, limit the return result depend on size
select.fields & select.value    : if both are not none, filter by provided fields by the same value using OR operator
"""


class ModelViewSetMixin:
    init_filter_field_contain_list = [
        ("created_at",),
        ("updated_at",),
        ("deleted_at",),
    ]

    # TODO implement filter_select_field_list

    filter_field_contain_list = []
    filter_field_equal_list = []
    filter_field_custom_list = []
    sorter_field_list = []

    def mixin_get_serializer_context(self, c):
        fields = self.request.query_params.getlist('fields[]')
        exclude_fields = self.request.query_params.getlist('exclude_fields[]')
        if fields:
            c.update({
                "fields": fields
            })
        if exclude_fields:
            c.update({
                "exclude_fields": exclude_fields
            })
        return c

    def mixin_get_queryset(self, qs):
        filters = self.request.query_params.get('filter')

        if filters:
            filters = json.loads(filters)

            for field_tuple in self.init_filter_field_contain_list + self.filter_field_contain_list:
                field_name = field_tuple[0]
                field_name_query = field_tuple[1] if len(field_tuple) == 2 else None
                qs = filter_field_contain(qs, filters, field_name=field_name, field_name_query=field_name_query)

            for field_tuple in self.filter_field_equal_list:
                field_name = field_tuple[0]
                field_name_query = field_tuple[1] if len(field_tuple) == 2 else None
                qs = filter_field_equal(qs, filters, field_name=field_name, field_name_query=field_name_query)

            for field_tuple in self.filter_field_custom_list:
                field_name = field_tuple[0]
                filter_func = field_tuple[1]
                value = filters.get(field_name)
                if value is not None:
                    qs = filter_func(qs, value)

        sorter = self.request.query_params.get('sorter')
        if sorter:
            sorter = json.loads(sorter)
            field = sorter.get('field')
            order = sorter.get('order')

            if field and order:

                pair_list = self.init_filter_field_contain_list + self.filter_field_contain_list \
                            + self.filter_field_equal_list + self.sorter_field_list
                field_tuple = next((x for x in pair_list if x[0] == field), None)
                if field_tuple:

                    field_name_query = field_tuple[1] if len(field_tuple) == 2 else field_tuple[0]

                    if field_name_query:

                        if order.lower() in ('asc', 'ascend'):
                            qs = qs.order_by(field_name_query)
                        elif order.lower() in ('desc', 'descend'):
                            qs = qs.order_by('-' + field_name_query)

        select = self.request.query_params.get('select')
        if select:
            self.pagination_class = None
            select = json.loads(select)
            fields = select.get('fields')
            value = select.get('value')
            size = select.get('size')

            if fields and value:
                pair_list = self.init_filter_field_contain_list + self.filter_field_contain_list
                validated_fields = []

                def insert_into_validated_fields(sel_field):
                    sel_field_tuple = next((x for x in pair_list if x[0] == sel_field), None)
                    if sel_field_tuple:
                        if len(sel_field_tuple) == 2:
                            validated_fields.append(sel_field_tuple[1])
                        else:
                            validated_fields.append(sel_field_tuple[0])
                    else:
                        validated_fields.append(f)

                if isinstance(fields, list):
                    for f in fields:
                        insert_into_validated_fields(f)
                else:
                    insert_into_validated_fields(fields)

                qs = filter_select_field_contain(qs, validated_fields, value)

            if size:
                qs = qs[:int(size)]

        # For check query
        # print(qs.query)
        return qs


class CModelViewSet(viewsets.ModelViewSet, ModelViewSetMixin):

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            """
            Allow create in list (bulk)
            """
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return super().create(request, *args, **kwargs)

    def get_serializer_context(self):
        c = super().get_serializer_context()
        return super().mixin_get_serializer_context(c)

    def get_queryset(self):
        qs = super().get_queryset()
        return super().mixin_get_queryset(qs)


class CReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet, ModelViewSetMixin):
    def get_serializer_context(self):
        c = super().get_serializer_context()
        return super().mixin_get_serializer_context(c)

    def get_queryset(self):
        qs = super().get_queryset()
        return super().mixin_get_queryset(qs)
