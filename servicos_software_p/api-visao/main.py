import os
import uuid
import cv2
from collections import Counter
from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO

app = Flask(__name__)

UPLOAD_DIR = 'uploads'
OUTPUT_DIR = 'output'

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

model = YOLO('yolov8n.pt')

@app.route('/')
def home():
    return 'API de visão com YOLO ativa'

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada no campo "image"'}), 400
    
    file = request.files['image']

    if file.filename =='':
        return jsonify({'error': 'Arquivo vazio'}), 400
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext == '':
        ext = '.jpg'

    unique_name = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f'{unique_name}{ext}')
    output_path = os.path.join(OUTPUT_DIR, f'{unique_name}.jpg')

    file.save(input_path)

    results = model(input_path)

    annotated = results[0].plot()
    cv2.imwrite(output_path, annotated)

    if results[0].boxes is not None and len(results[0].boxes) > 0:
        class_ids = results[0].boxes.cls.tolist()
        detections = [results[0].names[int(i)] for i in class_ids]
    else:
        detections = []

    if not detections:
        texto_final = "nenhum objeto detectado"
    else:
        counts = Counter(detections)

    resultado_formatado = []
    for classe, qtd in counts.most_common():
        resultado_formatado.append(f"{classe}: {qtd}")

    texto_final = "\n".join(resultado_formatado)

    return jsonify({
        "image_url": f"/output/{unique_name}.jpg",
        "detections": texto_final
    })
  
@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
