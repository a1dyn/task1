import django_filters
from rest_framework import generics, filters
from .serializers import *
from .models import LeaveRequest
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

class LeaveRequestFilter(django_filters.FilterSet):
    class Meta:
        model = LeaveRequest
        fields = {
            'is_approved': ['exact'],
        }


# Employee List View and Create for Admins  ['GET', 'POST']
class EmployeeView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request):  # for get request
        # search_query = request.GET.get('search')
        ordering_param = request.GET.get('ordering')
        employees = get_user_model().objects.all()

        # if search_query:
        #     search_fields = ['name', 'email']
        #     search_filter = filters.SearchFilter()
        #     employees = search_filter.filter_queryset(request, employees, view=self)

        if ordering_param:
            if ordering_param.startswith('-'):
                employees = employees.order_by(ordering_param[1:]).reverse()
            else:
                employees = employees.order_by(ordering_param)

        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)


    # for post (post)
    queryset = get_user_model().objects.all()
    serializer_class = EmployeeCreateSerializer


# Employee detail page, edit, delete for Admins     ['PUT', 'PATCH', 'DELETE']
class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = EmployeeCreateSerializer


# To approve leave requests from employees ['PUT', 'PATCH']
class LeaveRequestEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LeaveRequestSerializerForAdmin
    queryset = LeaveRequest.objects.all()


# Looking all leave requests ['GET']
class LeaveListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = LeaveRequest.objects.order_by('-is_approved')
    serializer_class = LeaveRequestSerializerForAdmin
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['is_approved']


# Createing and Reading requests of current employee ['GET', 'POST']
class EmployeeLeaveRequestCreateView(generics.ListCreateAPIView):
    serializer_class = EmployeeLeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nature_of_leave']

    def get_queryset(self):
        return LeaveRequest.objects.filter(employee=self.request.user)
