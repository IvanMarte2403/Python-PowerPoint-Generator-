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
sheet5 = spreadsheet.get_worksheet(4) 

 


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

    prompt = f"Como experto diseñador de programas ac adémicos especializado en tecnología, tu tarea es desarrollar un nuevo curso titulado {course_name} dirigido a {profile}. Para garantizar que el curso sea competitivo y cumpla con las expectativas del público objetivo, realiza una investigación comparativa de tres cursos relacionados disponibles en plataformas de educación en línea, tomando en cuenta el {course_level} Formato:   'Nombre: [nombre], Año: [año], Objetivos: [objetivo1, objetivo2, objetivo3]', Descripcion Breve: [descripcion-breve], Temario Detallado [temario-detallado]  , Retorna [número] Nombre: [nombre], Año: [año], Objetivos: [objetivo1, objetivo2, objetivo3].  Descripcion Breve: [descripcion-breve], Temario Detallado [temario-detallado] , no se deben usar caracteres especiales o formatos específicos para el texto. solo es permitido []"
    response = generate_chatgpt(prompt)
    courses =response
    
    sections = re.split(r'\n\d',courses)
    if sections[0]  == ' ':
        sections = sections[1:]

    return sections


def generate_course_objectives(course_name, course_level, course_focus, profile, specific_topics,course):
    prompt = (
        f"Basándote en las áreas de oportunidad identificadas y en los {specific_topics} si es que existen, y los cursos {course} "
        f"para el curso de {course_name} con un nivel {course_level} y un enfoque {course_focus}, "
        f"orientado a {profile} procede a definir un objetivo claro y conciso del curso. "
        f"Estos objetivos deben estructurarse de manera que reflejen las metas educativas del programa y cómo se alinean con las necesidades del {profile}. "
        f"El nombre del objetivo tiene que captar la esencia del curso, y la descripción del objetivo describe en habilidades. No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido []."
        f"\n\nNombre[nombre del Objetivo], Descripción[descripcion del objetivo]\n"
    )
    return generate_chatgpt(prompt)


def generate_course_secondary_objectives(course_name, course_level, course_focus, profile, specific_topics, principal_objective,course):
    prompt = (
        f"Basándote en las áreas de oportunidad identificadas y en los {specific_topics} si es que existen, y en los cursos {course}"
        f"para el curso de {course_name} con un nivel {course_level} y un enfoque {course_focus}, y en el objetivo principal {principal_objective} "
        f"orientado a {profile} procede a definir 5 objetivos claros y concisos del curso. "
        f"Estos objetivos deben estructurarse de manera que reflejen las metas educativas del programa y cómo se alinean con las necesidades del {profile}. "
        f"El nombre del objetivo tiene que captar la esencia del curso, y la descripción del objetivo describe en habilidades. No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido []. Es obligatorio que el numero retorne con el formato Numero[numero del objetivo]"
        f"\n\nNumero[numero del objetivo],Nombre[nombre del Objetivo], Descripción[descripcion del objetivo]\n"
    )
    return generate_chatgpt(prompt)


def generate_graduate_profile(course_name, target_audience, specific_topics, next_learning_unit, principal_objetive, secondary_objetives):

    prompt = (
        f"Basándote en la descripción del curso que es {course_name}y los objetivos  que son {principal_objetive} y {secondary_objetives} tanto generales como específicos definidos previamente y en los {specific_topics}, "
        f"procede a crear un perfil de egreso para los estudiante   s que completen el curso de {course_name}, "
        f"enfocado especialmente en aquellos {target_audience}. "
        f"Considera que idealmente el siguiente paso en su camino de aprendizaje es tener las bases para continuar su aprendizaje en {next_learning_unit}, "
        f"sin embargo no lo menciones explícitamente. "
        f"- Redacta un párrafo que sea claro, conciso e impactante, reflejando el valor que los estudiantes aportarán a sus empresas o su crecimiento profesional tras completar el curso. "
        f"Este debe resumir las capacidades, la mentalidad y la preparación con la que contarán los egresados, destacando su preparación para enfrentar los desafíos tecnológicos actuales."
    )
    return generate_chatgpt(prompt)

def generate_key_skills(course_name, target_audience, graduate_profile):
        prompt = (
            f"En todas las habilidades basate tambien en {graduate_profile}. Para cada una de las 5 habilidades principales del curso {course_name}, enfocado en {target_audience}, "
            f"genera un detalle que incluya:\n"
            f"→ Nombre de la Habilidad: Breve y directo.\n"
            f"→ Dos Key Points: En forma de bullet points, destaca dos aspectos cruciales que evidencian por qué cada habilidad es esencial y cómo contribuye al perfil profesional del egresado en el entorno laboral dinámico de hoy.\n\n"
            f"Retorna el siguiente formato obligatorio  para cada habilidad:, no excluyas ningun []  No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido []\n"
            f"Numero[numero de la habilidad], Nombre:[nombre de la habilidad], Descripcion: [key[habildidad1, habilidad2 ]]"
        )
        
        return generate_chatgpt(prompt)


def generate_course_syllabus(course_name, entry_profile, course_focus, main_objective, course):
   
    # Determining the number of classes and their distribution based on course focus
    if course_focus == "teórico":
        total_classes = 24
        weekly_distribution = "4 clases por semana de 1 hora cada clase, con 3 conceptos clave por clase."
    elif course_focus == "técnico":
        total_classes = 12
        weekly_distribution = "2 clases por semana de 2 horas cada clase, 1 hora teoría y 1 hora de contenido técnico con ejercicios prácticos."

    # Sylabus Prompt
    prompt = (
        f"Como diseñador de programas académicos especializado en tecnología y con experiencia en la creación de cursos de ciencia de datos y negocios para empresas internacionales, basate en los cursos {course} "
        f"tu misión es concretar un temario completo y detallado para el curso de {course_name}, orientado especialmente a {entry_profile} utilizando como base el perfil de egreso previamente generado, "
        f"el objetivo principal y objetivos secundarios, tu tarea consiste en diseñar un temario que cumpla con las especificaciones detalladas y las necesidades de la audiencia. Este temario debe estructurarse considerando los siguientes requisitos:\n"
        f"1. Duración Total del Curso: 6 semanas de enseñanza teórica y práctica, enfocando cada semana en el avance de un proyecto final.\n"
        f"2. Total de clases: {total_classes}, distribución semanal: {weekly_distribution}\n"
        f"Al estructurar el temario, considera lo siguiente:\n"
        f"- La importancia de incorporar fundamentos teóricos sólidos junto con aplicaciones prácticas que reflejen situaciones reales del curso.\n"
        f"- La necesidad de adaptar los contenidos y metodologías de enseñanza para facilitar el aprendizaje del {entry_profile}, el {main_objective} y el enfoque {course_focus}.\n"
        f"- La creación de un ambiente de aprendizaje que promueva la interacción, la resolución de problemas, y el desarrollo de un proyecto final que consolide el aprendizaje de todo el curso y habilidades adquiridas durante el curso.\n"
        f"Nombre Semana: Tiene que ser un nombre de la semana, máximo 6 palabras,\n"
        f"Clase: Tiene que ser un titulo llamativo que refleje el contenido de la clase,\n"
        f"Conceptos: de clase: Los conceptos separados por comas de la clase,\n"
        f"Descripcion de la clase: Una breve descripcion que refleje los conceptos y el contenido de la clase y que outline saldrán los alumnos de esa clase,\n"
        f"Objetivos de la clase: 3 conceptos separados con comas de lo que se espera que los alumnos aprendan en la clase\n"
        f"Retorna el siguiente formato obligatorio para cada habilidad:, no excluyas ningun []  No se deben usar caracteres especiales o formatos específicos para el texto. Solo está permitido [] Semana[Nombre de la semana, Clases[Clase1 [Conceptos de clase], Descripcion de la clase, Objetivos de la clase], Clase2 [Conceptos de clase], Descripcion de la clase, Objetivos de la clase], Clase3 [Conceptos de clase], Descripcion de la clase, Objetivos de la clase], Clase4]\n"
        f"Ten en cuenta {total_classes} clases en total."
    )

    return generate_chatgpt(prompt)


    # ==========================[Aplicación]=================================

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

principal_objetive = generate_course_objectives(course_name, course_level, course_focus, profile, specific_topics, course)

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


# ======================Generating Objetives=====================

print('Generating  Objectives .... 🤖')

secondary_objetives = generate_course_secondary_objectives(course_name, course_level, course_focus, profile, specific_topics, principal_objetive,course)

print("Objetivos secundarios generados:")
print('Escribiendo en Google Sheets .... ✍️')

# Dividir el texto en líneas
lines = secondary_objetives.strip().split('\n')

# Verificar que las líneas se están dividiendo correctamente
print(f"Total de líneas a procesar: {len(lines)}")

# Iterar sobre las líneas
for i, line in enumerate(lines, start=3):
    print(f"Procesando línea {i}")  # Impresión de depuración
    number_match = re.search(r'Numero\[(.*?)\]', line)
    name_match = re.search(r'Nombre\[(.*?)\]', line)
    description_match = re.search(r'Descripci[oó]n\[(.*?)\]', line)

    if number_match and name_match and description_match:
        print(f"Actualizando Google Sheets para la línea {i}")  # Más impresiones de depuración
        sheet3.update_cell(i, 3, name_match.group(1))
        sheet3.update_cell(i, 4, description_match.group(1))
    else:
        print(f"No se encontraron coincidencias en la línea {i}")  # Ayuda a identificar líneas problemáticas

print ('Done! ✅')

print('Generating Graduate Profile .... 🤖')
graduate_profile = generate_graduate_profile(course_name, target_audience, specific_topics, next_learning_unit, principal_objetive, secondary_objetives)


print ('Writting in Google Sheets .... ✍️ ')


sheet4.update_cell(1, 2, graduate_profile)

print ('Done! ✅') 

print('Generating Principal Habilities .... 🤖')

key_skills = generate_key_skills(course_name, target_audience, graduate_profile)

print (key_skills)

print('Writting in Google Sheets .... ✍️ ')
key_skills_lines = key_skills.split('\n')  # Dividir por líneas

for line in key_skills_lines:
    # Extraer número, nombre y descripción
    number_match = re.search(r'Numero\[(\d+)\]', line)
    name_match = re.search(r'Nombre\:\[(.*?)\]', line)
    # Ajuste en la expresión regular para capturar toda la descripción correctamente
    description_match = re.search(r'Descripcion:\[key\[(.*?)\]\]', line, re.DOTALL)
    
    if number_match and name_match and description_match:
        number = int(number_match.group(1))
        name = name_match.group(1)
        # Ajuste para limpiar la descripción, eliminando saltos de línea innecesarios y espacios extra
        description = " ".join(description_match.group(1).split())
        
        # Calcular la fila en Google Sheets
        name_row = 2 + number  # Los nombres comienzan en la fila 3
        description_row = name_row  # La descripción va en la misma fila que el nombre
        
        # Actualizar Google Sheets
        sheet4.update_cell(name_row, 1, name)  # Nombre en columna 1
        sheet4.update_cell(description_row, 2, description)  # Descripción en columna 2

print ('Done! ✅') 


print('Generating Course Syllabus .... 🤖')

syllabus = generate_course_syllabus(course_name, profile, course_focus, principal_objetive, course)

print (syllabus)

print ('Writting in Google Sheets .... ✍️ ')


