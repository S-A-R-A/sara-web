# -*- coding: utf-8 -*-
from django.db import models

class Institution(models.Model):
    id = models.IntegerField
    acronym = models.CharField(max_length=20, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'

class Campus(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    institution = models.ForeignKey('Institution')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'

class RequirementType(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo do Requisito'
        verbose_name_plural = 'Tipos dos Requisitos'

class Requirement(models.Model):
    id = models.IntegerField
    type = models.ForeignKey('RequirementType')
    description = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Requisito'
        verbose_name_plural = 'Requisitos'

class Area(models.Model):
    id = models.IntegerField
    code = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    campus = models.ForeignKey('Campus')

    def __str__(self):
        return self.code +' - ' + self.description

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'

class RoomType(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo da Sala'
        verbose_name_plural = 'Tipos das Salas'

class Room(models.Model):
    id = models.IntegerField
    code = models.CharField(max_length=20, blank=False, null=False)
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
    id = models.IntegerField
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

class Program(models.Model):
    id = models.IntegerField
    acronym = models.CharField(max_length=20, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Course(models.Model):
    id = models.IntegerField
    code = models.CharField(max_length=20, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    workload = models.PositiveSmallIntegerField(default=0)
    semester_number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

class Class(models.Model):
    id = models.IntegerField
    course = models.ForeignKey('Course')
    code = models.CharField(max_length=200, blank=False, null=False)
    teacher = models.ForeignKey('Teacher')
    size = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=0)
    semester = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.course + " - " + code

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

class Period(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=100, blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

class TimeInterval(models.Model):
    id = models.IntegerField
    period = models.ForeignKey('Period')
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)

    def __str__(self):
        return "{:%H:%M}".format(self.start_time) + " - " + "{:%H:%M}".format(self.end_time)

    class Meta:
        verbose_name = 'Intervalo de Tempo'
        verbose_name_plural = 'Intervalos de Tempo'

class Slot(models.Model):
    id = models.IntegerField
    day = models.ForeignKey('Day')
    time_interval = models.ForeignKey('TimeInterval')
    room = models.ForeignKey('Room')
    class_ = models.ForeignKey('Class')

    def __str__(self):
        return day + " - " + time_interval + ": " +  class_ + " em " + room

    class Meta:
        verbose_name = 'Alocação da turma em sala'
        verbose_name_plural = 'Alocações das turmas em salas'
