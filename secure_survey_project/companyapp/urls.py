from django.urls import path
from . import views

app_name = 'companyapp'

urlpatterns = [
    path('request/', views.request_research, name='request'),
    path('success/', views.success, name='success_url'),
    path('survey_request/<int:survey_id>/',
         views.survey_request, name='survey_detail'),
    path('survey_response/<int:survey_id>/',
         views.survey_response, name='result'),
    path('totalresult/<int:survey_id>/',
         views.survey_total_result, name='totalresult'),
]
