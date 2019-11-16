from django.urls    import path
from .views         import (
                            YearView,
                            MonthView,
                            DayView,
                            SignUpView, 
                            SignInView, 
                            KakaoSignInView
                           )

urlpatterns = [
    path('/year', YearView.as_view()),
    path('/month', MonthView.as_view()),
    path('/day', DayView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/kakao_signin', KakaoSignInView.as_view()),
]
