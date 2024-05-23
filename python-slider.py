from pptx import Presentation
import openai
from config import api_key

openai.api_key = api_key


def generate_text(prompt):

    print(f"Prompt: {prompt}")

    messages = [
       
        {
            "role" : "user", "content" : prompt     
        },
    ]


    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Asegúrate de verificar el modelo disponible más reciente
        messages= messages,
        temperature= 0
    )
    return response.choices[0].message.content



def create_presentation(text, file_name="presentation.pptx"):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    
    title = slide.shapes.title
    content = slide.placeholders[1]

    title.text = "Generated Slide"
    content.text = text

    prs.save(file_name)
    print(f"Presentation saved as {file_name}")


def main():
    prompt = "Genera un texto para una presentación de powerPoint de una clase de con alumnos con pocos conociminetos en programación sobre Python con Pandas"
    generated_text = generate_text(prompt)
    print(f"Prompt: {prompt}")
    print(f"Generated text: {generated_text}")

    create_presentation(generated_text)

if __name__ == "__main__":
    main()
