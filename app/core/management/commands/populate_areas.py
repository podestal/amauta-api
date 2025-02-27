from school import models
from django.core.management.base import BaseCommand

areas = [
    "Desarollo personal y ciudadanía cívica",
    "Ciencias Sociales",
    "Educación para el trabajo",
    "Educación física",
    "Comunicación",
    "Arte y cultura",
    "Castellano como segunda lengua",
    "Inglés como segunda lengua",
    "Matemática",
    "Ciencia y tecnología",
    "Educación religiosa",
    "Transversales"
]

class Command(BaseCommand):
    help = 'Populate all areas of study'

    def handle(self, *args, **kwargs):
        i = 1
        for area in areas:
            models.Area.objects.create(id=i, title=area)
            self.stdout.write(self.style.SUCCESS(f'Area "{area}" created successfully.'))
            i += 1
