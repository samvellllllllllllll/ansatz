from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import RegisterView, VerifyEmailView, RegistrationSuccessView
urlpatterns = [
    # path('register/',views.StudentRegistrationView.as_view(),name='student_registration'),
    #path('enroll-course/',views.StudentEnrollCourseView.as_view(),name='student_enroll_course'),
    path('application/',views.StudentApplyCourseView.as_view(),name='student_apply_course'),
    # path('enroll-course/',views.StudentEnrollCourseView.as_view(),name='student_enroll_course'),
    path('courses/',views.StudentCourseListView.as_view(),name='student_course_list'),
    path('course/<pk>/',views.StudentCourseDetailView.as_view(),name='student_course_detail'),
    path('course/<pk>/<module_id>/',views.StudentCourseDetailView.as_view(),name='student_course_detail_module'),
    # path('register/', views.register, name='register'),
    # path('confirm/<str:confirmation_code>/', views.confirm_email, name='confirm_email'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/success/', RegistrationSuccessView.as_view(), name='registration-success'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('verify-email/success/', TemplateView.as_view(template_name='students/verification_success.html'), name='verification-success'),
]