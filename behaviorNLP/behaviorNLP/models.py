from django.db import models

# class test(models.Model):
#     name = models.CharField(max_length=32)

class Condition(models.Model):
    con_name = models.CharField(max_length=255)
    def __str__(self):
        return self.con_name

class Behavior(models.Model):
    con_id_list = models.CharField(max_length=255)
    detail_behavior = models.CharField(max_length=255)
    def __str__(self):
        return self.con_id_list

class Con_Beh(models.Model):
    con_name = models.CharField(max_length=255)
    detail_behavior = models.CharField(max_length=255)
    def __str__(self):
        return self.con_name