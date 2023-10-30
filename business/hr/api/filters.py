from django_filters import rest_framework as filters

from hr.models import Employee


class EmployeeListFilter(filters.FilterSet):
    dob_from = filters.DateFilter(
        field_name='dob',
        lookup_expr='gte',
        label='Born Date From',
    )
    
    dob_to = filters.DateFilter(
        field_name='dob',
        lookup_expr='lte',
        label='Born Date To',
    )
    
    surname = filters.CharFilter(
        field_name='last_name',
        lookup_expr='icontains',
        label='Surname contains',
    )
    
    class Meta:
        model = Employee
        fields = "__all__"
