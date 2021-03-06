from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
import random
from django.contrib.messages import error
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def info(request):
    if request.method == 'GET':
        data = {}
        recommend = random.sample(list(Content.objects.all()), 10)
        food = random.sample(list(Content.objects.filter(type='food')), 10)
        # diet_plan = random.sample(list(Content.objects.filter(type='diet_plan')), 10)
        workout = random.sample(list(Content.objects.filter(type='workout')), 10)
        # workout_routine = random.sample(list(Content.objects.filter(type='workout_routine')), 10)
        data['recommend'] = recommend
        data['food'] = food
        # data['diet_plan'] = diet_plan
        data['workout'] = workout
        # data['workout_routine'] = workout_routine
        return render(request, 'info/info.html', {'data': data})


def search(request):
    if request.method == 'GET':
        type = request.GET['type']
        query = request.GET['query']
        if type == '전체':
            results = Content.objects.filter(Q(item__icontains=query) | Q(description__icontains=query))
            if len(results) == 0:
                return render(request, 'info/search.html', {'no_result': '결과가 없습니다.'})
            data = {}
            for result in results:
                try:
                    data[result.type] += [result]
                except:
                    data[result.type] = [result]
        else:
            data = Content.objects.filter(Q(type=type) & (Q(item__icontains=query) | Q(description__icontains=query)))
            if len(data) == 0:
                return render(request, 'info/search.html', {'no_result': '결과가 없습니다.'})
        return render(request, 'info/search.html', {'data': data, 'type': type})


def content_type(request, type):
    if request.method == 'GET':
        page_number = request.GET.get('page')
        if not page_number:
            recommend = random.sample(list(Content.objects.filter(type=type)), 10)
            content = Content.objects.filter(type=type)[:30]
            return render(request, 'info/content_type.html', {'type': type, 'content': content, 'recommend': recommend})
        else:
            content_list = Content.objects.filter(type=type).order_by('pk')[20:]
            paginator = Paginator(content_list, 10)
            if int(page_number) <= paginator.num_pages:
                obj_list = paginator.get_page(page_number)
                data_list = [{'id': obj.id, 'item': obj.item} for obj in obj_list]
                return JsonResponse(data_list, status=200, safe=False)
            elif int(page_number) > paginator.num_pages:
                return HttpResponse(status=404)


def content_detail(request, pk):
    if request.method == 'GET':
        try:
            content = Content.objects.get(id=pk)
            type = content.type
            if type == 'food':
                data = Food.objects.get(content=content)
            elif type == 'diet_plan':
                data = DietPlan.objects.get(content=content)
            elif type == 'workout':
                data = Workout.objects.get(content=content)
            elif type == 'workout_routine':
                data = WorkoutRoutine.objects.get(content=content)
            if SaveContent.objects.filter(content=content, user=request.user).exists():
                return render(request, 'info/content_detail.html', {'type': type, 'data': data, 'save': 'no'})
            else:
                return render(request, 'info/content_detail.html', {'type': type, 'data': data})
        except:
            error(request, '존재하지 않는 컨텐츠 입니다.')
            return redirect('/info')

@login_required()
def content_save(request, pk):
    if request.method == 'POST':
        user = request.user
        content = Content.objects.get(id=pk)
        save_content = SaveContent.objects.filter(user=user, content=content)
        if save_content.exists():
            save_content.delete()
            error(request, '컨텐츠를 저장을 취소했습니다.')
        else:
            SaveContent.objects.create(user=user, content=content)
            error(request, '컨텐츠를 저장했습니다.')
        return redirect(request.headers['Referer'])


def calories_calculate(request):
    if request.method == 'GET':
        met = WorkoutCaloriesCalculate.objects.all()
        return render(request, 'info/calories_calculate.html', {'met': met})
