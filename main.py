import requests
import subprocess
import sys
import random
import string

def get_ai_code(project_description):
    prompt = "Kode Python Only"
    api_url = f"https://api.hy-tech.my.id/api/gemini/{prompt}:{project_description}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json().get('text')
    else:
        print("Failed to get code from AI.")
        return None

def create_project_file(code, file_name=None):
    code = code.replace("python", "").replace("```", "")
    if file_name is None:
        file_name = "result-+" + generate_random_name() + ".py"
    with open(file_name, 'w') as file:
        file.write(code)
    print(f"Project '{file_name}' created successfully.")
    install_required_libraries(code)
    subprocess.run(["python", file_name])

def generate_random_name(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def install_required_libraries(code):
    required_libraries = extract_libraries(code)
    for library in required_libraries:
        subprocess.run([sys.executable, "-m", "pip", "install", library])

def extract_libraries(code):
    lines = code.split('\n')
    libraries = []
    for line in lines:
        if line.startswith('import'):
            library = line.split(' ')[1]
            libraries.append(library)
        elif line.startswith('from'):
            library = line.split(' ')[1]
            libraries.append(library)
    return libraries

def main():
    project_description = input("Explain about your project: ")
    ai_code = get_ai_code(project_description)
    if ai_code:
        create_project_file(ai_code)

if __name__ == "__main__":
    main()
