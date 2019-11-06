from django.db import models
from multiselectfield import MultiSelectField


class EmployeeApplication(models.Model):
    name = models.CharField(max_length=50)
    employee_number = models.CharField(max_length=12,null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank= True)
    pic_url = models.CharField(max_length=1000, null=True, blank=True)
    post_applied_for = models.CharField(max_length=300)


class PersonalDetails(models.Model):
    sex_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    )
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    caste = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    sex = models.CharField(max_length=6, choices=sex_choices, default='male')


class Address(models.Model):
    select_address_type = (
        ('current', 'Address For Communication'),
        ('permanent', 'Permanent Address')
    )
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=13)
    address_type = models.CharField(max_length=25, choices=select_address_type, default='current')
    rented = models.BooleanField(null=True, blank=True)


class Language(models.Model):
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    speak = models.BooleanField(default=False)
    mother_tongue = models.BooleanField(default=False)


class EmergencyContacts(models.Model):
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    address = models.TextField()


class BankDetails(models.Model):
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    pan = models.CharField(max_length=15, null=True, blank=True)
    bank_name = models.CharField(max_length=60, null=True, blank=True)
    account_name = models.CharField(max_length=16, null=True, blank=True)
    branch = models.CharField(max_length=60, null=True, blank=True)
    ifsc = models.CharField(max_length=10, null=True, blank=True)


class AdditionalInfo(models.Model):
    house_choice = (
        ('rented', 'Rented'),
        ('own', 'Own')
    )
    drving_vehicle = (
        ('two_wheeler', 'Two Wheeler'),
        ('four_wheeler', 'Four Wheeler'),
        ('none', 'None')
    )
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    is_your_house = models.CharField(max_length=6, choices=house_choice)
    driving = models.CharField(max_length=12, choices=drving_vehicle)
    passport = models.BooleanField(default=False)
    passport_valid_upto = models.DateField(null=True, blank=True)
    married = models.BooleanField(default=False)
    date_of_marraige = models.DateField(null=True, blank=True)
    training_attended = models.TextField(null=True,blank=True)


class HealthHistory(models.Model):
    DISEASE_CHOICE = (
        ('respiratory_disorder','Respiratory Disorder'),
        ('heart_disease','Heart Disease'),
        ('blood_pressure','Blood Pressure'),
        ('diabetes', 'Diabetes'),
        ('asthma', 'Asthma'),
        ('tuberculosis', 'Tuberculosis'),
        ('others', 'Others'),
        ('none', 'None')
    )
    ALIMENTS_CHOICE = (
        ('malaria', 'Malaria'),
        ('jaundice', 'Jaundice'),
        ('hernia', 'Hernia'),
        ('piles', 'Piles'),
        ('liver_ailments', 'Liver ailments'),
        ('back_pain', 'Back Pain'),
        ('others', 'Others'),
        ('none', 'None')
    )

    CHEWING_CHOICE = (
        ('tobacco', 'Tobacco'),
        ('paan', 'Paan'),
        ('others', 'Others'),
        ('none', 'None')
    )
    LIQUOR_CONSUMPTION = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('occasionally', 'Occasionally')
    )

    EXERCISE_CHOICES =(
        ('jogging', 'Jogging'),
        ('running', 'Running'),
        ('gym', 'Gym'),
        ('walking', 'Walking'),
        ('others', 'Others'),
        ('none', 'None')
    )
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3)
    allergies = models.CharField(max_length=200)
    spectacles = models.BooleanField()
    right_eye_power = models.CharField(max_length=5, null=True, blank=True)
    left_eye_power = models.CharField(max_length=5, null=True, blank=True)
    suffer_from = models.CharField(max_length=20, choices=DISEASE_CHOICE)
    disease_others = models.CharField(max_length=100,null=True,blank=True)
    past_aliments = models.CharField(max_length=20, choices=ALIMENTS_CHOICE)
    aliments_others = models.CharField(max_length=100,null=True,blank=True)
    accident_in_past = models.CharField(max_length=200)
    surgery_in_past = models.CharField(max_length=200)
    smoke = models.BooleanField()
    cigrate_per_day = models.PositiveSmallIntegerField(null=True, blank=True)
    chewing = models.CharField(max_length=20, choices=CHEWING_CHOICE)
    chewing_others = models.CharField(max_length=100,null=True,blank=True)
    liquor = models.BooleanField()
    liquor_habit = models.CharField(max_length=20, choices=LIQUOR_CONSUMPTION, null=True, blank=True)
    exercise = MultiSelectField(choices=EXERCISE_CHOICES, default='none')
    exercise_other = models.CharField(max_length=100,null=True,blank=True)


class FamilyBackground(models.Model):
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    relation = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    qualification = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    dependent = models.BooleanField(default=False)


class EducationalHistory(models.Model):
    MARKS_CHOICE = (
        ('cgpa', 'CGPA'),
        ('percentage', 'Percentage')
    )
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institute = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    exam_passed = models.CharField(max_length=50, null=True, blank=True)
    special_subject = models.CharField(max_length=100)
    marks_type = models.CharField(max_length=20, choices=MARKS_CHOICE)
    marks = models.CharField(max_length=3)


class EmployementHistory(models.Model):

    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    destination = models.CharField(max_length=50, null=True, blank=True)
    functions = models.CharField(max_length=100)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=3)
    reason_for_leaving = models.TextField()


class LatestEmployement(models.Model):
    SELECT_REFERENCE = (
        ('reporting_manager', 'Reporting Manager'),
        ('reference1', 'Reference 1'),
        ('reference2', 'Reference 2')
    )
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    position = models.CharField(max_length=20, choices=SELECT_REFERENCE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    official_email = models.CharField(max_length=100)


class OtherInformation(models.Model):
    EXTRACURRICULAR_ACTIVITIES_CHOICES = (
        ('cinema', 'Cinema'),
        ('tv', 'TV'),
        ('reading_books', 'Reading Books'),
        ('music', 'Music'),
        ('stamp_collection', 'Stamp Collection'),
        ('social_services', 'Social Service'),
        ('sports', 'Sports'),
        ('others', 'Others')
    )
    employee_application = models.OneToOneField(EmployeeApplication, on_delete=models.CASCADE)
    previous_interview_with_us = models.BooleanField(default=False)
    previous_interview_position = models.CharField(max_length=50, null=True, blank=True)
    previous_interview_date = models.DateField(null=True, blank=True)
    job_responsibility = models.CharField(max_length=300)
    relative_in_company = models.BooleanField(default=False)
    relative_details = models.TextField(null=True, blank=True)
    how_did_you_know_about_vacancy = models.CharField(max_length=100)
    court_case_old = models.BooleanField(default=False)
    court_case_old_details = models.TextField(null=True, blank=True)
    court_case_current = models.BooleanField(default=False)
    court_case_current_details = models.TextField(null=True, blank=True)
    extracurricular_activities = models.CharField(max_length=20, choices=EXTRACURRICULAR_ACTIVITIES_CHOICES)
    extracurricular_activities_others = models.CharField(max_length=100, null=True, blank=True)








