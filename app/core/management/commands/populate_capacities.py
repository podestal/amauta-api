from school import models
from django.core.management.base import BaseCommand

capacities = [
    {
        "id": 1,
        "title": "Se valora a sí mismo",
        "competence": 1
    },
    {
        "id": 2,
        "title": "Autorregula sus emociones",
        "competence": 1
    },
    {
        "id": 3,
        "title": "Reflexiona y argumenta éticamente",
        "competence": 1
    },
    {
        "id": 4,
        "title": "Vive su sexualidad de manera integral y responsable de acuerdo a su etapa de desarrollo y madurez.",
        "competence": 1
    },
    {
        "id": 55,
        "title": "Interactúa con todas las personas",
        "competence": 2
    },
    {
        "id": 56,
        "title": "Construye y asume acuerdos y Normas",
        "competence": 2
    },
    {
        "id": 57,
        "title": "Maneja conflictos de manera constructiva",
        "competence": 2
    },
    {
        "id": 58,
        "title": "Delibera sobre asuntos públicos",
        "competence": 2
    },
    {
        "id": 59,
        "title": "Participa en acciones que promueven el bienestar común",
        "competence": 2
    },
    {
        "id": 60,
        "title": "Interpreta críticamente fuentes diversas",
        "competence": 3
    },
    {
        "id": 61,
        "title": "Comprende el tiempo histórico",
        "competence": 3
    },
    {
        "id": 62,
        "title": "Explica y argumenta procesos históricos",
        "competence": 3
    },
    {
        "id": 63,
        "title": "Comprende las relaciones entre los elementos naturales y sociales",
        "competence": 4
    },
    {
        "id": 64,
        "title": "Maneja fuentes de información para comprender el espacio geográfico y el ambiente",
        "competence": 4
    },
    {
        "id": 65,
        "title": "Genera acciones para preservar el ambiente local y global",
        "competence": 4
    },
    {
        "id": 66,
        "title": "Comprende las relaciones entre los elementos del sistema económico y financiero",
        "competence": 5
    },
    {
        "id": 67,
        "title": "Toma decisiones económicas y financieras",
        "competence": 5
    },
    {
        "id": 95,
        "title": "Crea propuestas de valor",
        "competence": 6
    },
    {
        "id": 96,
        "title": "Trabaja cooperativamente para lograr objetivos y metas",
        "competence": 6
    },
    {
        "id": 97,
        "title": "Aplica habilidades técnicas",
        "competence": 6
    },
    {
        "id": 98,
        "title": "Evalúa los resultados del proyecto de emprendimiento",
        "competence": 6
    },
    {
        "id": 5,
        "title": "Comprende su cuerpo",
        "competence": 7
    },
    {
        "id": 6,
        "title": "Se expresa corporalmente",
        "competence": 7
    },
    {
        "id": 7,
        "title": "Incorpora prácticas que mejoran su calidad de vida",
        "competence": 8
    },
    {
        "id": 8,
        "title": "Se relaciona utilizando sus habilidades sociomotrices",
        "competence": 9
    },
    {
        "id": 9,
        "title": "Crea y aplica estrategias y tácticas de juego",
        "competence": 9
    },
    {
        "id": 30,
        "title": "Obtiene información de textos orales",
        "competence": 10
    },
    {
        "id": 32,
        "title": "Infiere e interpreta información de textos orales",
        "competence": 10
    },
    {
        "id": 33,
        "title": "Adecúa, organiza y desarrolla las ideas de forma coherente y cohesionada",
        "competence": 10
    },
    {
        "id": 36,
        "title": "Utiliza recursos No verbales y paraverbales de forma estratégica",
        "competence": 10
    },
    {
        "id": 37,
        "title": "Interactúa estratégicamente con distintos interlocutores",
        "competence": 10
    },
    {
        "id": 40,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto oral",
        "competence": 10
    },
    {
        "id": 41,
        "title": "Obtiene información del texto escrito",
        "competence": 11
    },
    {
        "id": 44,
        "title": "Infiere e interpreta información del texto",
        "competence": 11
    },
    {
        "id": 45,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto escrito",
        "competence": 11
    },
    {
        "id": 48,
        "title": "Adecúa el texto a la situación comunicativa",
        "competence": 12
    },
    {
        "id": 49,
        "title": "Organiza y desarrolla las ideas de forma coherente y cohesionada",
        "competence": 12
    },
    {
        "id": 52,
        "title": "Utiliza convenciones del lenguaje escrito de forma pertinente",
        "competence": 12
    },
    {
        "id": 53,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto escrito",
        "competence": 12
    },
    {
        "id": 10,
        "title": "Percibe manifestaciones artístico-culturales",
        "competence": 13
    },
    {
        "id": 11,
        "title": "Contextualiza las manifestaciones artístico-culturales",
        "competence": 13
    },
    {
        "id": 12,
        "title": "Reflexiona creativa y críticamente sobre las manifestaciones artístico- culturales",
        "competence": 13
    },
    {
        "id": 13,
        "title": "Explora y experimenta los lenguajes de las artes",
        "competence": 14
    },
    {
        "id": 14,
        "title": "Aplica procesos de creación",
        "competence": 14
    },
    {
        "id": 15,
        "title": "Evalúa y comunica sus procesos y proyectos",
        "competence": 14
    },
    {
        "id": 16,
        "title": "Obtiene información de textos orales",
        "competence": 15
    },
    {
        "id": 17,
        "title": "Infiere e interpreta información de textos orales",
        "competence": 15
    },
    {
        "id": 18,
        "title": "Adecua, organiza y desarrolla las ideas de forma coherente y cohesionada",
        "competence": 15
    },
    {
        "id": 19,
        "title": "Utiliza recursos No verbales y paraverbales de forma estratégica",
        "competence": 15
    },
    {
        "id": 20,
        "title": "Interactúa estratégicamente con distintos interlocutores",
        "competence": 15
    },
    {
        "id": 21,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto oral",
        "competence": 15
    },
    {
        "id": 22,
        "title": "Obtiene información del texto escrito",
        "competence": 16
    },
    {
        "id": 23,
        "title": "Infiere e interpreta información del texto",
        "competence": 16
    },
    {
        "id": 24,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto escrito",
        "competence": 16
    },
    {
        "id": 25,
        "title": "Adecúa el texto a la Situación comunicativa",
        "competence": 17
    },
    {
        "id": 26,
        "title": "Organiza y desarrolla las ideas de forma coherente y cohesionada",
        "competence": 17
    },
    {
        "id": 27,
        "title": "Utiliza convenciones del lenguaje escrito de forma pertinente",
        "competence": 17
    },
    {
        "id": 28,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto escrito",
        "competence": 17
    },
    {
        "id": 29,
        "title": "Obtiene información de textos orales",
        "competence": 18
    },
    {
        "id": 31,
        "title": "Infiere e interpreta información de textos orales",
        "competence": 18
    },
    {
        "id": 34,
        "title": "Adecúa, organiza y desarrolla las ideas de forma coherente y cohesionada",
        "competence": 18
    },
    {
        "id": 35,
        "title": "Utiliza recursos No verbales y paraverbales de forma estratégica",
        "competence": 18
    },
    {
        "id": 38,
        "title": "Interactúa estratégicamente con distintos interlocutores",
        "competence": 18
    },
    {
        "id": 39,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto oral",
        "competence": 18
    },
    {
        "id": 42,
        "title": "Obtiene información del texto escrito",
        "competence": 19
    },
    {
        "id": 43,
        "title": "Infiere e interpreta información del texto",
        "competence": 19
    },
    {
        "id": 46,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto escrito",
        "competence": 19
    },
    {
        "id": 47,
        "title": "Adecúa el texto a la situación comunicativa",
        "competence": 20
    },
    {
        "id": 50,
        "title": "Organiza y desarrolla las ideas de forma coherente y cohesionada",
        "competence": 20
    },
    {
        "id": 51,
        "title": "Utiliza convenciones del lenguaje escrito de forma pertinente",
        "competence": 20
    },
    {
        "id": 54,
        "title": "Reflexiona y evalúa la forma, el contenido y el contexto del texto escrito",
        "competence": 20
    },
    {
        "id": 79,
        "title": "Traduce cantidades a expresiones numéricas",
        "competence": 21
    },
    {
        "id": 80,
        "title": "Comunica su comprensión sobre los números y las operaciones",
        "competence": 21
    },
    {
        "id": 81,
        "title": "Usa estrategias y procedimientos de estimación y cálculo",
        "competence": 21
    },
    {
        "id": 82,
        "title": "Argumenta afirmaciones sobre las relaciones numéricas y las operaciones",
        "competence": 21
    },
    {
        "id": 83,
        "title": "Traduce datos y condiciones a expresiones algebraicas",
        "competence": 22
    },
    {
        "id": 84,
        "title": "Comunica su comprensión sobre las relaciones algebraicas",
        "competence": 22
    },
    {
        "id": 85,
        "title": "Usa estrategias y procedimientos para encontrar reglas generales",
        "competence": 22
    },
    {
        "id": 86,
        "title": "Argumenta afirmaciones sobre relaciones de cambio y equivalencia",
        "competence": 22
    },
    {
        "id": 91,
        "title": "Modela objetos con formas geométricas y sus transformaciones",
        "competence": 23
    },
    {
        "id": 92,
        "title": "Comunica su comprensión sobre las formas y relaciones geométricas",
        "competence": 23
    },
    {
        "id": 93,
        "title": "Usa estrategias y procedimientos para orientarse en el espacio",
        "competence": 23
    },
    {
        "id": 94,
        "title": "Argumenta afirmaciones sobre relaciones geométricas",
        "competence": 23
    },
    {
        "id": 87,
        "title": "Representa datos con gráficos y medidas estadísticas o probabilísticas",
        "competence": 24
    },
    {
        "id": 88,
        "title": "Comunica la comprensión de los conceptos estadísticos y probabilísticos",
        "competence": 24
    },
    {
        "id": 89,
        "title": "Usa estrategias y procedimientos para recopilar y procesar datos",
        "competence": 24
    },
    {
        "id": 90,
        "title": "Sustenta conclusiones o decisiones basado en información obtenida",
        "competence": 24
    },
    {
        "id": 68,
        "title": "Problematiza situaciones",
        "competence": 25
    },
    {
        "id": 69,
        "title": "Diseña estrategias para hacer indagación",
        "competence": 25
    },
    {
        "id": 70,
        "title": "Genera y registra datos e información",
        "competence": 25
    },
    {
        "id": 71,
        "title": "Analiza datos e información",
        "competence": 25
    },
    {
        "id": 72,
        "title": "Evalúa y comunica el proceso y los resultados de su indagación",
        "competence": 25
    },
    {
        "id": 73,
        "title": "Comprende y usa conocimientos sobre los seres vivos; materia y energía; biodiversidad, Tierra y universo",
        "competence": 26
    },
    {
        "id": 74,
        "title": "Evalúa las implicancias del saber y del quehacer científico y tecnológico",
        "competence": 26
    },
    {
        "id": 75,
        "title": "Determina una alternativa de solución tecnológica",
        "competence": 27
    },
    {
        "id": 76,
        "title": "Diseña la alternativa de solución tecnológica",
        "competence": 27
    },
    {
        "id": 77,
        "title": "Implementa y valida alternativas de solución tecnológica",
        "competence": 27
    },
    {
        "id": 78,
        "title": "Evalúa y comunica el funcionamiento y los impactos de su alternativa de solución tecnológica",
        "competence": 27
    },
    {
        "id": 106,
        "title": "Conoce a Dios y asume su identidad religiosa como persona digna, libre y trascendente",
        "competence": 28
    },
    {
        "id": 107,
        "title": "Cultiva y valora las manifestaciones religiosas de su entorno argumentando su fe de manera comprensible y respetuosa",
        "competence": 28
    },
    {
        "id": 108,
        "title": "Transforma su entorno desde el encuentro personal y comunitario con Dios y desde la fe que profesa",
        "competence": 29
    },
    {
        "id": 109,
        "title": "Actúa coherentemente en razón de su fe según los principios de su conciencia moral en situaciones concretas de la vida.",
        "competence": 29
    },
    {
        "id": 103,
        "title": "Define metas de aprendizaje",
        "competence": 30
    },
    {
        "id": 104,
        "title": "Organiza acciones estratégicas para alcanzar sus metas de aprendizaje",
        "competence": 30
    },
    {
        "id": 105,
        "title": "Monitorea y ajusta su desempeño durante el proceso de aprendizaje",
        "competence": 30
    },
    {
        "id": 99,
        "title": "Personaliza entornos virtuales",
        "competence": 31
    },
    {
        "id": 100,
        "title": "Gestiona información del entorno virtual",
        "competence": 31
    },
    {
        "id": 101,
        "title": "Interactúa en entornos virtuales",
        "competence": 31
    },
    {
        "id": 102,
        "title": "Crea objetos virtuales en diversos formatos",
        "competence": 31
    }
]

class Command(BaseCommand):
    help = 'Populate all capacities'

    def handle(self, *args, **kwargs):
        i = 1
        for capacity in capacities:
            models.Capacity.objects.create(id=i, title=capacity['title'], competence=models.Competence.objects.get(id=capacity['competence']))
            self.stdout.write(self.style.SUCCESS(f'Capacity "{capacity["title"]}" created successfully.'))
            i += 1