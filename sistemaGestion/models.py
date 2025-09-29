from django.db import models

# Create your models here.

#Definido modelo a modo de ejemplo para ir realizando los demas.
class Clientes(models,Model):
  numero_cliente = models.Charfield(max_length=50)
  nombre = models.Charfield(max_length=50)
  email = models.Charfield(max_length=50)
  telefono = models.Charfield(max_length=15)
  
  
