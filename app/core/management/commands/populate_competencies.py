from school import models
from django.core.management.base import BaseCommand

competencies = [
    {
        "id": 1,
        "title": "Construye su identidad.",
        "area": 1
    },
    {
        "id": 2,
        "title": "Convive y participa democráticamente en la búsqueda del bien común.",
        "area": 1
    },
    {
        "id": 3,
        "title": "Construye interpretaciones históricas.",
        "area": 2
    },
    {
        "id": 4,
        "title": "Gestiona responsablemente el espacio y el ambiente.",
        "area": 2
    },
    {
        "id": 5,
        "title": "Gestiona responsablemente los recursos económicos",
        "area": 2
    },
    {
        "id": 6,
        "title": "Gestiona proyectos de emprendimiento económico o social.",
        "area": 3
    },
    {
        "id": 7,
        "title": "Se desenvuelve de manera autónoma a través de su motricidad.",
        "area": 4
    },
    {
        "id": 8,
        "title": "Asume una vida saludable.",
        "area": 4
    },
    {
        "id": 9,
        "title": "Interactúa a través de sus habilidades sociomotrices.",
        "area": 4
    },
    {
        "id": 10,
        "title": "Se comunica oralmente en su lengua materna.",
        "area": 5
    },
    {
        "id": 11,
        "title": "Lee diversos tipos de textos escritos en lengua materna.",
        "area": 5
    },
    {
        "id": 12,
        "title": "Escribe diversos tipos de textos en lengua materna.",
        "area": 5
    },
    {
        "id": 13,
        "title": "Aprecia de manera crítica manifestaciones artístico-culturales.",
        "area": 6
    },
    {
        "id": 14,
        "title": "Crea proyectos desde los lenguajes artísticos.",
        "area": 6
    },
    {
        "id": 15,
        "title": "Se comunica oralmente en castellano como segunda lengua.",
        "area": 7
    },
    {
        "id": 16,
        "title": "Lee diversos tipos de textos escritos en castellano como segunda lengua.",
        "area": 7
    },
    {
        "id": 17,
        "title": "Escribe diversos tipos de textos en castellano como segunda lengua.",
        "area": 7
    },
    {
        "id": 18,
        "title": "Se comunica oralmente en inglés como lengua extranjera",
        "area": 8
    },
    {
        "id": 19,
        "title": "Lee diversos tipos de textos escritos en inglés como lengua extranjera.",
        "area": 8
    },
    {
        "id": 20,
        "title": "Escribe diversos tipos de textos en inglés como lengua extranjera.",
        "area": 8
    },
    {
        "id": 21,
        "title": "Resuelve problemas de cantidad.",
        "area": 9
    },
    {
        "id": 22,
        "title": "Resuelve problemas de regularidad, equivalencia y cambio.",
        "area": 9
    },
    {
        "id": 23,
        "title": "Resuelve problemas de forma, movimiento y localización.",
        "area": 9
    },
    {
        "id": 24,
        "title": "Resuelve problemas de gestión de datos e incertidumbre.",
        "area": 9
    },
    {
        "id": 25,
        "title": "Indaga mediante métodos científicos para construir conocimientos.",
        "area": 10
    },
    {
        "id": 26,
        "title": "Explica el mundo físico basándose en conocimientos sobre los seres vivos, materia y energía, biodiversidad, Tierra y universo.",
        "area": 10
    },
    {
        "id": 27,
        "title": "Diseña y construye soluciones tecnológicas para resolver problemas de su entorno.",
        "area": 10
    },
    {
        "id": 28,
        "title": "Construye su identidad como persona humana, amada por Dios, digna, libre y trascendente, comprendiendo la doctrina de su propia religión, abierto al diálogo con las que le son cercanas.",
        "area": 11
    },
    {
        "id": 29,
        "title": "Asume la experiencia del encuentro personal y comunitario con Dios en su proyecto de vida en coherencia con su creencia religiosa.",
        "area": 11
    },
    {
        "id": 30,
        "title": "Gestiona su aprendizaje de manera autónoma.",
        "area": 12
    },
    {
        "id": 31,
        "title": "Se desenvuelve en entornos virtuales generados por las TIC.",
        "area": 12
    },
]

class Command(BaseCommand):
    help = 'Populate all competencies'

    def handle(self, *args, **kwargs):

        for competency in competencies:
            models.Competence.objects.create(
                id=competency['id'],
                title=competency['title'],
                area=models.Area.objects.get(id=competency['area'])
            )
            self.stdout.write(self.style.SUCCESS(f'Competency "{competency["title"]}" created successfully.'))