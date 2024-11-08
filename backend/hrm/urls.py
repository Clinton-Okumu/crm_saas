from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet,
    PositionViewSet,
    EmployeeViewSet,
    SalaryViewSet,
    DeductionViewSet,
    PayrollRecordViewSet,
    PerformanceReviewViewSet,
    GoalViewSet,
    TimeSheetViewSet,
    OvertimeViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()

# Department endpoints
# /api/departments/
# /api/departments/{id}/
# /api/departments/{id}/employees/
# /api/departments/{id}/deactivate/
# /api/departments/{id}/activate/
# /api/departments/{id}/statistics/
router.register(r'departments', DepartmentViewSet)

# Position endpoints
# /api/positions/
# /api/positions/{id}/
# /api/positions/{id}/employees/
# /api/positions/{id}/statistics/
router.register(r'positions', PositionViewSet)

# Employee endpoints
# /api/employees/
# /api/employees/{id}/
# /api/employees/{id}/profile/
# /api/employees/{id}/leaves/
# /api/employees/{id}/salary/
# /api/employees/{id}/performance/
# /api/employees/{id}/attendance/
# /api/employees/{id}/toggle_status/
router.register(r'employees', EmployeeViewSet)

# Salary endpoints
# /api/salaries/
# /api/salaries/{id}/
# /api/salaries/{id}/history/
router.register(r'salaries', SalaryViewSet)

# Deduction endpoints
# /api/deductions/
# /api/deductions/{id}/
router.register(r'deductions', DeductionViewSet)

# Payroll record endpoints
# /api/payroll-records/
# /api/payroll-records/{id}/
# /api/payroll-records/{id}/process/
# /api/payroll-records/{id}/mark_paid/
# /api/payroll-records/monthly_summary/
router.register(r'payroll-records', PayrollRecordViewSet)

# Performance review endpoints
# /api/performance-reviews/
# /api/performance-reviews/{id}/
# /api/performance-reviews/{id}/submit/
# /api/performance-reviews/{id}/complete/
router.register(r'performance-reviews', PerformanceReviewViewSet)

# Goal endpoints
# /api/goals/
# /api/goals/{id}/
# /api/goals/{id}/start/
# /api/goals/{id}/complete/
# /api/goals/team_goals/
# /api/goals/summary/
router.register(r'goals', GoalViewSet)

# Timesheet endpoints
# /api/timesheets/
# /api/timesheets/{id}/
# /api/timesheets/my_timesheet/
# /api/timesheets/team_timesheet/
# /api/timesheets/{id}/approve/
router.register(r'timesheets', TimeSheetViewSet)

# Overtime endpoints
# /api/overtime/
# /api/overtime/{id}/
# /api/overtime/{id}/approve/
# /api/overtime/{id}/reject/
# /api/overtime/summary/
router.register(r'overtime', OvertimeViewSet)

# Wire up our API using automatic URL routing
urlpatterns = [
    path('api/', include(router.urls)),
]