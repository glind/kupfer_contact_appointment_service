from rest_framework import viewsets, filters as drf_filters
from django_filters import rest_framework as django_filters

from crm.mixins import OrganizationQuerySetWithGlobalFilterMixin, OrganizationExtensionMixin
from crm.pagination import ContactLimitOffsetPagination
from .models import Contact, Type
from .permissions import ContactPermission
from .serializers import ContactSerializer, TypeSerializer
from . import filters


class ContactViewSet(viewsets.ModelViewSet):
    """
    User's contacts.
    """
    def list(self, request):
        # Use this or the ordering filter won't work
        queryset = self.filter_queryset(self.get_queryset())
        organization_uuid = request.session.get('jwt_organization_uuid')
        queryset = queryset.filter(organization_uuid=organization_uuid)
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        core_user_uuid = self.request.session.get('jwt_core_user_uuid')
        organization_uuid = self.request.session.get('jwt_organization_uuid')
        serializer.save(core_user_uuid=core_user_uuid,
                        organization_uuid=organization_uuid)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(ContactViewSet, self).update(request, *args, **kwargs)

    ordering = ('first_name',)
    filter_backends = (drf_filters.OrderingFilter,
                       drf_filters.SearchFilter,
                       django_filters.DjangoFilterBackend,
                       filters.StartsWithSearchFilter,)
    filter_class = filters.ContactFilter
    search_fields = ('first_name', 'last_name')
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (ContactPermission,)
    pagination_class = ContactLimitOffsetPagination


class TypeViewSet(OrganizationQuerySetWithGlobalFilterMixin,
                  OrganizationExtensionMixin,
                  viewsets.ModelViewSet):

    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = (ContactPermission,)
