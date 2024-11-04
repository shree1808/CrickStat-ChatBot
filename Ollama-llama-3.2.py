import gradio as gr
import json
import requests

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type' : 'application/json'
}

history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "".join(prompt)

    data = {
        "model":"llama3.2",
        "prompt" : final_prompt,
        "stream" : False 
    }

    response = requests.post(url, headers = headers, data = json.dumps(data))

    if response.status_code == 200:
        response = response.text
        data = json.loads(response)
        actual_response = data['response']
        return actual_response
    else:
        print('Error', response.text)

interface = gr.Interface(
    fn = generate_response,
    inputs = gr.Textbox(lines = 2, placeholder = 'Enter your prompt'),
    outputs = "text"
)

interface.launch()