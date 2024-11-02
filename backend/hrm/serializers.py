from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PositionSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Position
        fields = ['id', 'title', 'description', 'department', 'department_name', 
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 
            'first_name', 'last_name', 'full_name',
            'email', 'phone',
            'department', 'department_name',
            'position', 'position_title',
            'hire_date', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class EmergencyContactSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)

    class Meta:
        model = EmergencyContact
        fields = [
            'id', 'employee', 'employee_name',
            'name', 'relationship', 
            'phone', 'alternative_phone',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id', 'name', 'description', 
                 'days_allowed', 'is_active',
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name',
            'leave_type', 'leave_type_name',
            'start_date', 'end_date', 'duration',
            'reason', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_duration(self, obj):
        return (obj.end_date - obj.start_date).days + 1

class SalarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    total_salary = serializers.SerializerMethodField()

    class Meta:
        model = Salary
        fields = [
            'id', 'employee', 'employee_name',
            'basic_salary', 'allowance', 'total_salary',
            'is_active', 'effective_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_salary(self, obj):
        return obj.basic_salary + obj.allowance

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction
        fields = [
            'id', 'name', 'description',
            'amount', 'is_percentage', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class PayrollRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)

    class Meta:
        model = PayrollRecord
        fields = [
            'id', 'employee', 'employee_name',
            'salary', 'total_deductions', 'net_salary',
            'payment_date', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class GoalSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)

    class Meta:
        model = Goal
        fields = [
            'id', 'employee', 'employee_name',
            'title', 'description',
            'target_date', 'status', 'priority',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    
    class Meta:
        model = PerformanceReview
        fields = [
            'id', 'employee', 'employee_name',
            'reviewer', 'reviewer_name',
            'review_period', 'review_date',
            'status', 'overall_rating', 'comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class TimeSheetSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    total_hours = serializers.SerializerMethodField()

    class Meta:
        model = TimeSheet
        fields = [
            'id', 'employee', 'employee_name',
            'date', 'time_in', 'time_out',
            'total_hours', 'status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_hours(self, obj):
        if obj.time_in and obj.time_out:
            time_diff = obj.time_out.hour - obj.time_in.hour
            return f"{time_diff:.2f}"
        return "0.00"

class OvertimeSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)

    class Meta:
        model = Overtime
        fields = [
            'id', 'employee', 'employee_name',
            'date', 'hours', 'reason',
            'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']