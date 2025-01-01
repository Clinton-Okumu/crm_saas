from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from hrm.permissions import CanManageDepartments, CanManageLeaves, CanManageSalaries, CanManageEmployees
from .models import Department, Employee, Salary, LeaveRequest, LeaveType
from .serializers import DepartmentSerializer, EmployeeSerializer, LeaveRequestSerializer, LeaveTypeSerializer, SalarySerializer
from rest_framework import status

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
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated, CanManageSalaries]

    def create(self, request, *args, **kwargs):
        # Extract data from the request
        employee_name = request.data.get('employee')
        basic_salary = request.data.get('basic_salary')
        bonus = request.data.get('bonus', 0)  # Default bonus to 0 if not provided
        effective_date = request.data.get('effective_date')

        # Validate required fields
        if not employee_name or not basic_salary or not effective_date:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Optional: Validate employee existence
        if not Employee.objects.filter(first_name=employee_name).exists():
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Create the Salary instance
            salary = Salary.objects.create(
                employee=employee_name,
                basic_salary=basic_salary,
                bonus=bonus,
                effective_date=effective_date
            )

            # Prepare the response data manually
            response_data = {
                "id": salary.id,
                "employee": salary.employee,
                "basic_salary": salary.basic_salary,
                "bonus": salary.bonus,
                "effective_date": salary.effective_date
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

