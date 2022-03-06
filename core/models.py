from django.db import models


# Create your models here.
class Operation(models.Model):
    operation_name = models.CharField(max_length=100, blank=False)
    number_of_arguments = models.IntegerField(default=1)
    argument_type = models.CharField(choices=(('number', 'number'), ('text', 'text')), default='number', max_length=10)
    example_text = models.TextField(blank=True, null=True)
    operation_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.operation_name}'
