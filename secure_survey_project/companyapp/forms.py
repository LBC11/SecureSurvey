from django import forms
from django.forms import formset_factory


class PersonalConditionForm(forms.Form):

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

    gender = forms.MultipleChoiceField(choices=GENDER_CHOICES)
    age = forms.MultipleChoiceField(choices=AGE_CHOICES)
    marriage = forms.MultipleChoiceField(choices=MARRIAGE_CHOICES)
    income = forms.MultipleChoiceField(choices=INCOME_CHOICES)
    education = forms.MultipleChoiceField(choices=EDUCATION_CHOICES)
    job = forms.MultipleChoiceField(choices=JOB_CHOICES)
    phone = forms.MultipleChoiceField(choices=PHONE_CHOICES)
    phone_maker = forms.MultipleChoiceField(choices=PHONE_MAKER_CHOICES)
    email = forms.EmailField()


class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=1000)


QuestionFormset = formset_factory(QuestionForm, extra=1)
