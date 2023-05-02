from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    search_fields = ('name',)
    lookup_field = 'slug'
