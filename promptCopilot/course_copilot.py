import openai
import gspread
import re
from config import api_key, api_google
from oauth2client.service_account import ServiceAccountCredentials
from prompts import course_name, target_audience, specific_topics, course_level, course_focus, next_learning_unit

# Initial Configuration
openai.api_key = api_key
#API Google Sheets
#API Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('course-copilot-425602-78432e6747e5.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Pipeline para creación de cursos')
sheet1 = spreadsheet.sheet1
sheet2 = spreadsheet.get_worksheet(1) 
sheet3 = spreadsheet.get_worksheet(2) 
sheet4 = spreadsheet.get_worksheet(3) 



def generate_chatgpt(prompt, model="gpt-4o",temperature =0.7):
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
        f"Este curso tiene un nivel {course_level}. El perfil de ingreso ideal para este curso es..., no se deben usar caracteres especiales o formatos específicos para el texto."
    )

    return generate_chatgpt(prompt)



def search_and_analyze_courses(course_name, course_level,profile):
    print(f"Realizando investigación de cursos similares a {course_name} de nivel {course_level}...")

    prompt = f"Como experto diseñador de programas académicos especializado en tecnología, tu tarea es desarrollar un nuevo curso titulado {course_name} dirigido a {profile}. Para garantizar que el curso sea competitivo y cumpla con las expectativas del público objetivo, realiza una investigación comparativa de tres cursos relacionados disponibles en plataformas de educación en línea, tomando en cuenta el {course_level} Formato:   'Nombre: [nombre], Año: [año], Objetivos: [objetivo1, objetivo2, objetivo3]', Descripcion Breve: [descripcion-breve], Temario Detallado [temario-detallado]  , Retorna [número] Nombre: [nombre], Año: [año], Objetivos: [objetivo1, objetivo2, objetivo3].  Descripcion Breve: [descripcion-breve], Temario Detallado [temario-detallado] , no se deben usar caracteres especiales o formatos específicos para el texto. solo es permitido []"
    response = generate_chatgpt(prompt)
    courses =response
    
    sections = re.split(r'\n\d',courses)
    if sections[0]  == ' ':
        sections = sections[1:]

    return sections


def generate_course_objectives(course_name, course_level, course_focus, profile, specific_topics):
    prompt = (
        f"Basándote en las áreas de oportunidad identificadas y en los {specific_topics} si es que existen, "
        f"para el curso de {course_name} con un nivel {course_level} y un enfoque {course_focus}, "
        f"orientado a {profile} procede a definir un objetivo claro y conciso del curso. "
        f"Estos objetivos deben estructurarse de manera que reflejen las metas educativas del programa y cómo se alinean con las necesidades del {profile}. "
        f"El nombre del objetivo tiene que captar la esencia del curso, y la descripción del objetivo describe en habilidades. No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido []."
        f"\n\nNombre[nombre del Objetivo], Descripción[descripcion del objetivo]\n"
    )
    return generate_chatgpt(prompt)


def generate_course_secondary_objectives(course_name, course_level, course_focus, profile, specific_topics, principal_objective):
    prompt = (
        f"Basándote en las áreas de oportunidad identificadas y en los {specific_topics} si es que existen, "
        f"para el curso de {course_name} con un nivel {course_level} y un enfoque {course_focus}, y en el objetivo principal {principal_objective} "
        f"orientado a {profile} procede a definir 5 objetivos claros y concisos del curso. "
        f"Estos objetivos deben estructurarse de manera que reflejen las metas educativas del programa y cómo se alinean con las necesidades del {profile}. "
        f"El nombre del objetivo tiene que captar la esencia del curso, y la descripción del objetivo describe en habilidades. No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido []."
        f"\n\nNumero[numero del objetivo],Nombre[nombre del Objetivo], Descripción[descripcion del objetivo]\n"
    )
    return generate_chatgpt(prompt)


def generate_graduate_profile(course_name, target_audience, specific_topics, next_learning_unit, principal_objetive, secondary_objetives):

    prompt = (
        f"Basándote en la descripción del curso que es {course_name}y los objetivos  que son {principal_objetive} y {secondary_objetives} tanto generales como específicos definidos previamente y en los {specific_topics}, "
        f"procede a crear un perfil de egreso para los estudiantes que completen el curso de {course_name}, "
        f"enfocado especialmente en aquellos {target_audience}. "
        f"Considera que idealmente el siguiente paso en su camino de aprendizaje es tener las bases para continuar su aprendizaje en {next_learning_unit}, "
        f"sin embargo no lo menciones explícitamente. "
        f"- Redacta un párrafo que sea claro, conciso e impactante, reflejando el valor que los estudiantes aportarán a sus empresas o su crecimiento profesional tras completar el curso. "
        f"Este debe resumir las capacidades, la mentalidad y la preparación con la que contarán los egresados, destacando su preparación para enfrentar los desafíos tecnológicos actuales."
    )
    return generate_chatgpt(prompt)

print('Generating Income Profile .... 🤖')

profile = generate_course_entry_profile(course_name, target_audience, specific_topics, course_level, course_focus)
print ('Writting in Google Sheets .... ✍️ ')

sheet1.update_cell(2, 1, profile)

print ('Done! ✅')


print('Generating Courses  .... 🤖')

course = search_and_analyze_courses(course_name, course_level,profile)



print ('Writting in Google Sheets .... ✍️ ')

for i, section in enumerate(course, start=0):
    sheet2.update_cell(i+2, 1, section)


print ('Done! ✅')



print('Generating  Principal Objetive .... 🤖')

principal_objetive = generate_course_objectives(course_name, course_level, course_focus, profile, specific_topics)

print ('Writting in Google Sheets .... ✍️ ')

# Search Objetivo in the text
match = re.search(r'Nombre\[(.*?)\]', principal_objetive)
if match:
    name = match.group(1)
    sheet3.update_cell(2, 1, name)

match = re.search(r'Descripción\[(.*?)\]', principal_objetive)
if match:
    description = match.group(1)
    sheet3.update_cell(3, 1, description)

    print ('Done! ✅')



print('Generating  Objectives .... 🤖')

secondary_objetives = generate_course_secondary_objectives(course_name, course_level, course_focus, profile, specific_topics, principal_objetive)

print ('Writting in Google Sheets .... ✍️ ')

# Dividir el texto en líneas
lines = secondary_objetives.strip().split('\n')

# Iterar sobre las líneas
for i, line in enumerate(lines, start=3):
    number_match = re.search(r'Número\[(.*?)\]', line)
    name_match = re.search(r'Nombre\[(.*?)\]', line)
    description_match = re.search(r'Descripción\[(.*?)\]', line)


    if number_match and name_match and description_match:
        sheet3.update_cell(i, 3, name_match.group(1))
        sheet3.update_cell(i, 4, description_match.group(1))

print ('Done! ✅')

print('Generating Graduate Profile .... 🤖')
graduate_profile = generate_graduate_profile(course_name, target_audience, specific_topics, next_learning_unit, principal_objetive, secondary_objetives)


print ('Writting in Google Sheets .... ✍️ ')


sheet4.update_cell(1, 2, graduate_profile)

print ('Done! ✅')

print('Generating Principal Habilities .... 🤖')
