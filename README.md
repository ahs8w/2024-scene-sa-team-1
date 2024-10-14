# 2024-scene-sa-team-1

Members: Adam Schiller, Samet Arda, Ethan Evans

## Installation instructions:

```
# create a virtual environment (recommended)
python -m venv .venv
# activate the virtual environment 
source .venv/bin/activate
# install all dependencies for local development
pip install -r requirements.txt
# create/populate .env for secrets
touch .env
echo OPENAI_API_KEY=<openai api key> >> .env
```

## Run CLI:
```
# show available cli arguments
python cli.py --help
# run sample
python cli.py data/train.jpg
```

## Challenge Instructions
[slide deck](https://boozallen.sharepoint.com/:p:/r/teams/CTONavaroliTeam/_layouts/15/doc2.aspx?action=edit&file=DS%20Challenge%201%20-%20Kickoff.pptx&mobileredirect=true&sourcedoc=%7B2A637790-6D17-4D70-94EA-2429E715E815%7D)

Develop an innovative AI program that can analyze any given image scene and provide critical insights about potential threats and safety considerations. ​

### ​Input: ​
- Image of an environment​
- Questions about safety and potential threats​
    1. Which objects in the frame can be used as a weapon?​
    2. Is there a crowd of people in the frame?​
    3. How many / which objects in the frame are intended for safety?​
    4. How many / which communication devices (phones, radios, etc.) are available?​
    5. How many / which transportation mediums are available (car, bus, bike, etc.)?​
    6. Is there adequate lighting to navigate safely?​
    7. Estimate the total weight of any heavy objects (>1000 lbs) in the photo.​

### Outputs: ​
- Answers to 7 questions for each image​
- Report the runtime to answer questions for each image​
- Define set of assumptions your program makes for each question​

### ​Key Objectives:​
- Create a versatile algorithm capable of processing diverse visual inputs​
- Design a robust system to answer predefined questions consistently​
- Demonstrate the ability to extract relevant safety information from visual data​
- Showcase your creative problem-solving skills in AI and computer vision​

### Sample Output format:​​
Image 1:​​
1. Knife​​
2. Yes​
3. Traffic Light: 1​, Stop Sign: 2​  
...  

Assumptions​
1. Weapons consist of knives, guns and long slim objects. ​
2. A crowd exists if 3 or more humans are within 5 feet of each other.​
3. Safety objects are constrained to objects that keep people safe around roads / vehicles.  
...  