from django.db import models
from django.urls import reverse
# Create your models here.

length = 100

study_type = (
    ('choises...', 'Choises...'),
    ('individual', 'Individual'),
    ('team', 'Team'),
)

study_days = (
    ('choises...', 'Choises...'),
    ('du-ch-j', 'Du-Ch-J'),
    ('se-p-sh', 'Se-P-Sh'),
    ('du-se-ch-p-j', 'Du-Se-Ch-P-J'),
    ('every-day', 'Every-day')
)

# Markazda o'rgatiladigan fanlarni royhatga olish


class Subject(models.Model):
    name = models.CharField(max_length=length, blank=True, null=True)
    payment = models.IntegerField(default=150000)
    added_time = models.DateTimeField(auto_now_add=True)

    @property
    # Bitta fan uchun O'quvchi qancha to'lagani Korsatib beradi
    def get_total_benifit(self):
        student_payment = self.student_set.all()
        total = sum([item.paied_payment for item in student_payment])
        return total

    @property
    def get_total(self):  # Bitta fanda qancha o'quvchi o'qishini Korsatadi
        students = self.student_set.all()
        total = students.filter(study_subject=self.id).count()
        return total

    @property
    def get_total_teacher(self):  # Bitta fanda nechta o'qituvchi borligini Korsatadi
        teachers = self.teacher_set.all()
        total = teachers.filter(subject=self.id).count()
        return total

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('List:Subjects', kwarg={self.id: 'id'})

# Markazda ishlaydigan O'qituvchilarni royhatga olish uchun

class Teacher(models.Model):
    first_name = models.CharField(max_length=length, blank=True, null=True)
    last_name = models.CharField(max_length=length, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    expirence = models.CharField(max_length=length)
    added_time = models.DateTimeField(auto_now_add=True)

    @property
    # O'qituvchini O'quvchilari qancha to'lov qilganlarini korsatadi
    def get_total_benifit(self):
        student_payment = self.student_set.all()
        total = sum([item.paied_payment for item in student_payment])
        return total

    @property
    # Bitta O'qituvchining qancha oylik olishini korsatadi (o'quvchi tolagan summani yarmini)
    def get_total_salary(self):
        salary = self.get_total_benifit // 2
        return salary

    @property
    def total_salary(self):  # hamma o'qituvchilar umumiy qancha oylik olishayotgani korsatadi
        items = Teacher.objects.all()
        total = sum([i.get_total_salary for i in items])
        return total

    @property
    def get_total(self):  # O'qituchining qancha O'quvchisi borligini Korsatadi
        students = self.student_set.all()
        total = students.filter(teacher=self.id).count()
        return total

    def __str__(self):
        return f'{self.first_name} from {self.subject}'

    def __unicode__(self):
        return self.first_name

# Markazda O'qiydigan talabalarni royhatga olish uchun


class Student(models.Model):
    first_name = models.CharField(max_length=length, blank=True, null=True)
    last_name = models.CharField(max_length=length, blank=True, null=True)
    study_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    study_days = models.CharField(
        max_length=length, choices=study_days, default='choises...')
    study_type = models.CharField(
        max_length=length, choices=study_type, default='choises...')
    paied_payment = models.IntegerField(default=0)
    phone_number = models.IntegerField()
    added_time = models.DateTimeField(auto_now_add=True)

    @property
    def total_paied_payment(self):  # talaba qancha tolov qilgani korsatadi
        students = Student.objects.all()
        total = sum([item.paied_payment for item in students])
        return total

    @property
    # talaba tolagan summadan qanchasi oqituvchiga tegishini korsatadi
    def total_for_teachers_payment(self):
        students = Student.objects.all()
        total_payment = sum([item.paied_payment for item in students])
        total = total_payment // 2
        return total

    @property
    def total_outlay(self):  # firma hisobidan qancha chiqib bolayotgani hisoblaydi
        outlay = AllofOutlay.objects.all()
        total = sum([i.outlay for i in outlay])
        return total

    @property
    def pureBenifit(self):  # soft foydani korsatib beradi
        benifit = self.total_for_teachers_payment - self.total_outlay
        return benifit

    @property
    def total_student(self):  # Umumiy talabalar sonini hisoblaydi
        students = Student.objects.all().count()
        return students

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def __unicode__(self):
        return f'{self.first_name} in {self.study_subject}'

# markazni umumiy chiqimlarini royhatga olish


class AllofOutlay(models.Model):
    name = models.CharField(max_length=length, blank=True, null=True)
    outlay = models.IntegerField(default=0)
    spending_time = models.DateTimeField(auto_now_add=True)

    @property
    def total_outlay(self):  # umumiy chiqimlarni korsatadi
        outlay = AllofOutlay.objects.all()
        total = sum([i.outlay for i in outlay])
        return total

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
