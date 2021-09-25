from django.shortcuts import render
from .models import (
    Student,
    Teacher,
    Subject,
    AllofOutlay
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import (
    SubjectForm,
    TeacherForm,
    StudentForm,
    Outlayform
)
from django.db.models import Q

# Create your views here.


def Home(request):
    return render(request, 'home.html')

# fanlar royhati uchun


def Subjects(request):
    sub = Subject.objects.all().order_by('id')
    context = {
        'sub': sub
    }
    return render(request, 'subjects.html', context)

# bitta fanga bog'langan ustozlar


def Teachers(request, sub_id):
    tea = Teacher.objects.filter(subject=sub_id)

    context = {
        'tea': tea,
        'sub_id': sub_id,
    }
    return render(request, 'teachers.html', context)

# bitta ustozga va fanga bo'glangan oquvchilar


def Students(request, tea_id):
    stu = Student.objects.filter(teacher=tea_id).order_by('id')
    context = {
        'tea_id': tea_id,
        'stu': stu,
    }
    return render(request, 'students.html', context)

# royhatga olish bolimi


def Register(request):
    return render(request, 'register/register_home.html')

# hamma o'qituvchilarni ko'rsatish uchun


class WorkerList(ListView):
    model = Teacher
    template_name = 'coworkers/workers.html'
    ordering = 'added_time'
    paginate_by = 5

# fanlarni qoshish o'chirish va yangilash


class SubjectCreate(CreateView):
    form_class = SubjectForm
    template_name = 'register/subject_form.html'
    success_url = '/register'

    def form_valid(self, form):
        return super().form_valid(form)


class SubjectUpdate(UpdateView):
    model = Subject
    template_name = 'update/subject_update.html'
    success_url = '/'
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)


class SubjectDelete(DeleteView):
    model = Subject
    success_url = '/subjects'
    template_name = 'delete/subject_delete.html'
# o'qituvchilarni qoshish o'chirish va yangilash


class TeacherCreate(CreateView):
    form_class = TeacherForm
    template_name = 'register/teacher_form.html'
    success_url = '/register'

    def form_valid(self, form):
        return super().form_valid(form)


class TeacherUpdate(UpdateView):
    model = Teacher
    template_name = 'update/teacher_update.html'
    success_url = '/subjects'
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)


class TeacherDelete(DeleteView):
    model = Teacher
    success_url = '/subjects'
    template_name = 'delete/teacher_delete.html'

# talabalarni qoshish o'chirish va yangilash


class StudentCreate(CreateView):
    form_class = StudentForm
    template_name = 'register/student_form.html'
    success_url = '/register'

    def form_valid(self, form):
        return super().form_valid(form)


class StudentUpdate(UpdateView):
    model = Student
    template_name = 'update/student_update.html'
    success_url = '/subjects'
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)


class StudentDelete(DeleteView):
    model = Student
    success_url = '/subject'
    template_name = 'delete/student_delete.html'

# umumiy malumotlar


def All_of_Them(request):
    sub, tea, stu = Subject.objects.all(), Teacher.objects.all(), Student.objects.all()
    c_sub, c_tea, c_stu, = sub.count(), tea.count(), stu.count(),
    context = {
        'sub': sub,
        'tea': tea,
        'stu': stu,
        'c_sub': c_sub,
        'c_tea': c_tea,
        'c_stu': c_stu,
    }
    return render(request, 'report_section/report_home.html', context)

# chiqimlarni kosatish uchun


class Total_Outlies(CreateView):
    form_class = Outlayform
    template_name = 'report_section/total_outlies.html'
    success_url = '/outlay'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = AllofOutlay.objects.all()
        return super().get_context_data(**kwargs)


class Total_OutliesUpdate(UpdateView):
    model = AllofOutlay
    template_name = 'report_section/outlies_update.html'
    success_url = '/outlay'
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)


class Total_OutlayDelete(DeleteView):
    model = AllofOutlay
    success_url = '/outlay'
    template_name = 'delete/outlay_delete.html'

# Hamma Talabalarni korsatish uchun


class All_StudentList(ListView):
    model = Student
    template_name = 'all/all_students.html'
    ordering = '-added_time'
    paginate_by = 5

# Qidiruv tizimi uchun


class SearchWorkerList(ListView):
    model = Teacher
    template_name = 'search/worker_search.html'
    ordering = 'first_name'

    def get_queryset(self):
        query = self.request.GET.get('W')
        object_list = Teacher.objects.filter(
            Q(first_name__icontains=query) | Q(address__icontains=query) | Q(
                expirence__icontains=query) | Q(last_name__icontains=query)
        )
        return object_list


class SearchStudentList(ListView):
    model = Student
    template_name = 'search/student_search.html'
    ordering = 'teacher'

    def get_queryset(self):
        query = self.request.GET.get('S')
        object_list = Student.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query))
        return object_list
