import django_filters
from rest_framework import generics
from .serializers import *
from .models import LeaveRequest
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout


class LoginAPIView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Login successful'})
        else:
            return Response({'detail': 'Invalid credentials'})


class LogoutAPIView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'})


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
        employees = get_user_model().objects.all()
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

    def get_queryset(self):
        return LeaveRequest.objects.filter(employee=self.request.user)
