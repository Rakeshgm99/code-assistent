import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json'
}

history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "codeassisst",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        data = response.json()
        actual_response = data.get('response', '')
        history.append(actual_response)  # Save the generated response to the history
        return actual_response
    else:
        return f"Error: {response.status_code} - {response.text}"

css = """
body {
    background-color: #d4edda;
    font-family: Arial, sans-serif;
}

#input-container, #output-container {
    background-color: #f8d7da;
    border: 1px solid #721c24;
    padding: 20px;
    border-radius: 10px;
}

textarea {
    font-size: 16px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #721c24;
}

button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
}

#interface-title {
    text-align: center;
    font-size: 24px;
    color: #333333;
}
"""

interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your Prompt", label="Input"),
    outputs=gr.Textbox(label="Response"),
    title="AI Response Generator",
    description="Type your prompt in the input box and get a response from the AI model.",
    css=css
)

interface.launch()
