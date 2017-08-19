# -*- coding: utf-8 -*-
from django.db import models
from manager import managers

class Institution(models.Model):
    id = models.AutoField(primary_key=True)
    acronym = models.CharField(max_length=50, blank=False, null=False, verbose_name="abreviação")
    name = models.CharField(max_length=500, blank=False, null=False, verbose_name="nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'

class Campus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, blank=False, null=False, verbose_name="nome")
    address = models.CharField(max_length=500, blank=False, null=False, verbose_name="endereço")
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, verbose_name=Institution._meta.verbose_name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'

class RequirementType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name="nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo do Requisito'
        verbose_name_plural = 'Tipos dos Requisitos'

class Requirement(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey('RequirementType', on_delete=models.CASCADE, verbose_name="tipo")
    description = models.CharField(max_length=100, blank=False, null=False, verbose_name="descrição")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Requisito'
        verbose_name_plural = 'Requisitos'

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=False, null=False, verbose_name="código")
    description = models.CharField(max_length=100, blank=False, null=False, verbose_name="descrição")
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, verbose_name=Campus._meta.verbose_name)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'

class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name="nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo da Sala'
        verbose_name_plural = 'Tipos das Salas'

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=False, null=False, verbose_name="código")
    description = models.CharField(max_length=100, blank=False, null=False, verbose_name="descrição")
    capacity = models.PositiveSmallIntegerField(default=0, verbose_name="capacidade")
    type = models.ForeignKey('RoomType', verbose_name=RoomType._meta.verbose_name)
    area = models.ForeignKey('Area', verbose_name=Area._meta.verbose_name)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    acronym = models.CharField(max_length=50, blank=False, null=False, verbose_name="abreviação")
    name = models.CharField(max_length=500, blank=False, null=False, verbose_name="nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=False, null=False, verbose_name="código")
    name = models.CharField(max_length=500, blank=False, null=False, verbose_name="nome")
    workload = models.PositiveSmallIntegerField(default=0, verbose_name="carga horária")
    semester_number = models.PositiveSmallIntegerField(default=0, verbose_name="semestre")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

class Period(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="nome")
    start_time = models.TimeField(blank=False, null=False, verbose_name="hora inicial")
    end_time = models.TimeField(blank=False, null=False, verbose_name="hora final")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

class TimeInterval(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    start_time = models.TimeField(blank=False, null=False, verbose_name="hora inicial")
    end_time = models.TimeField(blank=False, null=False, verbose_name="hora final")

    def __str__(self):
        return "{:%H:%M}".format(self.start_time) + " - " + "{:%H:%M}".format(self.end_time)

    class Meta:
        verbose_name = 'Intervalo de Tempo'
        verbose_name_plural = 'Intervalos de Tempo'

class Day(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="nome")
    time_intervals = models.ManyToManyField('TimeInterval', verbose_name=TimeInterval._meta.verbose_name_plural)

    def __str__(self):
        return self.name

    def get_day_time_intervals(self):
        return self.time_intervals

    class Meta:
        verbose_name = 'Dia'
        verbose_name_plural = 'Dias'

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.ForeignKey('Day', on_delete=models.CASCADE,  verbose_name=Day._meta.verbose_name)
    time_interval = models.ForeignKey('TimeInterval', on_delete=models.CASCADE, verbose_name=TimeInterval._meta.verbose_name_plural)

    def __str__(self):
        return "{0} - {1}".format(self.day, self.time_interval)

    class Meta:
        verbose_name = 'Cronograma'
        verbose_name_plural = 'Cronogramas'
        unique_together = (('day', 'time_interval'),)

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    code = models.CharField(max_length=500, blank=False, null=False, verbose_name="código")
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=0)
    semester = models.PositiveSmallIntegerField(default=0)
    schedules = models.ManyToManyField('Schedule', blank=True, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.course, self.code)

    @classmethod
    def reset_all_schedules(self):
        for s_class in Class.objects.all():
            s_class.schedules.through.objects.all().delete()

    def reset_schedules_by_day(self, day):
        for s_class in self.objects.all():
            for schedule in s_class.schedules.get(day = day):
                s_class.schedules.remove(schedule)

    def reset_schedules_by_course(self, course):
        for s_class in self.objects.get(course = course):
            s_class.schedules.through.objects.all().delete()

    def reset_class_schedules(self, id):
        s_class = self.objects.get(id = id)
        if s_class:
            s_class.schedules.through.objects.all().delete()

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

class Slot(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.ForeignKey('Day', on_delete=models.CASCADE, verbose_name="dia")
    time_interval = models.ForeignKey('TimeInterval', on_delete=models.CASCADE, verbose_name=TimeInterval._meta.verbose_name)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name=Room._meta.verbose_name)
    s_class = models.ForeignKey('Class', blank=True, null=True, verbose_name=Class._meta.verbose_name)
    objects = managers.SlotManager()

    def __str__(self):
        return "{0} - {1} : {2} em {3}".format(self.day, self.time_interval, "Espaço vago" if self.s_class is None else self._class, self.room)

    class Meta:
        verbose_name = 'Alocação da turma em sala'
        verbose_name_plural = 'Alocações das turmas em salas'
        unique_together = (('day', 'time_interval', 'room'),)
