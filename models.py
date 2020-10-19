from django.db import models

from project.models import AppModel


class Board(AppModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.CharField(max_length=255, verbose_name="Описние", blank=True)
    number = models.PositiveIntegerField(verbose_name="Номер", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "доска"
        verbose_name_plural = "доски"
        ordering = ("number",)


class Label(AppModel):
    COLOR_CHOICES = (
        ('black', 'Черный'),
        ('gray', 'Серый'),
        ('blue', 'Синий'),
        ('dodgerblue', 'Голубой'),
        ('green', 'Зеленый'),
        ('red', 'Красный'),
        ('orange', 'Оранжевый'),
    )

    name = models.CharField(verbose_name="Название", max_length=255)
    color = models.CharField(verbose_name="Цвет", max_length=50, choices=COLOR_CHOICES, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "лейбл"
        verbose_name_plural = "лейблы"


class Issue(AppModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описние", blank=True)
    private = models.BooleanField(verbose_name="Приватная задача", default=False)
    active = models.BooleanField(default=True)
    assigner = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="назначивший",
        blank=True,)
    assignee = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="исполнитель",
        blank=True,
        related_name="issues",)
    board = models.ForeignKey(
        "dashboard.Board",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="доска",
        blank=True,
        related_name="issues", )
    order = models.ForeignKey(
        "order.Order",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="заявка",
        blank=True,
        related_name="issues", )
    labels = models.ManyToManyField(
        "dashboard.Label",
        verbose_name="лейблы",
        related_name="issues",
        blank=True, )
    expiration_date = models.DateField(
        verbose_name="дата окончания", null=True, blank=True
    )
    number = models.PositiveIntegerField(verbose_name="номер", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ("-number",)
