import argparse
import dotenv
import time
import os
from helpers import encode_image
from openai_api import Api


def analyze_image():
    parser = argparse.ArgumentParser(
        description="Analyze an image to identify potential threats and safety objects."
    )
    parser.add_argument("image", help="Image to analyze")
    parser.add_argument(
        "--model", help="Openai model", default="gpt-4o-mini"
    )
    parser.add_argument(
        "--temperature", help="Temperature for sampling", default=0.7
    )
    parser.add_argument(
        "--stream", help="Use api streaming", action="store_true"
    )
    args = parser.parse_args()

    api = Api(model=args.model)

    questions = '''QUESTIONS:
    1. Which objects in the frame can be used as a weapon?
    2. Is there a crowd of people in the frame?
    3. How many / which objects in the frame are intended for safety?
    4. How many / which communication devices (phones, radios, etc.) are available?
    5. How many / which transportation mediums are available (car, bus, bike, etc.)?
    6. Is there adequate lighting to navigate safely?
    7. Estimate the total weight of any heavy objects (>1000 lbs) in the photo.

    After providing an answer to each question, please note any assumptions made in order to answer the question.
    '''

    system_prompt = '''
    You are a safety officer reporting on the quality of safety and potential threats in an image. 
    Your job is to identify objects in the image that both directly and indirectly relate to potential threats and safety. 
    Focus on objects like potential weapons, communication devices, people, and transportation, as well as objects that could have an underlying purpose of safety. 
    Assess the purpose of each object in the image and answer the following questions while keeping these considerations in mind.
    =================
    '''

    # Construct paths dynamically
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, args.image)
    riot_image_path = os.path.join(script_dir, 'data', 'riot.png')
    table_image_path = os.path.join(script_dir, 'data', 'table.jpg')

    image_url = f"data:image/png;base64,{encode_image(image_path)}"
    riot_url = f"data:image/png;base64,{encode_image(riot_image_path)}"
    table_url = f"data:image/png;base64,{encode_image(table_image_path)}"

    start_time = time.time()
    response = api.chat(
        messages=[
            {"role": "system", "content": system_prompt + questions},
            # few shot prompts
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": riot_url}}
            ]},
            {"role": "assistant", "content":
                '''
                1. The police officers are carrying batons or sticks that can be used as blunt force weapons. 
                    - Assumption: Weapons are any objects designed or intended to cause harm or injury.
                2. Yes, there is a crowd of over 20 police officers in the center of this image. 
                    - Assumption: A crowd consists of 3 or more people within close proximity of each other.
                3. The police officers are all wearing safety vests and helmets to protect them from threats. The police officers are also jumping over a barricade which is used to safely keep people in and out of certain areas. In the background, you can also see traffic lights used to control traffic safely. 
                    - Assumption: Safety objects are anything that can be used to help control or provide safety to participants in the image.
                4. There are no communication devices in the image. 
                    - Assumption: Communication devices include electronic devices like phones, radios, or computers or non-electronic methods of communication.
                5. There are no mediums of transportation visible, but there are likely some nearby as the image is set on the street. 
                    - Assumption: Transportation mediums include anything that can move people from place to place.
                6. Although it is dusk, there appears to be adequate lighting due to the bright sky and numerous street lights in the background. 
                    - Assumption: A bright sky indicates sufficient ambient lighting and external light sources also help.
                7. The concrete barrier weighs tens of thousands of pounds. 
                    - Assumption: Each segment of the concrete barricade weighs roughly 1500lbs.
                '''
            },
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": table_url}}
            ]},
            {"role": "assistant", "content":
                '''
                1. There are no obvious weapons in the scene.  The silverware could potentially be used as a weapon, but it is unlikely.
                    - Assumption: Weapons are any objects designed or intended to cause harm or injury.
                2. Yes, there is evidence of at least 4 people in the image.
                    - Assumption: A crowd consists of 3 or more people within close proximity of each other.
                3. There is a hand rail visible behind the table.
                    - Assumption: Safety objects are anything that can be used to keep people safe or protect them from harm.
                4. One man is using a mobile phone at the table.
                    - Assumption: Communication devices include electronic devices like phones, radios, or computers or non-electronic methods of communication.
                5. There are no mediums of transportation visible.
                    - Assumption: Transportation mediums include anything designed to move people from place to place.
                6. Although the lighting is low there appears to be adequate lighting due to the candles and ambient light in the room.
                    - Assumption: The scene is clearly visible indicating sufficient lighting to navigate safely.
                7. There are no objects in the scene that weigh over 1000 lbs.
                    - Assumption: The table visible in the image is the heaviest object in the scene and likely weighs less than 100 lbs.
                '''
            },
            # image to analyze
            {"role": "user", "content": [
                # {"type": "text", "content": questions},  #repeat questions?
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ],
        temperature = args.temperature,
        stream = args.stream
    )
    runtime = round(time.time() - start_time, 2)
    return response, runtime

if __name__ == "__main__":
    dotenv.load_dotenv()
    answer, runtime = analyze_image()
    print(answer)
    print(f"Runtime: {runtime} seconds")