from rest_framework import serializers
from .models import Employee, LeaveRequest
from django.contrib.auth import get_user_model


class EmployeeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'name', 'email', 'password', 'contact_number', 'emergency_contact_number', 'address', 'position', 'date_of_birth',
            'marital_status', 'blood_group', 'job_title', 'work_location', 'date_of_joining', 'reporting_to',
            'linkedin_link', 'profile_pic'
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class EmployeeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id', 'name', 'contact_number', 'email',
                  'job_title', 'reporting_to', 'work_location']


class LeaveRequestSerializerForAdmin(serializers.ModelSerializer):

    class Meta:
        model = LeaveRequest
        fields = "__all__"
        ordering = ['-is_approved', 'id']


class EmployeeLeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = LeaveRequest
        exclude = ['is_approved']
