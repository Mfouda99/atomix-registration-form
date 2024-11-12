from django.db import models


class Registrationform(models.Model):
    # Choices for Position dropdown
    POSITION_CHOICES = [
        ('select', 'Select your position'),
        ('LCP', 'LCP'),
        ('LCVP', 'LCVP'),
        ('MM', 'MM'),
        ('TM', 'TM'),
    ]

    # Choices for Function dropdown
    FUNCTION_CHOICES = [
        ('select', 'Select your function'),
        ('OGV', 'OGV'),
        ('OGT', 'OGT'),
        ('IGV', 'IGV'),
        ('IGTa', 'IGTa'),
        ('B2C', 'B2C'),
        ('B2B', 'B2B'),
        ('MXP', 'MXP'),
        ('F and L', 'F and L'),
    ]

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email= models.EmailField()
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, default='select',null= False)
    function = models.CharField(max_length=100, choices=FUNCTION_CHOICES, default='select')
    id_front = models.FileField(upload_to='idfront')
    id_back = models.FileField(upload_to='idback')
    indemnity_form = models.FileField(upload_to='indemnityform')
    personal_photo = models.ImageField(upload_to='personalphoto')
    submitted_at = models.DateTimeField(auto_now_add=True)
  
  
    