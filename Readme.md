# Login API
Provide email and password to login

# For Admins

**Every admin class based view contains attribute `permission_classes = [IsAdminUser]` to restrict CRUD methods for anonymouses and others from admin/superusers**

## Employee Management Page

### API List of Employees

Gets all employees' instances and via **EmployeeListSerializer** serializes data to Python renderable format (JSON/XML)

```
def get(self, request):
    employees = get_user_model().objects.all()
    serializer = EmployeeListSerializer(employees, many=True)
    return Response(serializer.data)
```

### Employee Detail, Update, Delete API

All these API methods are done by single class **EmployeeDetailView**, it uses _Generic Class Based API Views_, being more specific **RetrieveUpdateDestroyAPIView** where queryset is employees' instances as serializer_class used **EmployeeCreateSerializer** since fields are same for create and update.

```
class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = EmployeeCreateSerializer
```

### Employee Create API

This method is done by using **CreateAPIView** which is also imported from _Generic Class Based API Views_. It requires queryset and serializer*class (\_same as in Deatil, Update, Delete*)

```
class EmployeeView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request):  # for get request
        employees = get_user_model().objects.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)

    # Post request
    queryset = get_user_model().objects.all()
    serializer_class = EmployeeCreateSerializer
```

## Leave Management page

### List of Employees' Leave Requests

Listing leave requests is done by method "read" so used **ListAPIView** that is _Generic Class Based API View_. Also requires queryset and serializer class. Queryset is ordered by from approved requests to pending to approve. Additionally were used filter methods. Firstly specified what backend filter to use then according to what filter the view (In our case **'is_approved'** field).

```
class LeaveListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = LeaveRequest.objects.order_by('-is_approved')
    serializer_class = LeaveRequestSerializerForAdmin
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['is_approved']
```

### Approve Leave Request

To approve Leave Requests from employees' was used **update** method. Only work that should be done was to update. Different serializers for admin and employee as admin can access to **'is_approved'**.

```
class LeaveRequestEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LeaveRequestSerializerForAdmin
    queryset = LeaveRequest.objects.all()
```

# For Employee

**Every class based view contains attribute `permission_classes = [IsAuthenticated]` to restrict CRUD methods for anonymouses and others except current employee and admin**

## List of all Leave Reuqests

Used _Generic Class API Views_ to read the Leave Requests instances. Required attributes: queryset and serializer_class. For the queryset logged in employee must have list of all **HIS** requests, that is why queryset must be filtered. Created method to filter instances by logged in user and getting that employee's requests.

```
class EmployeeLeaveRequestCreateView(generics.ListCreateAPIView):
    serializer_class = EmployeeLeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LeaveRequest.objects.filter(employee = self.request.user)
```

## Create Leave Reuqest

Used same class taht were used to read list of all requests as _Generic Class API Views_ that we used **ListCreateAPIView**. During creating request it must automatically fill employee with current user(publisher) that is why **create** method was overwritten.

```
class EmployeeLeaveRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveRequest
        exclude = ['is_approved']

    employee = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        validated_data['employee'] = self.context['request'].user
        return LeaveRequest.objects.create(**validated_data)
```
# Logout API
Url **127.0.0.1:8000/api/logout/** for logging out