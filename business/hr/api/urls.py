from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from hr.api.views import (
    EmployeeList,
    EmployeeDetail,
    average_salaries_per_industry,
    average_salaries_per_yoe,
    average_age_per_industry,
    average_salaries_per_yoe_and_industry,
    agg_salaries_per_yoe_intervals,
)


urlpatterns = [
    path("employees/", EmployeeList.as_view(), name="api_employee_list"),
    path("employees/<int:pk>", EmployeeDetail.as_view(), name="api_employee_detail"),
    path("statistics/average-salaries-per-industry", average_salaries_per_industry, name="api_average_salaries_per_industry"),
    path("statistics/average-salaries-per-yoe", average_salaries_per_yoe, name="api_average_salaries_per_yoe"),
    path("statistics/average-age-per-industry", average_age_per_industry, name="api_average_age_per_industry"),
    path("statistics/average-salaries-per-yoe-and-industry", average_salaries_per_yoe_and_industry, name="api_average_salaries_per_yoe_and_industry"),
    path("statistics/agg-salaries-per-yoe-intervals", agg_salaries_per_yoe_intervals, name="api_agg_salaries_per_yoe_intervals"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
