from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# --------------------------
# 1️⃣ Stop Model
# --------------------------
class Stop(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


# --------------------------

# 2️⃣ Bus Model
# --------------------------
class Bus(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    bus_no = models.CharField(max_length=20, unique=True)
    stop = models.CharField(max_length=100)

    pickup_time = models.CharField(max_length=20, blank=True, null=True)
    drop_time = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.bus_no


# --------------------------
# 3️⃣ Enrollment Request Model
# --------------------------
class EnrollmentRequest(models.Model):
    ROLE_CHOICES = [('Employee', 'Employee'), ('Intern', 'Intern')]
    STATUS_CHOICES = [('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')]

    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/')
    dob = models.DateField()
    gender = models.CharField(max_length=20)
    email = models.EmailField( max_length=254)
    contact_no = models.CharField(max_length=15)
    alternate_no = models.CharField(max_length=15, blank=True, null=True)
    present_address = models.TextField()
    permanent_address = models.TextField()
    entity = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    emp_id = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    date_of_joining = models.DateField()
    pickup_drop_point = models.ForeignKey(Stop, on_delete=models.SET_NULL, null=True)
    working_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.status}"


# --------------------------
# 4️⃣ Exit Request Model
# --------------------------
class ExitRequest(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')]

    employee_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=20)
    contact_no = models.CharField(max_length=15)
    present_address = models.TextField()
    permanent_address = models.TextField()
    entity = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    date_of_leaving = models.DateField()
    pickup_drop_point = models.ForeignKey(Stop, on_delete=models.SET_NULL, null=True)
    bus_no = models.CharField(max_length=20)
    bus_pass_no = models.CharField(max_length=20)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.employee_name} - {self.status}"

class AdminUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=128)  # store hashed password
    full_name = models.CharField(max_length=100, blank=True, null=True)
    is_superadmin = models.BooleanField(default=False)  # main admin flag
    created_at = models.DateTimeField(default=timezone.now)

    

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.username
    
from django.db import models
from django.contrib.auth.models import User

class ActionLog(models.Model):
    action = models.TextField()
    performed_by = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.performed_by} - {self.action[:30]}"
