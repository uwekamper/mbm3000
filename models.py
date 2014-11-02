from redisco import models
    
class Person(models.Model):
    name = models.Attribute(required=True)
    mustvote = models.BooleanField(default=False)
    voted = models.IntegerField(default=0)

class Meeting(models.Model):
    name = models.Attribute(required=True)
    people = models.ListField(Person)
    started = models.BooleanField(default=False)
    wave_the_flag = models.BooleanField(default=False)

