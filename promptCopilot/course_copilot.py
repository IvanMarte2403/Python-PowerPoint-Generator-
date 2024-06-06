import openai
import gspread
import requests
from config import api_key, api_google
from oauth2client.service_account import ServiceAccountCredentials

# Configura tu API key de OpenAI aquí
openai.api_key = api_key

def generate_course_entry_profile(course_name, target_audience, specific_topics, course_level, course_focus):
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

    # Llamada a la API de OpenAI para generar el texto
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Puedes cambiar el modelo si es necesario
        messages=[{"role": "system", "content": "Start"}, {"role": "user", "content": prompt}],
        temperature=0.7  # Puedes ajustar la temperatura para variar la creatividad de las respuestas
    )

    # Devolver solo el contenido de la respuesta
    return response.choices[0].message.content

# Ejemplo de cómo usar la función
course_name = "Introducción a la Inteligencia Artificial"
target_audience = "principiantes en tecnología"
specific_topics = "aprendizaje automático, redes neuronales"
course_level = "básico"
course_focus = "teórico y práctico"


#Modificación de Hoja Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('course-copilot-425602-78432e6747e5.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Pipeline para creación de cursos').sheet1
#Genera 
sheet.append_row([course_name, target_audience, specific_topics, course_level, course_focus])

profile = generate_course_entry_profile(course_name, target_audience, specific_topics, course_level, course_focus)
print(profile)
