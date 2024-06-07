import openai
import gspread
import json
from config import api_key, api_google
from oauth2client.service_account import ServiceAccountCredentials
from prompts import course_name, target_audience, specific_topics, course_level, course_focus

# Initial Configuration
openai.api_key = api_key
#API Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('course-copilot-425602-78432e6747e5.json', scope)


def generate_chatgpt(prompt, model="gpt-3.5-turbo",temperature =0.7):
    response = openai.chat.completions.create(
        model= model,
        messages=[{"role": "system", "content": "Start"}, {"role": "user", "content": prompt}],
        temperature = temperature
    )
    return response.choices[0].message.content






def generate_course_entry_profile(course_name, target_audience, specific_topics, course_level,course_focus):
    """
    Generates an entry profile for a course based on provided parameters.
    
    Args:
    course_name (str): The name of the course.
    target_audience (str): The intended audience for the course.
    specific_topics (str): Specific topics covered in the course.
    course_level (str): The level of the course (e.g., beginner, intermediate).
    course_focus (str): The main focus of the course.

    Returns:
    str: The recommended entry profile for the course.
    """
    # Definir el prompt para la generación de texto
    prompt = (
        f"Como experto diseñador de programas académicos especializado en tecnología, "
        f"tu tarea es mejorar el perfil de ingreso para el curso de {course_name} "
        f"tomando como base a estudiantes {target_audience} definido para este curso. "
        f"Este curso tiene un nivel {course_level}. El perfil de ingreso ideal para este curso es..."
    )

    response = generate_chatgpt(prompt)
    print(response)



def search_and_analyze_courses(course_name, course_level):
    """Busca y analiza cursos similares para identificar oportunidades de mejora."""
    print(f"Realizando investigación de cursos similares a {course_name} de nivel {course_level}...")

    prompt = f"Genera una lista de cinco cursos similares a {course_name} de nivel {course_level}. Cada curso debe tener un nombre, un año de lanzamiento y una lista de objetivos. Formato: 'Nombre: [nombre], Año: [año], Objetivos: [objetivo1, objetivo2, objetivo3]'. Retorna [número] Nombre: [nombre], Año: [año], Objetivos: [objetivo1, objetivo2, objetivo3]. en lista"
    response = generate_chatgpt(prompt)

    courses = parse_response_to_courses(response)

    # Análisis comparativo
    for course in courses:
        print(f"Evaluando {course['name']} lanzado en {course['year']} con los siguientes objetivos: {course['objectives']}")

    # Identificar cinco áreas de oportunidad
    opportunities = ["Mejora en la profundidad de temas", "Actualización de tecnologías", "Inclusión de proyectos prácticos", "Extensión de colaboraciones industriales", "Ampliación de la comunidad de aprendizaje"]
    return opportunities

 

def parse_response_to_courses(response):
    """Convierte la respuesta de generate_chatgpt en una lista de diccionarios."""
    try:
        courses = json.loads(response)
    except json.JSONDecodeError:
        print("La respuesta no tiene un formato JSON válido.")
        courses = []
    return courses    




profile = generate_course_entry_profile(course_name, target_audience, specific_topics, course_level, course_focus)
print('Generating Income Profile ....')

client = gspread.authorize(creds)
sheet = client.open('Pipeline para creación de cursos').sheet1
sheet.update_cell(2, 1, profile)

print ('Done!')

print ('Writting in Google Sheets ...., ')



