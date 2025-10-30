from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import EnrollmentRequest, ExitRequest, Bus, Stop, AdminUser, ActionLog
from .forms import BusForm
from .models import Bus
from django.contrib import messages

# ---------------- Home / Employee Views ----------------
def home(request):
    buses = Bus.objects.filter(status='Active')
    return render(request, 'home.html', {'buses': buses})


def buses(request):
    """Employee-facing list of active buses (cards)"""
    buses = Bus.objects.filter(status='Active').select_related('stop').order_by('bus_no')
    return render(request, 'buses.html', {'buses': buses})




def enroll(request):
    stops = Stop.objects.all()
    if request.method == "POST":
        EnrollmentRequest.objects.create(
            name=request.POST['name'],
            photo=request.FILES['photo'],
            dob=request.POST['dob'],
            gender=request.POST['gender'],
            email=request.POST['email'],
            contact_no=request.POST['contact_no'],
            alternate_no=request.POST.get('alternate_no'),
            present_address=request.POST['present_address'],
            permanent_address=request.POST['permanent_address'],
            entity=request.POST['entity'],
            department=request.POST['department'],
            role=request.POST['role'],
            emp_id=request.POST.get('emp_id'),
            designation=request.POST.get('designation'),
            date_of_joining=request.POST['date_of_joining'],
            pickup_drop_point_id=request.POST['pickup_drop_point'],
            working_type=request.POST['working_type'],
        )
        messages.success(request, "Enrollment request submitted.")
        return redirect('home')
    return render(request, 'enroll.html', {'stops': stops})


def exit_view(request):
    stops = Stop.objects.all()
    if request.method == "POST":
        ExitRequest.objects.create(
            employee_name=request.POST['employee_name'],
            dob=request.POST['dob'],
            gender=request.POST['gender'],
            contact_no=request.POST['contact_no'],
            present_address=request.POST['present_address'],
            permanent_address=request.POST['permanent_address'],
            entity=request.POST['entity'],
            department=request.POST['department'],
            designation=request.POST['designation'],
            date_of_leaving=request.POST['date_of_leaving'],
            pickup_drop_point_id=request.POST['pickup_drop_point'],
            bus_no=request.POST['bus_no'],
            bus_pass_no=request.POST['bus_pass_no'],
            remarks=request.POST.get('remarks'),
        )
        messages.success(request, "Exit request submitted.")
        return redirect('home')
    return render(request, 'exit.html', {'stops': stops})


def buses_view(request):
    buses = Bus.objects.all().order_by('bus_no')
    return render(request, 'buses.html', {'buses': buses})


def rules(request):
    return render(request, 'rules.html')


# ---------------- Admin Views ----------------
def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Look up admin in database
        try:
            admin = AdminUser.objects.get(username=username)
        except AdminUser.DoesNotExist:
            messages.error(request, "Invalid credentials.")
            return render(request, 'admin_login.html')

        if admin.check_password(password):
            # login successful
            request.session['admin_id'] = admin.id  # save actual admin ID in session
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'admin_login.html')


def admin_logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('home')



def admin_dashboard(request):
    # Handle Bus Add Form (POST)
    if request.method == "POST":
        bus_no = request.POST.get("bus_no")
        stop = request.POST.get("stop").strip
        pickup_time = request.POST.get("pickup_time")
        drop_time = request.POST.get("drop_time")
        status = request.POST.get("status")

        try:
            stop, created = Stop.objects.get_or_create(name=stop)
            Bus.objects.create(
                bus_no=bus_no,
                stop=stop,
                pickup_time=pickup_time,
                drop_time=drop_time,
                status=status
            )
            messages.success(request, f"Bus {bus_no} added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding bus: {str(e)}")

        return redirect("admin_dashboard")

    # ✅ For GET request → show all data
    buses = Bus.objects.all()
    stops = Stop.objects.all()
    enrollment_requests = EnrollmentRequest.objects.filter(status='Pending')
    exit_requests = ExitRequest.objects.filter(status='Pending')

    return render(request, "admin_dashboard.html", {
        "buses": buses,
        "stops": stops,
        "enrollment_requests": enrollment_requests,
        "exit_requests": exit_requests,
    })


# -------- Enrollment/Exit Status Update --------
@require_POST
def update_enrollment_status(request, pk):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    req = get_object_or_404(EnrollmentRequest, pk=pk)
    status = request.POST.get('status')
    if status not in ('Pending', 'Accepted', 'Rejected'):
        messages.error(request, "Invalid status.")
        return redirect('admin_dashboard')
    req.status = status
    req.save()
    ActionLog.objects.create(action=f"Enrollment status updated for {req.name} to {status}", performed_by="Admin")
    messages.success(request, f"Enrollment for {req.name} set to {status}.")
    return redirect('admin_dashboard')


@require_POST
def update_exit_status(request, pk):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    req = get_object_or_404(ExitRequest, pk=pk)
    status = request.POST.get('status')
    if status not in ('Pending', 'Accepted', 'Rejected'):
        messages.error(request, "Invalid status.")
        return redirect('admin_dashboard')
    req.status = status
    req.save()
    ActionLog.objects.create(action=f"Exit status updated for {req.employee_name} to {status}", performed_by="Admin")
    messages.success(request, f"Exit request for {req.employee_name} set to {status}.")
    return redirect('admin_dashboard')


def edit_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    
    if request.method == 'POST':
        form = BusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus updated successfully!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Please fill all required fields correctly.")
    else:
        form = BusForm(instance=bus)

    return redirect('admin_dashboard')
   
def delete_bus(request, bus_id):
    if request.method == "POST":
        bus = get_object_or_404(Bus, id=bus_id)
        bus.delete()
        messages.success(request, f"Bus {bus.bus_no} deleted successfully!")
    else:
        messages.error(request, "Invalid request method for deleting bus.")
    return redirect("admin_dashboard")

# -------- Stop Management --------
def add_stop(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    if request.method == "POST":
        name = request.POST.get('name').strip()
        location = request.POST.get('location','').strip()
        if not name:
            messages.error(request, "Stop name required.")
            return redirect('admin_dashboard')
        Stop.objects.get_or_create(name=name, defaults={'location': location})
        messages.success(request, "Stop added successfully.")
    return redirect('admin_dashboard')


def edit_stop(request, pk):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    stop = get_object_or_404(Stop, pk=pk)
    if request.method == "POST":
        stop.name = request.POST.get('name').strip()
        stop.location = request.POST.get('location','').strip()
        stop.save()
        messages.success(request, "Stop updated successfully.")
    return redirect('admin_dashboard')


@require_POST
def delete_stop(request, pk):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    stop = get_object_or_404(Stop, pk=pk)
    stop.delete()
    messages.success(request, "Stop deleted successfully.")
    return redirect('admin_dashboard')


# -------- Logs --------
def view_logs(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    logs = ActionLog.objects.all().order_by('-timestamp')
    return render(request, 'logs.html', {'logs': logs})


# -------- AdminUser / Logins Management --------
def manage_logins(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    admins = AdminUser.objects.all().order_by('-created_at')
    return render(request, 'manage_logins.html', {'admins': admins})


def add_admin(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    if request.method == "POST":
        username = request.POST.get('username').strip()
        raw_password = request.POST.get('password')
        full_name = request.POST.get('full_name','').strip()
        is_super = True if request.POST.get('is_super') == 'on' else False
        if AdminUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('manage_logins')
        admin = AdminUser(username=username, full_name=full_name, is_superadmin=is_super)
        admin.set_password(raw_password)
        admin.save()
        messages.success(request, "Admin account created successfully.")
    return redirect('manage_logins')


def delete_admin(request, pk):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    admin = get_object_or_404(AdminUser, pk=pk)
    current = request.session.get('admin_id')
    if admin.username == current:
        messages.error(request, "Cannot delete currently logged-in admin.")
        return redirect('manage_logins')
    admin.delete()
    messages.success(request, "Admin deleted successfully.")
    return redirect('manage_logins')

# -------------------- BUS CRUD for Admin --------------------


def dashboard(request):
    buses = Bus.objects.all()
    return render(request, 'admin_dashboard.html', {'buses': buses})


def add_bus(request):
    if request.method == "POST":
        try:
            bus_number = request.POST.get('bus_number')
            route = request.POST.get('route')
            stop = request.POST.get('stop')
            capacity = request.POST.get('capacity')

            Bus.objects.create(
                bus_number=bus_number,
                route=route,
                stop=stop,
                capacity=capacity
            )

            messages.success(request, "Bus added successfully!")
            return redirect('admin_dashboard')

        except Exception as e:
            messages.error(request, f"Error adding bus: {e}")
            return redirect('admin_dashboard')


from django.core.mail import send_mail
from django.http import HttpResponse
def test_email(request):
    try:
        send_mail(
            subject="Test Email from Django",
            message="If you see this, email setup works!",
            from_email=None,
            recipient_list=["yourgmail@gmail.com"],  # send to yourself
            fail_silently=False,
        )
        return HttpResponse("✅ Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"❌ Error: {e}")

