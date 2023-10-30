import pandas as pd
from json import loads
from datetime import date, timedelta

from rest_framework import mixins, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
import django_filters.rest_framework
                    
from hr.api.serializers import (
    ListEmployeeSerializer,
    DetailEmployeeSerializer,
    StatisticsEmployeeSerializer
)
from hr.models import Employee
from hr.api.filters import EmployeeListFilter


class EmployeeList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    filterset_class = EmployeeListFilter
    ordering_fields = ["id", "last_name", "dob", "industry", "annual_income", "yoe"]
    pagination_class = PageNumberPagination
    queryset = Employee.objects.all()
    serializer_class = ListEmployeeSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = DetailEmployeeSerializer

    
def extract():
    employees = Employee.objects.all()
    return pd.DataFrame(StatisticsEmployeeSerializer(employees, many=True).data)
    
def load(df):
    return loads(df.to_json(orient='records'))


@api_view(["GET"])
def average_salaries_per_industry(request):
    df = extract()
    
    df = df.groupby('industry', as_index=False)['annual_income'].mean()
    df['annual_income'] = df['annual_income'].astype(int)
    df.rename(columns={'annual_income': 'average_annual_income'}, inplace=True)
    
    return Response(load(df))


@api_view(["GET"])
def average_salaries_per_yoe(request):
    df = extract()
    
    df = df.groupby('yoe', as_index=False)['annual_income'].mean()
    df['annual_income'] = df['annual_income'].astype(int)
    df.rename(columns={'annual_income': 'average_annual_income'}, inplace=True)
    
    return Response(load(df))


@api_view(["GET"])
def average_age_per_industry(request):
    df = extract()
    
    df['dob'] = pd.to_datetime(df['dob'], format='%Y-%m-%d')
    df['age'] = (date.today() - df['dob'].dt.date) / timedelta(days=365)
    df['age'] = df['age'].astype(int)
    
    df = df.groupby('industry', as_index=False)['age'].mean()
    df['age'] = df['age'].astype(int)
    df.rename(columns={'age': 'average_age'}, inplace=True)
    
    return Response(load(df))


@api_view(["GET"])
def average_salaries_per_yoe_and_industry(request):
    df = extract()
    
    df = df.groupby(['yoe', 'industry'], as_index=False)['annual_income'].mean()
    df['annual_income'] = df['annual_income'].astype(int)
    df.rename(columns={'annual_income': 'average_annual_income'}, inplace=True)
    
    return Response(load(df))


@api_view(["GET"])
def agg_salaries_per_yoe_intervals(request):
    df = extract()
    
    bins = pd.cut(df['yoe'],
                  bins=[0, 2, 5, 10, 20, 35],
                  include_lowest=True,
                  labels=['0-2 yoe', '2-5 yoe', '5-10 yoe', '10-20 yoe', '20-35 yoe'])
    
    agg_lst = ['mean', 'median', 'std', 'min', 'max', 'count']
    df = df.groupby(bins, as_index=False)['annual_income'].agg(agg_lst)
    df = df[df['count'] > 1]
    
    df[agg_lst] = df[agg_lst].astype(int)
    
    
    return Response(load(df))
