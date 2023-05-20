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
            # PersonalInfoForm 데이터 저장

            survey = Survey(email=form.cleaned_data['email'])
            survey.save()

            for question_form in formset:
                # 각 QuestionForm 데이터 저장
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
        # survey_id로 Survey 인스턴스를 가져옵니다.
        survey = get_object_or_404(Survey, id=survey_id)

        # 관련된 모든 Question 인스턴스를 가져옵니다.
        questions = survey.questions.all()

        for question in questions:
            # Question에 대한 응답을 가져옵니다.
            response = request.POST.get(f'response_{question.id}')

            # 응답에 따라 적절한 answer_count 값을 증가시킵니다.
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
                # 잘못된 응답 값을 처리합니다.
                return JsonResponse({'error': 'Invalid response value.'}, status=400)

            # Question 인스턴스를 업데이트합니다.
            question.save()

        total_responses = 0
        for question in questions:
            total_responses += question.answer_count_1
            total_responses += question.answer_count_2
            total_responses += question.answer_count_3
            total_responses += question.answer_count_4
            total_responses += question.answer_count_5

        # 3명이 응답하면 전송
        if (total_responses == survey.questions.count() * 3):
            company = Company()
            company.send_survey_result_to_company(survey_id)

        return HttpResponse('Success', status=200)
    else:
        # POST가 아닌 다른 HTTP 메소드를 처리합니다.
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


def survey_total_result(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()
    return render(request, 'companyapp/survey_total_result.html', {'survey': survey, 'questions': questions})


def home(request):
    return render(request, 'companyapp/home.html')
