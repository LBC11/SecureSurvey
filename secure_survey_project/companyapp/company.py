from serverapp.component import Network
from django.core.mail import send_mail
from userapp.models import PersonalEmail
from companyapp.models import Survey


class PersonalCondition:
    def __init__(self, form_data):
        self.gender = form_data.cleaned_data.get('gender')
        self.age = form_data.cleaned_data.get('age')
        self.marriage = form_data.cleaned_data.get('marriage')
        self.income = form_data.cleaned_data.get('income')
        self.education = form_data.cleaned_data.get('education')
        self.job = form_data.cleaned_data.get('job')
        self.phone = form_data.cleaned_data.get('phone')
        self.phone_maker = form_data.cleaned_data.get('phone_maker')

    def to_dict(self):
        return {0: self.gender,
                1: self.age,
                2: self.marriage,
                3: self.income,
                4: self.education,
                5: self.job,
                6: self.phone,
                7: self.phone_maker}


class Company():
    def __init__(self):
        self.personal_conditions = None

    def set_personal_conditions(self, personal_condition: PersonalCondition):
        self.personal_conditions = personal_condition

    def save_personal_conditions(self, network: Network):
        personal_conditions_dict = self.personal_conditions.to_dict()
        network.save_personal_conditions(personal_conditions_dict)

    def send_survey_link(self, email, survey_id):
        subject = "Survey Link"
        message = f"Please participate in our survey: http://localhost:8000/companyapp/survey_request/{survey_id}"
        sender = "wpdltm4@gmail.com"
        send_mail(subject, message, sender, [email], fail_silently=False)

    def send_survey_result(self, email, survey_id):
        subject = "Survey Result Link"
        message = f"This is the result of survey: http://localhost:8000/companyapp/totalresult/{survey_id}"
        sender = "wpdltm4@gmail.com"
        send_mail(subject, message, sender, [email], fail_silently=False)

    def send_survey_to_target_user(self, survey_id: int, network: Network):
        user_ids = network.find_target_user()
        for user_id in user_ids:
            user = PersonalEmail.objects.get(id=user_id)
            self.send_survey_link(user.email, survey_id)

    def send_survey_result_to_company(self, survey_id: int):
        survey = Survey.objects.get(id=survey_id)
        self.send_survey_result(survey.email, survey_id)
