from phone_field import PhoneField
from django.conf import settings
from django.db import models


class Clients(models.Model):

    firstname = models.CharField(max_length=25, blank=False)
    lastname = models.CharField(max_length=25, blank=False)
    email = models.EmailField(max_length=50)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    mobile = PhoneField(blank=True, help_text='Contact mobile number')
    companyname = models.CharField(max_length=250, blank=False)
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)
    salescontact = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True)
    clientstatus = models.BooleanField(default=False,
                                       verbose_name='prospect/Client')

    def __str__(self):
        statut = "Prospect"
        if self.clientstatus is True:
            statut = "Client"
        return f"{self.id}, {self.companyname}, ({statut})"

    class Meta:
        verbose_name_plural = "Clients"


class Contrats(models.Model):

    salescontact = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE,
                               related_name='contrat')
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)
    contratstatus = models.BooleanField(default=False,
                                        verbose_name='contrat non signé/Signé')
    amount = models.FloatField()
    paymentdue = models.DateTimeField(auto_now=True)

    def __str__(self):
        statut = "non signé"
        if self.contratstatus is True:
            statut = "signé"
        return f"{self.id}, ({statut})"

    class Meta:
        verbose_name_plural = "Contrats"


class Events(models.Model):

    client = models.ForeignKey(Clients, on_delete=models.CASCADE,
                               related_name='client')
    contrat = models.OneToOneField(Contrats, on_delete=models.CASCADE,
                                   related_name='event')
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)
    supportcontact = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.SET_NULL,
                                       null=True, blank=True)
    eventstatus = models.BooleanField(default=False,
                                      verbose_name='en cours/Terminé')
    attendees = models.IntegerField()
    eventdate = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=250, blank=False)

    def __str__(self):
        statut = "En cours"
        if self.eventstatus is True:
            statut = "Terminé"

        return f"{self.supportcontact}, {self.contrat}, ({statut})"

    class Meta:
        verbose_name_plural = "Events"
