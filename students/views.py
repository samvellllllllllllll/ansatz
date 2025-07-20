from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
# from .forms import MyUserCreationForm
# from .forms import CustomUserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.core.mail import send_mail
# class StudentRegistrationView(CreateView):
#     template_name='students/student/registration.html'
#     form_class=CustomUserCreationForm
#     success_url=reverse_lazy('student_course_list')

#     def form_valid(self, form):
#         result=super().form_valid(form)
#         cd=form.cleaned_data
#         user=authenticate(username=cd['username'], password=cd['password1'])
#         login(self.request, user)
#         return result

# class StudentEnrollCourseView(LoginRequiredMixin, FormView):
#     course=None
#     form_class=CourseEnrollForm

#     def form_valid(self, form):
#         self.course=form.cleaned_data['course']
#         self.course.students.add(self.request.user)
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse_lazy('student_course_detail', args=[self.course.id])

class StudentApplyCourseView(LoginRequiredMixin, FormView):
    course=None
    form_class=CourseEnrollForm

    def form_valid(self, form):
        self.course=form.cleaned_data['course']
        self.course.applications.add(self.request.user)
        send_mail(
                subject="Заявка на курс",
                message= f"{self.request.user.email} отправил заявку на '{self.course.title}'. Идентификатор курса: {self.course.id}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["s.89041229317@gmail.com"],
                fail_silently=False,
            )
        messages.success(
            self.request,
            f'Вы успешно подали заявку на курс "{self.course.title}"!'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('course_detail', args=[self.course.slug])
    
class StudentCourseListView(LoginRequiredMixin, ListView):
    model=Course
    template_name='students/course/list.html'

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    
class StudentCourseDetailView(DetailView):
    model=Course
    template_name='students/course/detail.html'

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        course=self.get_object()
        if 'module_id' in self.kwargs:
            context['module']=course.modules.get(id=self.kwargs['module_id'])
        else:
            if course.modules.count()>0:
                context['module']=course.modules.all()[0]
        return context
    
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

from .models import CustomUser, ConfirmationCode
from .forms import UserRegistrationForm, EmailVerificationForm#, ResendCodeForm

class RegisterView(FormView):
    template_name = 'students/registration_form.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('verify-email')

    def form_valid(self, form):
        self.request.session['registration_email'] = form.cleaned_data['email']
        self.request.session['password'] = form.cleaned_data['password']
        confirmation = ConfirmationCode.generate_code(self.request.session['registration_email'])
        
        subject = 'Подтверждение регистрации'
        html_message = render_to_string('students/email_confirmation.html', {
            'email': self.request.session['registration_email'],
            'code': confirmation.code,
            'CONFIRMATION_CODE_EXPIRE_MINUTES': settings.CONFIRMATION_CODE_EXPIRE_MINUTES
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.session['registration_email']],#user.email],
            fail_silently=False,
        )
        
        return super().form_valid(form)

class RegistrationSuccessView(TemplateView):
    template_name = 'students/registration_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('registration_email')
        return context

class VerifyEmailView(FormView):
    template_name = 'students/verification_form.html'
    form_class = EmailVerificationForm
    success_url = reverse_lazy('verification-success')

    def get_initial(self):
        initial = super().get_initial()
        if 'registration_email' in self.request.session:
            initial['email'] = self.request.session['registration_email']
        return initial

    def form_valid(self, form):
        
        email=self.request.session['registration_email']
        code = form.cleaned_data['code']
        
        try:
            confirmation = ConfirmationCode.objects.get(email=email, code=code)
            if not confirmation.is_valid():
                confirmation.delete()
                form.add_error('code', 'Срок действия кода истек. Запросите новый.')
                return self.form_invalid(form)
            
            user =CustomUser.objects.create_user(email, self.request.session['password'])

            user.is_email_verified = True
            user.save()
            confirmation.delete()
            
            if 'registration_email' in self.request.session:
                del self.request.session['registration_email']
            if 'password' in self.request.session:
                del self.request.session['password']
            
            return super().form_valid(form)
        except ConfirmationCode.DoesNotExist:
            form.add_error('code', 'Неверный код подтверждения.')
            return self.form_invalid(form)