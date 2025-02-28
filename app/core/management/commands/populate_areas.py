from school import models
from django.core.management.base import BaseCommand

areas = [
    {
        "id": 1,
        "title": "Desarollo personal y ciudadanía cívica"
    },
    {
        "id":2,
        "title": "Ciencias Sociales"
    },
    {
        "id":3,
        "title": "Educación para el trabajo"
    },
    {
        "id":4,
        "title": "Educación física"
    },
    {
        "id":5,
        "title": "Comunicación"
    },
    {
        "id":6,
        "title": "Arte y cultura"
    },
    {
        "id":7,
        "title": "Castellano como segunda lengua"
    },
    {
        "id":8,
        "title": "Inglés como segunda lengua"
    },
    {
        "id":9,
        "title": "Matemática"
    },
    {
        "id":10,
        "title": "Ciencia y tecnología"
    },
    {
        "id":11,
        "title": "Educación religiosa"
    },
    {
        "id":12,
        "title": "Transversales"
    }
]

class Command(BaseCommand):
    help = 'Populate all areas of study'

    def handle(self, *args, **kwargs):
        i = 1
        for area in areas:
            title = area['title']
            models.Area.objects.create(id=area['id'], title=title)
            self.stdout.write(self.style.SUCCESS(f'Area "{title}" created successfully.'))
            i += 1
