from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from datetime import datetime
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Logged in Successfully as ' + request.user.username)
                return redirect('Tenants:index')
            else:
                messages.warning(request, 'Account not activated')
                return render(request, 'Tenants/login.html')
        else:
            messages.warning(request, 'Invalid Username or Password!')
            return render(request, 'Tenants/login.html')
    return render(request, 'Tenants/login.html')


def logout_user(request):
    logout(request)
    form = UserLogForm(request.POST or None)
    context = {
        'form': form
    }
    messages.success(request, 'Successfully Logged out.')
    return redirect('Tenants:login_user')


def register_caretaker(request):
    if request.method == 'GET':
        form = CaretakerForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'Tenants/register_caretaker.html', context)

    if request.method == 'POST':
        form = CaretakerForm(request.POST or None)
        first_name = form.data['first_name']
        sur_name = form.data['sur_name']
        last_name = form.data['last_name']
        phone = form.data['phone']
        gender = form.data['gender']
        id_number = form.data['id_number']
        email = form.data['email']
        location = form.data['location']

        Caretaker.objects.create(
            first_name=first_name,
            sur_name=sur_name,
            last_name=last_name,
            id_number=id_number,
            gender=gender,
            email=email,
            contact=phone,
            location=location,
        )
        messages.success(request, 'Caretaker created successfully')
        return redirect('Tenants:index')


def caretaker_list(request):
    all_caretakers = Caretaker.objects.all()
    context = {
        'all_caretakers': all_caretakers,
    }
    return render(request, 'Tenants/caretaker_list.html', context)


def delete_caretaker(request, pk):
    caretaker = Caretaker.objects.get(id=pk)
    caretaker.delete()
    messages.success(request, 'Record deleted successfully.')
    return redirect('Tenants:caretaker_list')


def index(request):
    # form = TenantRegistrationForm(request.POST or None)
    # if request.method == 'POST':
    #     form = TenantRegistrationForm(request.POST or None)
    #     if form.is_valid():
    #
    #         form.save()
    #         return redirect('Tenants:index')
    # context = {
    #     'form': form,
    # }
    propeties = Apartment.objects.all().count()
    units = House.objects.all().count()
    tenants = Tenant.objects.all().count()
    leases = Lease.objects.filter(current_status=True).count()

    context = {
        'propeties': propeties,
        'units': units,
        'tenants': tenants,
        'leases': leases,
    }
    return render(request, 'Tenants/dashboard.html', context)


def register_tenant(request):
    if request.method == 'GET':
        form = TenantRegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'Tenants/register_tenant.html', context)
    if request.method == 'POST':
        form = TenantRegistrationForm(request.POST or None)
        first_name = form.data['first_name']
        sur_name = form.data['sur_name']
        last_name = form.data['last_name']
        phone = form.data['phone']
        gender = form.data['gender']
        id_number = form.data['id_number']
        email = form.data['email']

        Tenant.objects.create(
            first_name=first_name,
            sur_name=sur_name,
            last_name=last_name,
            id_number=id_number,
            gender=gender,
            email=email,
            contact=phone
        )
        messages.success(request, 'Tenant created successfully')
        return redirect('Tenants:index')


def tenants_list(request):
    all_tenants = Tenant.objects.all()
    context = {
        'all_tenants': all_tenants,
    }
    return render(request, 'Tenants/tenants_list.html', context)


def tenant_details(request, pk):
    tenant = Tenant.objects.get(id=pk)
    all_leases = Lease.objects.filter(tenant=pk)
    all_invoices = Invoice.objects.filter(tenant=pk)
    context = {
        'tenant': tenant,
        'all_leases': all_leases,
        'all_invoices': all_invoices,
    }
    return render(request, 'Tenants/tenant_details.html', context)


def all_apartments(request):
    all_apartments_qs = Apartment.objects.all()
    context = {
        'all_apartments_qs': all_apartments_qs
    }
    return render(request, 'Tenants/all_apartments.html', context)


def all_houses(request):
    all_houses_qs = House.objects.all()
    context = {
        'all_houses_qs': all_houses_qs,
    }
    return render(request, 'Tenants/houses_list.html', context)


def house_details(request, pk):
    house = House.objects.get(id=pk)
    active_lease = Lease.objects.filter(house_id=pk, current_status=True)
    terminated_leases = Lease.objects.filter(house_id=pk, current_status=False)
    context = {
        'house': house,
        'active_leases': active_lease,
        'terminated_leases': terminated_leases,
    }
    return render(request, 'Tenants/house_details.html', context)


def load_houses(request):
    apartment_id = request.GET.get('apartment')
    houses = House.objects.filter(apartment_id=apartment_id, vacant=True)
    context = {
        'houses': houses,
    }
    return render(request, 'Tenants/house_dropdown.html', context)


def payment_houses(request):
    apartment_id = request.GET.get('apartment')
    houses = House.objects.filter(apartment_id=apartment_id, vacant=False)
    context = {
        'houses': houses,
    }
    return render(request, 'Tenants/house_dropdown.html', context)


def rent_payment(request):
    if request.method == 'GET':
        form = PayRentForm(request.POST or None)
        context = {
            'form': form,
        }

        return render(request, 'Tenants/pay_rent.html', context)

    if request.method == 'POST':
        form = PayRentForm(request.POST or None)
        if form.is_valid():
            payment = form.save(commit=False)
            house_object = payment.house
            amount_paid = payment.amount_paid
            lease_object = Lease.objects.filter(house=house_object, current_status=True).first()
            lease_object.running_balance = lease_object.running_balance - amount_paid
            lease_object.save()
            payment.save()
            messages.success(request, 'Payment made successfully.')
            return redirect('Tenants:index')
        else:
            print(request.POST)
            print(form.errors)
            messages.warning(request, 'Form invalid')
            return redirect('Tenants:rent_payment')


def pay_invoice(request, pk):
    if request.method == 'POST':
        invoice_object = Invoice.objects.get(id=pk)

        leases_id = invoice_object.lease.id
        all_invoices_objects = Invoice.objects.filter(lease_id=leases_id)
        print(all_invoices_objects)
        amount_incurred = invoice_object.amount_incurred
        amount_due = invoice_object.lease.running_balance
        amount_paid = request.POST['amount_paid']
        date_paid = request.POST['date_paid']
        apartment = invoice_object.apartment
        house = invoice_object.house
        tenant = invoice_object.tenant
        lease = invoice_object.lease
        payment_for = invoice_object.date_generated

        # create Payment record

        # PaidRent.objects.create(
        #     apartment=apartment,
        #     house=house,
        #     amount_paid=amount_paid,
        #     date_paid=date_paid
        # )
        rent_pay = PaidRent(
            apartment=apartment,
            house=house,
            amount_paid=amount_paid,
            lease=lease,
            date_paid=date_paid,
            payment_for=payment_for,
            tenant=tenant,
        )
        rent_pay.save()
        # update invoice objects
        invoice_object.amount_paid = float(amount_paid) + invoice_object.amount_paid
        invoice_object.date_paid = date_paid
        invoice_object.lease.running_balance = invoice_object.lease.running_balance - float(amount_paid)

        invoice_object.amount_due = invoice_object.amount_due - float(amount_paid)
        if invoice_object.amount_due <= 0:
            invoice_object.fully_paid = True
            invoice_object.save()
        invoice_object.save()
        invoice_object.lease.save()

        for each_item in all_invoices_objects:
            if float(each_item.amount_due) > float(each_item.amount_incurred):
                each_item.amount_due = float(each_item.amount_due) - float(amount_paid)
                each_item.save()
            if float(each_item.previous_over_dues) > 0:
                each_item.previous_over_dues = each_item.previous_over_dues - float(amount_paid)
                each_item.save()
        messages.success(request, 'Invoice paid successfully.')
        return redirect('Tenants:invoice_list', pk=leases_id)


def register_lease(request):
    if request.method == 'GET':
        form = LeaseForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'Tenants/register_lease.html', context)

    if request.method == 'POST':
        form = LeaseForm(request.POST or None, request.FILES or None)

        #  apartment = form.data['apartment'],
        #  house = form.data['house']
        #  house = House.objects.get(pk=house)
        #  tenant = form.data['tenant']
        #  tenant = Tenant.objects.get(pk=tenant)
        #  lease_end_date = form.data['lease_end_date']
        #  lease_documents = request.FILES['lease_documents']
        #  current_status = request.POST.get('current_status', False)
        #  if current_status == 'on':
        #      current_status = True
        #  else:
        #      current_status == False

        #  Lease.objects.create(
        #      apartment=apartment,
        #      house=house,
        #      tenant=tenant,
        #      lease_end_date=lease_end_date,
        #      lease_documents=lease_documents,
        #      current_status=current_status,
        #  )
        if form.is_valid():
            lease = form.save(commit=False)
            house = lease.house.id

            lease.lease_documents = request.FILES['lease_documents']
            selected_house = House.objects.get(id=house)
            print(selected_house)
            selected_house.vacant = False
            lease.apartment.available_rooms -= 1
            lease.apartment.save()
            selected_house.save()
            house_object = House.objects.get(id=house)
            rent = house_object.rent
            lease.running_balance = rent

            lease.save()
            lease_object = Lease.objects.filter(house=house_object, current_status=True).first()
            tenant_object = lease_object.tenant
            # generate first invoice.
            apartment = lease.apartment
            amount_incurred = lease.house.rent
            date_generated = datetime.now()

            Invoice.objects.create(
                apartment=apartment,
                house=selected_house,
                lease=lease_object,
                tenant=tenant_object,
                amount_incurred=amount_incurred,
                amount_due=amount_incurred,
                date_generated=date_generated,
                previous_over_dues=0,
            )

            messages.success(request, 'Lease created successfully.')
            return redirect('Tenants:index')
        else:
            print(request.POST)
            print(form.errors)
            messages.warning(request, 'The form is invalid. Please retry.')
            return redirect('Tenants:register_lease')


def invoice_list(request, pk):
    all_invoices = Invoice.objects.filter(lease=pk).order_by('-date_generated')
    all_payments = PaidRent.objects.filter(lease=pk).order_by('-payment_for', '-date_paid')

    context = {
        'all_invoices': all_invoices,
        'my_lease_pk': pk,
        'all_payments': all_payments,
    }

    return render(request, 'Tenants/Invoice_list.html', context)


def active_lease(request):
    all_active_leases = Lease.objects.filter(current_status=True)
    all_terminated_leases = Lease.objects.filter(current_status=False)
    context = {
        'all_active_leases': all_active_leases,
        'all_terminated_leases': all_terminated_leases,
    }
    return render(request, 'Tenants/active_leases.html', context)


def leases_list(request):
    all_active_leases = Lease.objects.filter(current_status=True)
    all_terminated_leases = Lease.objects.filter(current_status=False)

    context = {
        'all_active_leases': all_active_leases,
        'all_terminated_leases': all_terminated_leases,
    }
    return render(request, 'Tenants/leases_list.html', context)


def terminate_lease(request, pk):
    house = House.objects.get(id=pk)
    lease = Lease.objects.filter(house_id=pk, current_status=True).first()
    if lease:
        lease.current_status = False
        lease.save()

        house.vacant = True
        lease.apartment.available_rooms += 1
        lease.apartment.save()
        house.save()
        messages.success(request, 'The Lease has been terminated successfully.')
        return redirect('Tenants:index')
    else:
        messages.warning(request, 'Unit has not associated lease.')
        return redirect('Tenants:index')


def register_apartments(request):
    if request.method == 'GET':
        form = ApartmentRegistrationForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'Tenants/register_apartments.html', context)

    if request.method == 'POST':
        print(request.POST)
        form = ApartmentRegistrationForm(
            request.POST or None, request.FILES or None)

        apartment_name = form.data['apartment_name']
        location = form.data['town']
        payment_plan = form.data['payment_plan']
        auto_house_id = request.POST.get('auto_house_id', False)
        caretaker_id = form.data['caretaker']
        caretaker = Caretaker.objects.get(pk=caretaker_id)
        description = form.data['description']
        city = form.data['city']
        state = form.data['street']
        postal_code = form.data['postal_code']
        agency_comission = form.data['agency_comission']
        # logic starts here.
        single_units = form.data['single']
        bed_sitter = form.data['bed_sitters']
        one_bedroom = form.data['One_Bedroom']
        single_rent = form.data['single_rent']
        bed_sitters_rent = form.data['bed_sitters_rent']
        one_bedroom_rent = form.data['One_Bedroom_rent']
        air_conditioner = request.POST.get('air_conditioner', False)
        if air_conditioner == 'on':
            air_conditioner = True
        car_parking = request.POST.get('car_parking', False)
        if car_parking == 'on':
            car_parking = True
        laundry_room = request.POST.get('laundry_room', False)
        if laundry_room == 'on':
            laundry_room = True

        heater = request.POST.get('heater', False)
        if heater == 'on':
            heater = True
        balcony = request.POST.get('balcony', False)
        if balcony == 'on':
            balcony = True
        gym = request.POST.get('gym', False)
        if gym == 'on':
            gym = True
        internet = request.POST.get('internet', False)
        if internet == 'on':
            internet = True
        garden = request.POST.get('garden', False)
        if garden == 'on':
            garden = True
        alarm = request.POST.get('alarm', False)
        if alarm == 'on':
            alarm = True
        picture = request.FILES['property_image']

        total_units = int(single_units) + int(bed_sitter) + int(one_bedroom)
        default_house_type = ''

        if int(single_units) > 0 and int(bed_sitter) == 0 and int(one_bedroom) == 0:
            default_house_type = 'Single'
        elif int(single_units) > 0 and int(bed_sitter) > 0 and int(one_bedroom) == 0:
            default_house_type = 'Single, Bed-Sitter'
        elif int(single_units) > 0 and int(bed_sitter) > 0 and int(one_bedroom) > 0:
            default_house_type = 'Single, Bed-Sitter, One-Bedroom'
        try:
            apartment_name_validation = Apartment.objects.get(
                apartment_name=apartment_name)
            if apartment_name_validation:
                messages.warning(
                    request, 'Sorry Apartment with that name exists.')
                return redirect('Tenants:register_apartments')
        except ObjectDoesNotExist:
            pass
        n = Apartment.objects.create(
            apartment_name=apartment_name,
            location=location,
            city=city,
            state=state,
            post_code=postal_code,
            caretaker=caretaker,
            payment_plan=payment_plan,
            description=description,
            units=int(total_units),
            available_rooms=int(total_units),
            default_house_type=default_house_type,
            agency_commission=agency_comission,
            apartment_image=picture,
            air_conditioners=air_conditioner,
            car_parking=car_parking,
            laundry_room=laundry_room,
            heaters=heater,
            balcony=balcony,
            gym=gym,
            internet=internet,
            garden=garden,
            alarm=alarm,
        )
        # create the houses
        single_loops = int(single_units)
        bed_sitter_loops = int(bed_sitter)
        one_bedroom_loops = int(one_bedroom)
        apartment_loop = Apartment.objects.get(pk=n.id)

        # single_loop
        if auto_house_id:
            for i in range(1, single_loops + 1):
                House.objects.create(
                    apartment=apartment_loop,
                    house_code=i,
                    rent=single_rent,
                    deposit=single_rent,
                    house_type='Single',
                )
        else:
            for i in range(1, single_loops + 1):
                House.objects.create(
                    apartment=apartment_loop,
                    rent=single_rent,
                    deposit=single_rent,
                    house_type='Single',
                )
        if auto_house_id:
            for i in range(single_loops + 1, single_loops + 1 + bed_sitter_loops):
                House.objects.create(
                    apartment=apartment_loop,
                    house_code=i,
                    rent=bed_sitters_rent,
                    deposit=bed_sitters_rent,
                    house_type='Bed-Sitter',
                )

        else:
            for i in range(0, bed_sitter_loops):
                House.objects.create(
                    apartment=apartment_loop,
                    rent=bed_sitters_rent,
                    deposit=bed_sitters_rent,
                    house_type='Bed-Sitter',
                )
        if auto_house_id:
            for i in range(single_loops + 1 + bed_sitter_loops,
                           single_loops + 1 + bed_sitter_loops + one_bedroom_loops):
                House.objects.create(
                    apartment=apartment_loop,
                    house_code=i,
                    rent=one_bedroom_rent,
                    deposit=one_bedroom_rent,
                    house_type='One Bedroom',
                )
        else:
            for i in range(0, one_bedroom_loops):
                House.objects.create(
                    apartment=apartment_loop,
                    rent=one_bedroom_rent,
                    deposit=one_bedroom_rent,
                    house_type='One Bedroom',
                )

        print(request.POST)
        messages.success(request, 'Success')
        return redirect('Tenants:index')


def apartment_list(request):
    all_apartments_qs = Apartment.objects.all()
    context = {
        'all_apartments_qs': all_apartments_qs
    }
    return render(request, 'Tenants/apartment_list.html', context)


def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, id=pk)
    apartment_houses = apartment.house_set.all()
    active_apartment_leases = Lease.objects.filter(apartment_id=pk, current_status=True)
    terminated_apartment_leases = Lease.objects.filter(apartment_id=pk, current_status=False)
    context = {
        'apartment': apartment,
        'apartment_houses': apartment_houses,
        'active_apartment_leases': active_apartment_leases,
        'terminated_apartment_leases': terminated_apartment_leases,
    }
    return render(request, 'Tenants/apartment_details.html', context)


def invoice_template(request, my_lease_pk, pk):
    invoice = Invoice.objects.get(id=pk)
    generation_date = invoice.date_generated
    gmonth = generation_date.month

    invoice_lease_id = invoice.lease.id
    invoice_count = Invoice.objects.filter(lease_id=invoice_lease_id).count()
    if invoice_count > 1:
        over_due = invoice.lease.running_balance - invoice.amount_incurred
    else:
        over_due = 0

    context = {
        'invoice': invoice,
        'gmonth': gmonth,
        'over_due': over_due,
        'ipk': my_lease_pk,
    }
    return render(request, 'Tenants/invoice_template.html', context)


def generate_invoices(request):
    if request.method == 'GET':
        form = InvoiceForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'Tenants/generate_invoice.html', context)

    if request.method == 'POST':
        form = InvoiceForm(request.POST or None)
        date_generated = form.data['date_generated']

        active_leases = Lease.objects.filter(current_status=True)
        print(active_leases)
        for lease_object in active_leases:
            print(lease_object)
            apartment = lease_object.apartment
            house = lease_object.house
            tenant = lease_object.tenant
            lease = lease_object
            amount_due = lease_object.running_balance + lease_object.house.rent
            amount_incurred = lease_object.house.rent
            previous_over_dues = lease_object.running_balance
            date_generated = date_generated

            if previous_over_dues < -amount_incurred:
                fully_paid = True
            else:
                fully_paid = False

            invoice_loop = Invoice(

                apartment=apartment,
                house=house,
                tenant=tenant,
                lease=lease,
                amount_due=amount_due,
                amount_incurred=amount_incurred,
                previous_over_dues=previous_over_dues,
                date_generated=date_generated,
                fully_paid=fully_paid,
            )
            invoice_loop.save()

            # Invoice.objects.create(
            #     apartment=apartment,
            #     house=house,
            #     tenant=tenant,
            #     lease=lease,
            #     amount_incurred=amount_incurred,
            #     date_generated=date_generated,
            #
            # )
            #
            lease.running_balance = lease.running_balance + lease.house.rent
            lease.save()
        messages.success(request, 'Invoices created successfully')
        return redirect('Tenants:active_leases')


# api functions


@api_view(['GET'])
def apartment_list_view(request):
    all_apartments_qs = Apartment.objects.all()
    serializer = ApartmentSerializer(all_apartments_qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def apartment_detail_view(request, pk):
    apartment = Apartment.objects.get(id=pk)
    serializer = ApartmentSerializer(apartment, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def caretakers_list_view(request):
    all_caretakers = Caretaker.objects.all()
    serializer = CaretakerSerializer(all_caretakers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def caretaker_detail_view(request, pk):
    caretaker = Caretaker.objects.get(id=pk)
    serializer = CaretakerSerializer(caretaker, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def house_list_view(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    all_houses_qs = apartment.apartment.house_set.all()
    serializer = HouseSerializer(all_houses_qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def house_detail_view(request, pk):
    house = House.objects.get(id=pk)
    serializer = HouseSerializer(house, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_apartment(request):
    serializer = ApartmentSerializer(data=request.data)

    apartment_name = serializer.initial_data['apartment_name']
    location = serializer.initial_data['location']
    payment_plan = serializer.initial_data['payment_plan']
    caretaker_id = serializer.initial_data['caretaker']
    auto_house_id = serializer.initial_data.get('auto_house_id', False)
    # look up for caretaker instance
    caretaker = Caretaker.objects.get(pk=caretaker_id)
    description = serializer.initial_data['description']
    # logic starts here.
    single_units = serializer.initial_data['single']
    bed_sitter = serializer.initial_data['bed_sitters']
    one_bedroom = serializer.initial_data['One_Bedroom']
    total_units = int(single_units) + int(bed_sitter) + int(one_bedroom)
    default_house_type = ''

    if int(single_units) > 0 and int(bed_sitter) == 0 and int(one_bedroom) == 0:
        default_house_type = 'Single'
    elif int(single_units) > 0 and int(bed_sitter) > 0 and int(one_bedroom) == 0:
        default_house_type = 'Single, Bed-Sitter'
    elif int(single_units) > 0 and int(bed_sitter) > 0 and int(one_bedroom) > 0:
        default_house_type = 'Single, Bed-Sitter, One-Bedroom'

    try:
        apartment_name_validation = Apartment.objects.get(
            apartment_name=apartment_name)
        if apartment_name_validation:
            messages.warning(request, 'Sorry Apartment with that name exists.')
            return redirect('Tenants:register_apartments')
    except ObjectDoesNotExist:
        pass
    n = Apartment.objects.create(
        apartment_name=apartment_name,
        location=location,
        payment_plan=payment_plan,
        caretaker=caretaker,
        description=description,
        units=int(total_units),
        available_rooms=int(total_units),
        default_house_type=default_house_type
    )
    # create the houses
    single_loops = int(single_units)
    bed_sitter_loops = int(bed_sitter)
    one_bedroom_loops = int(one_bedroom)
    apartment_loop = Apartment.objects.get(pk=n.id)

    # single_loop
    if auto_house_id:
        for i in range(1, single_loops + 1):
            House.objects.create(
                apartment=apartment_loop,
                house_code=i,
                house_type='Single',
            )
    else:
        for i in range(1, single_loops + 1):
            House.objects.create(
                apartment=apartment_loop,
                house_type='Single',
            )
    # bed sitter loop
    if auto_house_id:
        for i in range(single_loops + 1, single_loops + 1 + bed_sitter_loops):
            House.objects.create(
                apartment=apartment_loop,
                house_code=i,
                house_type='Bed-Sitter',
            )

    else:
        for i in range(0, bed_sitter_loops):
            House.objects.create(
                apartment=apartment_loop,
                house_type='Bed-Sitter',
            )

    # one bedroom loop
    if auto_house_id:
        for i in range(single_loops + 1 + bed_sitter_loops, single_loops + 1 + bed_sitter_loops + one_bedroom_loops):
            House.objects.create(
                apartment=apartment_loop,
                house_code=i,
                house_type='One Bedroom',
            )
    else:
        for i in range(0, one_bedroom_loops):
            House.objects.create(
                apartment=apartment_loop,
                house_type='One Bedroom',
            )
    # end of the loops
    serializer.is_valid()
    return Response(serializer.data)


@api_view(['POST'])
def create_caretaker(request):
    serializer = CaretakerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
