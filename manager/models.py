# -*- coding: utf-8 -*-
from django.db import models
from manager import managers
from itertools import chain

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
        unique_together = (('area', 'code'),)
        ordering = ['area', 'code']

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="nome")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

class ProgramLevel(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=20, blank=False, null=False, verbose_name="descrição")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Nível do Curso'
        verbose_name_plural = 'Níveis dos Cursos'

class ProgramType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=False, null=False, verbose_name="descrição")
    level = models.ForeignKey('ProgramLevel', on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Nível do Curso'
        verbose_name_plural = 'Níveis dos Cursos'

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    acronym = models.CharField(max_length=50, blank=False, null=False, verbose_name="abreviação")
    name = models.CharField(max_length=500, blank=False, null=False, verbose_name="nome")
    type = models.ForeignKey('ProgramType', on_delete=models.CASCADE)

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
        return "{0} - {1}".format(self.code, self.name)

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        unique_together = (('code'),)
        ordering = ['code', 'name']

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
        ordering = ['start_time']

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
        ordering = ['id']


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.ForeignKey('Day', on_delete=models.CASCADE,  verbose_name=Day._meta.verbose_name)
    time_interval = models.ForeignKey('TimeInterval', on_delete=models.CASCADE, verbose_name=TimeInterval._meta.verbose_name_plural)

    def __str__(self):
        return "{0} - {1}".format(self.day, self.time_interval)

    @classmethod
    def get_used_slots(self):
        used_schedules = []
        for schedule in self.objects.all():
            if Class.objects.filter(schedules = schedule) :
                used_schedules.append(schedule)
        return used_schedules

    class Meta:
        verbose_name = 'Cronograma'
        verbose_name_plural = 'Cronogramas'
        unique_together = (('day', 'time_interval'),)

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    code = models.CharField(max_length=500, blank=False, null=False, verbose_name="código")
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name=Teacher._meta.verbose_name)
    size = models.PositiveSmallIntegerField(default=0, verbose_name="tamanho")
    year = models.PositiveSmallIntegerField(default=0, verbose_name="ano letivo")
    semester = models.PositiveSmallIntegerField(default=0, verbose_name="semestre")
    schedules = models.ManyToManyField('Schedule', verbose_name=Schedule._meta.verbose_name_plural)

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

    @classmethod
    def get_scheduled_classes(self):
        scheduled_classes = []
        for s_class in self.objects.all():
            if s_class.schedules.all():
                scheduled_classes.append(s_class)
        return scheduled_classes

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        unique_together = (('course', 'code'),)
        ordering = ['course']

class Slot(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.ForeignKey('Day', on_delete=models.CASCADE, verbose_name="dia")
    time_interval = models.ForeignKey('TimeInterval', on_delete=models.CASCADE, verbose_name=TimeInterval._meta.verbose_name)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name=Room._meta.verbose_name)
    s_class = models.ForeignKey('Class', blank=True, null=True, verbose_name=Class._meta.verbose_name)
    objects = managers.SlotManager()

    def __str__(self):
        return "{0} - {1} : {2} em {3}".format(self.day, self.time_interval, "Espaço vago" if self.s_class is None else self.s_class, self.room)

    @classmethod
    def reset_all(self):
        Slot.objects.all().update(s_class=None)

    @classmethod
    def get_empty_slots(self):
        return Slot.objects.filter(s_class=None)

    @classmethod
    def get_filled_slots(self):
        return Slot.objects.exclude(s_class=None)

    @classmethod
    def get_slots_to_schedules(self):
        slots = []
        for schedule in Class.get_filled_schedules():
            slots_by_schedule = list(self.objects.filter(day = schedule.day, time_interval = schedule.time_interval))
            print(slots_by_schedule)
            break
            for current in slots_by_schedule:
                if not current in slots:
                    slots.append(current)
        return slots

    class Meta:
        verbose_name = 'Alocação da turma em sala'
        verbose_name_plural = 'Alocações das turmas em salas'
        unique_together = (('day', 'time_interval', 'room'),)
        ordering = ['day', 'time_interval', 'room']
