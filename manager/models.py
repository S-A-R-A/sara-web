# -*- coding: utf-8 -*-
from django.db import models
from manager import managers

class Institution(models.Model):
    id = models.AutoField(primary_key=True)
    acronym = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'

class Campus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, blank=False, null=False)
    address = models.CharField(max_length=500, blank=False, null=False)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'

class RequirementType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo do Requisito'
        verbose_name_plural = 'Tipos dos Requisitos'

class Requirement(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey('RequirementType', on_delete=models.CASCADE)
    description = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Requisito'
        verbose_name_plural = 'Requisitos'

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.code, self.description)

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'

class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo da Sala'
        verbose_name_plural = 'Tipos das Salas'

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    capacity = models.PositiveSmallIntegerField(default=0)
    type = models.ForeignKey('RoomType')
    area = models.ForeignKey('Area')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    acronym = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=500, blank=False, null=False)
    workload = models.PositiveSmallIntegerField(default=0)
    semester_number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    code = models.CharField(max_length=500, blank=False, null=False)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=0)
    semester = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{0} - {1}".format(self.course, self.code)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

class Period(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

class TimeInterval(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)

    def __str__(self):
        return "{:%H:%M}".format(self.start_time) + " - " + "{:%H:%M}".format(self.end_time)

    class Meta:
        verbose_name = 'Intervalo de Tempo'
        verbose_name_plural = 'Intervalos de Tempo'

class Day(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    time_intervals = models.ManyToManyField('TimeInterval')

    def __str__(self):
        return self.name

    def get_day_time_intervals(self):
        return self.time_intervals

    class Meta:
        verbose_name = 'Dia'
        verbose_name_plural = 'Dias'

class Slot(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.ForeignKey('Day', on_delete=models.CASCADE)
    time_interval = models.ForeignKey('TimeInterval', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    s_class = models.ForeignKey('Class', blank=True, null=True)
    objects = managers.SlotManager()

    def __str__(self):
        return "{0} - {1} : {2} em {3}".format(self.day, self.time_interval, "Espaço vago" if self.s_class is None else self._class, self.room)

    class Meta:
        verbose_name = 'Alocação da turma em sala'
        verbose_name_plural = 'Alocações das turmas em salas'
        unique_together = (('day', 'time_interval', 'room'),)
