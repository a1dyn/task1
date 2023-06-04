from django.urls import path
from .views import *


urlpatterns = [
    path('', LoginAPIView.as_view(), name = 'login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name = 'employee_detail'),
    path("employees/", EmployeeView.as_view(), name= 'employee_list'),
    path("leave-requests/<int:pk>/", LeaveRequestEditView.as_view(), name = 'leave_requests_update'),
    path("leave-requests/", LeaveListView.as_view(), name= 'leave_requests'),
    path("employee/leave-requests/", EmployeeLeaveRequestCreateView.as_view(), name = 'employee_leave_requests'),
    ]