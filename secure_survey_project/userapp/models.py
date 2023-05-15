from django.db import models


class User(models.Model):
    GENDER_CHOICES = [
        (2, 'female'),
        (3, 'male'),
    ]

    AGE_CHOICES = [
        (2, '10s'),
        (3, '20s'),
        (4, '30s'),
        (5, '40s'),
        (6, '50s'),
        (7, '60s'),
        (8, '70s'),
        (9, '80s'),
        (10, '90s'),
    ]

    MARRIAGE_CHOICES = [
        (2, 'married'),
        (3, 'single'),
        (4, 'divorce'),
        (5, 'deceased'),
    ]

    INCOME_CHOICES = [
        (2, '-1000'),
        (3, '1000-3000'),
        (4, '3000-5000'),
        (5, '5000-7000'),
        (6, '7000-10000'),
        (7, '10000-'),
    ]

    EDUCATION_CHOICES = [
        (2, 'middle school'),
        (3, 'high school'),
        (4, 'bachelor'),
        (5, 'master'),
        (6, 'doctor'),
    ]

    JOB_CHOICES = [
        (2, 'public enterprise'),
        (3, 'teacher'),
        (4, 'profession'),
        (5, 'managerial'),
        (6, 'office'),
        (7, 'production'),
        (8, 'service'),
        (9, 'student'),
    ]

    PHONE_CHOICES = [
        (2, 'feature phone'),
        (3, 'smartphone'),
        (4, 'both'),
        (5, 'not use'),
    ]

    PHONE_MAKER_CHOICES = [
        (2, 'Samsung'),
        (3, 'LG'),
        (4, 'Apple'),
    ]

    gender = models.IntegerField(choices=GENDER_CHOICES)
    age = models.IntegerField(choices=AGE_CHOICES)
    marriage = models.IntegerField(choices=MARRIAGE_CHOICES)
    income = models.IntegerField(choices=INCOME_CHOICES)
    education = models.IntegerField(choices=EDUCATION_CHOICES)
    job = models.IntegerField(choices=JOB_CHOICES)
    phone = models.IntegerField(choices=PHONE_CHOICES)
    phone_maker = models.IntegerField(choices=PHONE_MAKER_CHOICES)
    email = models.EmailField(max_length=254)
