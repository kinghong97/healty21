import random
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm
from .models import User, UserFollowing, UserProfile


def home(request):
    user = request.user
    if user.is_authenticated:
        all_users = User.objects.all().select_related("userprofile")  # user.profile시 query 사용 방지
        # 유저를 팔로우하는 유저들 = user.follower.all() = follower_list의 following_user가 로그인 된 유저
        # follower_list[0].user 시 쿼리 방지
        follower_list = UserFollowing.objects.filter(following_user=user).select_related("user", "following_user")
        follower_list = all_users.filter(following__in=follower_list)  # follower_list[2].userprofile로 접근 가능 + 쿼리 방지

        # 유저가 팔로잉 하는 유저들 = user.following.all() = user가 로그인 된 유저인 관계
        # following_list[2].following_user 시 쿼리 방지
        following_list = UserFollowing.objects.filter(user=user).select_related("user", "following_user")
        # 유저가 팔로잉 하지 않는 다른 유저들 (nofollowings[8].userprofile.id 해도 query 사용 안함)
        nofollowing_list = all_users.exclude(Q(follower__in=following_list) | Q(id=user.id)).select_related(
            "userprofile"
        )

        following_list = all_users.filter(follower__in=following_list)  # following_list[2].userprofile로 접근 가능 + 쿼리 방지

        # 추천 필터링
        if user.point == 0 and (len((users_by_points := User.objects.filter(point=0).exclude(id=user.id))) <= 5):
            users_by_points = users_by_points
        elif user.point == 0:
            users_by_points = random.sample(list(users_by_points), 5)
        else:
            # 같은 그룹과 유사한 포인트 가진 사람 보여주기
            users_by_groups = User.objects.filter(group=user.group).exclude(id=user.id)  # 유저 그룹으로 1차 필터링
            # 유저와 포인트 차이로 sort하고 5명까지
            users_by_points = sorted(users_by_groups, key=lambda x: abs(x.point - user.point))[:5]
        return render(
            request,
            "user/home.html",
            {
                "all_users": all_users,
                "nofollowing_list": nofollowing_list,
                "follower_list": follower_list,
                "following_list": following_list,
                "users_by_points": users_by_points,
            },
        )
    else:
        return render(request, "user/home.html")


@login_required()
def profile(request):
    if request.method == "POST":
        try:
            form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        except:
            form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            if "image" in request.FILES:
                request.user.image = request.FILES["image"]
            profile = form.save(commit=False)  # 저장 늦추기
            profile.user = request.user
            weight = form.cleaned_data["weight"]
            height = form.cleaned_data["height"] / 100

            # bmi 계산
            bmi = round(weight / (height * height), 1)
            # bmi 카테고리
            profile.bmi = bmi
            if bmi <= 18.5:
                bmi_category = "저체중 Underweight"
            elif bmi <= 24.9:
                bmi_category = "정상체중 Normal"
            elif bmi <= 29.9:
                bmi_category = "과체중 Overweight"
            else:
                bmi_category = "비만 Obesity"
            profile.bmi_category = bmi_category
            # 나이 계산
            today = date.today()
            born = form.cleaned_data["birth_day"]
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            profile.age = age
            # 기초 대사량 계산
            if profile.gender == "M":
                profile.bmr = round(66.4730 + (13.7516 * weight) + (5.0033 * height) - (6.7550 * age), 1)
            elif profile.gender == "F":
                profile.bmr = round(655.0955 + (9.5634 * weight) + (1.8496 * height) - (4.6756 * age), 1)
            profile.save()
            messages.success(request, f"프로필이 성공적으로 업데이트 되었습니다!")
            return redirect("home")  # ! 나중에 경쟁/game으로 변경
    else:
        try:
            form = ProfileForm(instance=request.user.userprofile)
        except:
            form = ProfileForm()
    return render(request, "user/profile.html", {"form": form})


@login_required()
def follow(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)  # following 할 사람
    following = UserFollowing.objects.filter(following_user=person, user=request.user)
    if person != request.user:
        if not following:
            UserFollowing.objects.create(following_user=person, user=request.user)
        else:
            following[0].delete()
    return redirect("home")


def people_list(request):  # TemplateView 고려
    return redirect("home")


def profile_view(request):
    return redirect("home")
