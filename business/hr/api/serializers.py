from rest_framework import serializers

from hr.models import Employee, Industry


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

        
class DetailEmployeeSerializer(EmployeeSerializer):
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all())


class StatisticsEmployeeSerializer(EmployeeSerializer):
    industry = serializers.StringRelatedField(read_only=True)


class ListEmployeeSerializer(EmployeeSerializer):
    industry = IndustrySerializer(read_only=True)
