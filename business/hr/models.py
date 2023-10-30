from django.db import models
from django.core.validators import MaxValueValidator

from hr.constants import (
    GENDER_CHOICES,
    MAXIMUM_YOE,
    MAXIMUM_ANNUAL_INCOME,
)

from hr.validators import (
    validate_dob,
    validate_dob_with_yoe
)


class Industry(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['name']


class Employee(models.Model):
    first_name = models.CharField(max_length=128, default="")
    last_name = models.CharField(max_length=128, default="")
    annual_income = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(MAXIMUM_ANNUAL_INCOME)])
    gender = models.CharField(null=True, max_length=1, choices=GENDER_CHOICES)
    yoe = models.PositiveSmallIntegerField(null=True, db_comment="Years of experience", validators=[MaxValueValidator(MAXIMUM_YOE)])
    dob = models.DateField(null=True, db_comment="Date of birth in the format", validators=[validate_dob])
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['id']
        
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def full_clean(self):
        super(Employee, self).clean()
        validate_dob_with_yoe(self.dob, self.yoe)
