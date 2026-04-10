import os
import tempfile
import requests
import gradio as gr

BACKEND_URL = os.getenv('BACKEND_URL', 'http://api-visao:8081')

def detectar_objetos(image, confidence):
    if image is None:
        return None, 'Nenhuma imagem enviada'
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        image.save(tmp.name)
        temp_path = tmp.name

    with open(temp_path, "rb") as f:
        files = {"image": f}
        data = {"confidence": confidence}
        response = requests.post(f"{BACKEND_URL}/detect", files=files, data=data)

    os.remove(temp_path)

    if response.status_code != 200:
        return None, f'Erro no backend: {response.text}'
    
    data = response.json()
    image_url = data['image_url']
    detections = data['detections']

    full_image_url = f'{BACKEND_URL}{image_url}'
    img_response = requests.get(full_image_url, stream=True)

    if img_response.status_code != 200:
        return None, 'Não foi possível baixar a imagem processada.'
    
    output_tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    for chunk in img_response.iter_content(chunk_size=8192):
        output_tmp.write(chunk)
    output_tmp.close()

    texto = "Objetos detectados:\n" + detections

    return output_tmp.name, texto

demo = gr.Interface(
    fn=detectar_objetos,
    inputs=[
        gr.Image(
            type="pil",
            sources=["upload"],
            label="Envie uma imagem"
        ),
        gr.Slider(0.1, 0.9, value=0.4, step=0.05, label="Nível de detecção")
    ],
    outputs=[
        gr.Image(type="filepath", label="Imagem processada"),
        gr.Textbox(label="Resultado")
    ],
    title='Detector de Objetos com YOLO',
    description='Envie uma imagem para detectar objetos via API REST.'
)

if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0', server_port=7861)