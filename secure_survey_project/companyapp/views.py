from django.shortcuts import render, redirect, get_object_or_404
from .models import Survey, Question
from .forms import PersonalConditionForm, QuestionFormset
from .company import Company, PersonalCondition
from django.conf import settings
from django.http import HttpResponse, JsonResponse


def request_research(request):
    if request.method == 'POST':
        form = PersonalConditionForm(request.POST)
        formset = QuestionFormset(request.POST, prefix='questions')

        if form.is_valid() and formset.is_valid():

            survey = Survey(email=form.cleaned_data['email'])
            survey.save()

            for question_form in formset:
                question_text = question_form.cleaned_data['question_text']
                question = Question(survey=survey, question_text=question_text)
                question.save()

            personal_condition = PersonalCondition(form)
            company = Company()
            company.set_personal_conditions(personal_condition)

            network = settings.NETWORK_INSTANCE

            company.save_personal_conditions(network)
            company.send_survey_to_target_user(survey.id, network)

            return redirect('companyapp:success_url')

        else:

            print("is not vaild!!!")
            form = PersonalConditionForm()
            formset = QuestionFormset(prefix='questions')
            return render(request, 'companyapp/request_form.html', {'form': form, 'formset': formset})

    else:
        form = PersonalConditionForm()
        formset = QuestionFormset(prefix='questions')
        return render(request, 'companyapp/request_form.html', {'form': form, 'formset': formset})


def success(request):
    return render(request, 'companyapp/success.html')


def survey_request(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    for question in survey.questions.all():
        print(question.question_text)
    return render(request, 'companyapp/survey_request.html', {'survey': survey})


def survey_response(request, survey_id):
    if request.method == 'POST':
        survey = get_object_or_404(Survey, id=survey_id)

        questions = survey.questions.all()

        for question in questions:
            response = request.POST.get(f'response_{question.id}')

            if response == '1':
                question.answer_count_1 += 1
            elif response == '2':
                question.answer_count_2 += 1
            elif response == '3':
                question.answer_count_3 += 1
            elif response == '4':
                question.answer_count_4 += 1
            elif response == '5':
                question.answer_count_5 += 1
            else:
                return JsonResponse({'error': 'Invalid response value.'}, status=400)

            question.save()

        total_responses = 0
        for question in questions:
            total_responses += question.answer_count_1
            total_responses += question.answer_count_2
            total_responses += question.answer_count_3
            total_responses += question.answer_count_4
            total_responses += question.answer_count_5

        if (total_responses == survey.questions.count() * 3):
            company = Company()
            company.send_survey_result_to_company(survey_id)

        return HttpResponse('Success', status=200)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


def survey_total_result(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()
    return render(request, 'companyapp/survey_total_result.html', {'survey': survey, 'questions': questions})


def home(request):
    return render(request, 'companyapp/home.html')
