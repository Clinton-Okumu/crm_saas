from rest_framework import serializers
from .models import Department, Position, Employee, LeaveType, LeaveRequest, Salary, PayrollRecord, PerformanceReview, Goal

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

# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()  # Nested Department serializer
    position = PositionSerializer()  # Nested Position serializer

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'employee_id', 'department', 'position', 'hire_date', 'is_active', 'date_of_birth', 'profile_picture']

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

