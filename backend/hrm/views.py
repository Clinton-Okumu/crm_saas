from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action
from django.db.models import Q
from hrm.permissions import CanManageDepartments, CanManageEmployees, CanManageLeaves, CanManageSalaries

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, CanManageDepartments]
    
    def get_queryset(self):
        queryset = Department.objects.all()
        
        #search by name
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        #filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def employees(self, reqest, pk=None):
        """Get all employees in a department"""
        department = self.get_object()
        employees = Employee.objects.filter(department=department)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a department"""
        department = self.get_object()
        department.is_active = False
        department.save()
        return Response({'status': 'department deactivated'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a department"""
        department = self.get_object()
        department.is_active = True
        department.save()
        return Response({'status': 'department activated'})

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get department statistics"""
        department = self.get_object()
        stats = {
            'total_employees': Employee.objects.filter(department=department).count(),
            'active_employees': Employee.objects.filter(department=department, is_active=True).count(),
            'name': department.name,
            'status': 'active' if department.is_active else 'inactive'
        }
        return Response(stats)

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Position.objects.all()
        
        # Search by title
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
            
        # Filter by department
        department_id = self.request.query_params.get('department', None)
        if department_id:
            queryset = queryset.filter(department_id=department_id)
            
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
            
        return queryset

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in this position"""
        position = self.get_object()
        employees = Employee.objects.filter(position=position)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get position statistics"""
        position = self.get_object()
        stats = {
            'title': position.title,
            'department': position.department.name,
            'total_employees': Employee.objects.filter(position=position).count(),
            'active_employees': Employee.objects.filter(position=position, is_active=True).count(),
            'status': 'active' if position.is_active else 'inactive'
        }
        return Response(stats)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, CanManageEmployees]

    def get_queryset(self):
        queryset = Employee.objects.all()
        
        # Search by name or employee_id
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(employee_id__icontains=search)
            )
        
        # Filter by department
        department_id = self.request.query_params.get('department', None)
        if department_id:
            queryset = queryset.filter(department_id=department_id)
            
        # Filter by position
        position_id = self.request.query_params.get('position', None)
        if position_id:
            queryset = queryset.filter(position_id=position_id)
            
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
            
        return queryset

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get complete employee profile"""
        employee = self.get_object()
        return Response({
            'personal_info': EmployeeSerializer(employee).data,
            'department': employee.department.name,
            'position': employee.position.title,
            'is_active': employee.is_active
        })

    @action(detail=True, methods=['get'])
    def leaves(self, request, pk=None):
        """Get employee's leave history"""
        employee = self.get_object()
        leaves = LeaveRequest.objects.filter(employee=employee)
        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def salary(self, request, pk=None):
        """Get employee's salary information"""
        employee = self.get_object()
        try:
            salary = Salary.objects.get(employee=employee)
            serializer = SalarySerializer(salary)
            return Response(serializer.data)
        except Salary.DoesNotExist:
            return Response(
                {'message': 'No salary information found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """Get employee's performance reviews"""
        employee = self.get_object()
        reviews = PerformanceReview.objects.filter(employee=employee)
        serializer = PerformanceReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get employee's attendance records"""
        employee = self.get_object()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        timesheets = TimeSheet.objects.filter(employee=employee)
        if start_date:
            timesheets = timesheets.filter(date__gte=start_date)
        if end_date:
            timesheets = timesheets.filter(date__lte=end_date)
            
        serializer = TimeSheetSerializer(timesheets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Toggle employee active status"""
        employee = self.get_object()
        employee.is_active = not employee.is_active
        employee.save()
        return Response({
            'message': f"Employee status changed to {'active' if employee.is_active else 'inactive'}",
            'is_active': employee.is_active
        })

    def destroy(self, request, *args, **kwargs):
        """Soft delete by setting is_active to False"""
        employee = self.get_object()
        employee.is_active = False
        employee.save()
        return Response({
            'message': 'Employee deactivated successfully'
        }, status=status.HTTP_200_OK)


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated, CanManageSalaries]

    def get_queryset(self):
        queryset = Salary.objects.all()
        
        # Filter by employee
        employee_id = self.request.query_params.get('employee', None)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
            
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
            
        return queryset

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get salary history for an employee"""
        salary = self.get_object()
        payroll_records = PayrollRecord.objects.filter(employee=salary.employee)
        serializer = PayrollRecordSerializer(payroll_records, many=True)
        return Response(serializer.data)

class DeductionViewSet(viewsets.ModelViewSet):
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Deduction.objects.all()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
            
        return queryset

class PayrollRecordViewSet(viewsets.ModelViewSet):
    queryset = PayrollRecord.objects.all()
    serializer_class = PayrollRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PayrollRecord.objects.all()
        
        # Filter by employee
        employee_id = self.request.query_params.get('employee', None)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
            
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(payment_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(payment_date__lte=end_date)
            
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process a payroll record"""
        payroll = self.get_object()
        payroll.status = 'processed'
        payroll.save()
        return Response({
            'message': 'Payroll processed successfully'
        })

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark payroll as paid"""
        payroll = self.get_object()
        payroll.status = 'paid'
        payroll.save()
        return Response({
            'message': 'Payroll marked as paid'
        })

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """Get monthly payroll summary"""
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if not month or not year:
            return Response({
                'message': 'Month and year parameters are required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        records = PayrollRecord.objects.filter(
            payment_date__month=month,
            payment_date__year=year
        )
        
        summary = {
            'total_salary': sum(record.salary for record in records),
            'total_deductions': sum(record.total_deductions for record in records),
            'net_payroll': sum(record.net_salary for record in records),
            'processed_count': records.filter(status='processed').count(),
            'paid_count': records.filter(status='paid').count(),
            'pending_count': records.filter(status='pending').count(),
        }
        
        return Response(summary)

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PerformanceReview.objects.all()
        
        # Filter by employee
        employee_id = self.request.query_params.get('employee', None)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
            
        # Filter by reviewer
        reviewer_id = self.request.query_params.get('reviewer', None)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
            
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by review period
        review_period = self.request.query_params.get('review_period', None)
        if review_period:
            queryset = queryset.filter(review_period=review_period)
            
        return queryset

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit performance review for approval"""
        review = self.get_object()
        review.status = 'in_review'
        review.save()
        return Response({'message': 'Review submitted successfully'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark performance review as completed"""
        review = self.get_object()
        review.status = 'completed'
        review.save()
        return Response({'message': 'Review completed successfully'})

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Goal.objects.all()
        
        # Filter by employee
        employee_id = self.request.query_params.get('employee', None)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
            
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Mark goal as in progress"""
        goal = self.get_object()
        goal.status = 'in_progress'
        goal.save()
        return Response({'message': 'Goal started'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark goal as completed"""
        goal = self.get_object()
        goal.status = 'completed'
        goal.save()
        return Response({'message': 'Goal completed'})

    @action(detail=False, methods=['get'])
    def team_goals(self, request):
        """Get goals for team members (for managers)"""
        if request.user.role != 'manager':
            return Response({
                'message': 'Only managers can view team goals'
            }, status=status.HTTP_403_FORBIDDEN)
            
        department_employees = Employee.objects.filter(department=request.user.department)
        goals = Goal.objects.filter(employee__in=department_employees)
        serializer = self.get_serializer(goals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get goals summary for an employee"""
        employee_id = request.query_params.get('employee', None)
        if not employee_id:
            return Response({
                'message': 'Employee ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        goals = Goal.objects.filter(employee_id=employee_id)
        summary = {
            'total_goals': goals.count(),
            'completed': goals.filter(status='completed').count(),
            'in_progress': goals.filter(status='in_progress').count(),
            'pending': goals.filter(status='pending').count(),
            'by_priority': {
                'high': goals.filter(priority='high').count(),
                'medium': goals.filter(priority='medium').count(),
                'low': goals.filter(priority='low').count()
            }
        }
        return Response(summary)

class TimeSheetViewSet(viewsets.ModelViewSet):
    queryset = TimeSheet.objects.all()
    serializer_class = TimeSheetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TimeSheet.objects.all()
        
        # Filter by employee
        employee_id = self.request.query_params.get('employee', None)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    @action(detail=False, methods=['get'])
    def my_timesheet(self, request):
        """Get current user's timesheet"""
        timesheets = TimeSheet.objects.filter(employee=request.user)
        serializer = self.get_serializer(timesheets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def team_timesheet(self, request):
        """Get team's timesheet (for managers)"""
        if request.user.role != 'manager':
            return Response({
                'message': 'Only managers can view team timesheets'
            }, status=status.HTTP_403_FORBIDDEN)
            
        department_employees = Employee.objects.filter(department=request.user.department)
        timesheets = TimeSheet.objects.filter(employee__in=department_employees)
        serializer = self.get_serializer(timesheets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve timesheet"""
        timesheet = self.get_object()
        timesheet.status = 'approved'
        timesheet.save()
        return Response({'message': 'Timesheet approved successfully'})

class OvertimeViewSet(viewsets.ModelViewSet):
    queryset = Overtime.objects.all()
    serializer_class = OvertimeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Overtime.objects.all()
        
        # Filter by employee
        employee_id = self.request.query_params.get('employee', None)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve overtime request"""
        overtime = self.get_object()
        overtime.status = 'approved'
        overtime.save()
        return Response({'message': 'Overtime approved successfully'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject overtime request"""
        overtime = self.get_object()
        overtime.status = 'rejected'
        overtime.save()
        return Response({'message': 'Overtime rejected successfully'})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get overtime summary"""
        employee_id = request.query_params.get('employee', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        overtime_records = Overtime.objects.all()
        
        if employee_id:
            overtime_records = overtime_records.filter(employee_id=employee_id)
        if start_date:
            overtime_records = overtime_records.filter(date__gte=start_date)
        if end_date:
            overtime_records = overtime_records.filter(date__lte=end_date)
            
        summary = {
            'total_hours': sum(record.hours for record in overtime_records),
            'approved_hours': sum(record.hours for record in overtime_records.filter(status='approved')),
            'pending_hours': sum(record.hours for record in overtime_records.filter(status='pending')),
            'rejected_hours': sum(record.hours for record in overtime_records.filter(status='rejected')),
            'total_requests': overtime_records.count(),
            'status_breakdown': {
                'approved': overtime_records.filter(status='approved').count(),
                'pending': overtime_records.filter(status='pending').count(),
                'rejected': overtime_records.filter(status='rejected').count()
            }
        }
        
        return Response(summary)
