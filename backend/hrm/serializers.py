from rest_framework import serializers
from .models import Department, Position, Employee, LeaveType, LeaveRequest, Salary, PayrollRecord, PerformanceReview, Goal
from users.serializers import UserSerializer
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'is_active', 'manager']

# Position Serializer
class PositionSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()  # Nested Department serializer

    class Meta:
        model = Position
        fields = ['id', 'title', 'department', 'description', 'is_active']

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # Assuming a User model

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'department', 'position', 'hire_date', 'status', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)  # Extract user if present
        employee = Employee.objects.create(**validated_data)  # Create employee

        # Optionally handle user assignment here
        if user_data:
            employee.user = user_data
            employee.save()

        return employee

# LeaveType Serializer
class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name', 'days_allowed', 'is_active', 'max_days_per_year']

# LeaveRequest Serializer
class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()  # Nested Employee serializer
    leave_type = LeaveTypeSerializer()  # Nested LeaveType serializer

    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'leave_type', 'start_date', 'end_date', 'reason', 'status', 'created_at', 'updated_at']

# Salary Serializer
class SalarySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()  # Nested Employee serializer

    class Meta:
        model = Salary
        fields = ['id', 'employee', 'basic_salary', 'bonus', 'effective_date']

# PayrollRecord Serializer
class PayrollRecordSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()  # Nested Employee serializer

    class Meta:
        model = PayrollRecord
        fields = ['id', 'employee', 'salary', 'total_deductions', 'net_salary', 'payment_date', 'payment_method', 'remarks']

# PerformanceReview Serializer
class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()  # Nested Employee serializer
    reviewer = EmployeeSerializer()  # Nested Reviewer (Employee) serializer

    class Meta:
        model = PerformanceReview
        fields = ['id', 'employee', 'reviewer', 'review_period', 'review_date', 'overall_rating', 'comments', 'action_items']

# Goal Serializer
class GoalSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()  # Nested Employee serializer

    class Meta:
        model = Goal
        fields = ['id', 'employee', 'title', 'target_date', 'status', 'priority']

