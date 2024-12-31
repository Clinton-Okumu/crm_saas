from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from hrm.permissions import CanManageDepartments, CanManageLeaves, CanManageSalaries, CanManageEmployees
from .models import Department, Employee, Salary, LeaveRequest, LeaveType
from .serializers import DepartmentSerializer, EmployeeSerializer, LeaveRequestSerializer, LeaveTypeSerializer, SalarySerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing departments in the HR module.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, CanManageDepartments]

    @action(detail=False, methods=['get'])
    def list_departments(self, request):
        """
        Custom action to list departments
        """
        departments = self.get_queryset()
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Employee records.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Add any custom behavior during employee creation.
        For example, associate the employee with the currently logged-in user if necessary.
        """
        serializer.save()

    def get_queryset(self):
        """
        Customize the queryset if needed, e.g., filter employees by current user or status.
        """
        return Employee.objects.all()

class SalaryViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing salaries in the HR module.
    """
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated, CanManageSalaries]

    @action(detail=True, methods=['get'])
    def view_salary(self, pk=None):
        """
        Custom action to view a salary record
        """
        try:
            salary = self.get_object()
        except Salary.DoesNotExist:
            raise NotFound(detail="Salary record not found")
        serializer = self.get_serializer(salary)
        return Response(serializer.data)


class LeaveViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing leave requests in the HR module.
    """
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated, CanManageLeaves]

    @action(detail=True, methods=['get'])
    def view_leave(self, pk=None):
        """
        Custom action to view leave details
        """
        try:
            leave_request = self.get_object()
        except LeaveRequest.DoesNotExist:
            raise NotFound(detail="Leave request not found")
        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_leave_status(self, request, pk=None):
        """
        Custom action to update leave request status (approve or reject)
        """
        try:
            leave_request = self.get_object()
        except LeaveRequest.DoesNotExist:
            raise NotFound(detail="Leave request not found")

        status = request.data.get('status')  # Get the status from the request body

        if status not in [LeaveRequest.APPROVED, LeaveRequest.REJECTED]:
            return Response({"detail": "Invalid status"}, status=400)

        leave_request.status = status
        leave_request.save()
        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_leave_types(self, request):
        """
        Custom action to list all leave types
        """
        leave_types = LeaveType.objects.all()
        serializer = LeaveTypeSerializer(leave_types, many=True)
        return Response(serializer.data)

