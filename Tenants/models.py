from django.db import models

Gender_Choices = (
    ('Female', 'Female'),
    ('Male', 'Male'),
)

House_Choices = (
    ('Single', 'Single'),
    ('Bed-Sitter', 'Bed-Sitter'),
    ('One Bedroom', 'One Bedroom'),
    ('Two Bedroom', 'Two Bedroom'),
    ('Three Bedroom', 'Three Bedroom'),
    ('Four Bedroom', 'Four Bedroom'),
)
PaymentPlans = (
    ('Monthly', 'Monthly'),
    ('Per Semester', 'Per Semester'),
)


class Caretaker(models.Model):
    first_name = models.CharField(max_length=100)
    sur_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender_Choices, blank=True)
    email = models.EmailField()
    contact = models.IntegerField()
    location = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Caretaker'
        verbose_name_plural = 'Caretakers'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Apartment(models.Model):
    apartment_name = models.CharField(max_length=500, unique=True)
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=300, blank=True, null=True)
    state = models.CharField(max_length=300, blank=True, null=True)
    post_code = models.CharField(max_length=300, blank=True, null=True)
    units = models.IntegerField()
    available_rooms = models.IntegerField()
    payment_plan = models.CharField(max_length=100, choices=PaymentPlans)
    caretaker = models.ForeignKey(Caretaker, on_delete=models.DO_NOTHING)
    default_house_type = models.CharField(max_length=100, choices=House_Choices)
    description = models.TextField(max_length=2000)
    agency_commission = models.FloatField()
    auto_house_id = models.BooleanField(default=True)
    apartment_image = models.ImageField(blank=True, null=True)
    air_conditioners = models.BooleanField(default=False)
    car_parking = models.BooleanField(default=False)
    laundry_room = models.BooleanField(default=False)
    heaters = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    garden = models.BooleanField(default=False)
    alarm = models.BooleanField(default=False)

    def __str__(self):
        return self.apartment_name


class House(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    house_code = models.CharField(max_length=1000, blank=True, null=True)
    house_type = models.CharField(max_length=200, choices=House_Choices)
    rent = models.IntegerField(default=0)
    deposit = models.IntegerField(default=0)
    arrears = models.IntegerField(default=0)
    vacant = models.BooleanField(default=True)
    house_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.house_code)


class HouseType(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class Tenant(models.Model):
    first_name = models.CharField(max_length=100)
    sur_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender_Choices, blank=True)
    email = models.EmailField()
    contact = models.IntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.sur_name + ' ' + self.last_name


class Lease(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease_start_date = models.DateField(auto_now_add=True)
    lease_end_date = models.DateField()
    lease_documents = models.FileField(blank=True, null=True)
    current_status = models.BooleanField(default=False)
    running_balance = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class PaidRent(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, blank=True, null=True)
    amount_paid = models.FloatField()
    payment_for = models.DateField(blank=True, null=True)
    date_paid = models.DateField()

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    amount_incurred = models.FloatField(default=0)
    fully_paid = models.BooleanField(default=False)
    date_generated = models.DateField()
    amount_paid = models.FloatField(default=0, blank=True, null=True)
    amount_due = models.FloatField(default=0, blank=True, null=True)
    previous_over_dues = models.FloatField(default=0, blank=True, null=True)
    date_paid = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
    















# def create_houses(sender, instance, created, **kwargs):
#     if created:
#         loops = instance.units
#         for i in range(0, loops):
#             House.objects.create(
#                 apartment=instance,
#                 house_type=instance.default_house_type,
#             )
#
#
# post_save.connect(create_houses, sender=Apartment)

