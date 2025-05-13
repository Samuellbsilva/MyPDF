from flask import Blueprint, request, jsonify
import aspose.pdf as ap
import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

resumir_bp = Blueprint('resumir_pdf', __name__)

HUGGINGFACE_API_URL = os.getenv("HUGGINGFACE_API_URL")
API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

headers = {"Authorization": f"Bearer {API_TOKEN}"}


def extrair_texto(file_path):
    doc = ap.Document(file_path)
    texto_extraido = ""
    for page in doc.pages:
        text_absorber = ap.text.TextAbsorber()
        page.accept(text_absorber)
        texto_extraido += text_absorber.text
    return texto_extraido.strip()

@resumir_bp.route('/resumirpdf', methods=['POST'])
def resumirpdf():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    pdf = request.files['file']
    if not pdf.filename.endswith('.pdf'):
        return jsonify({"error": "Formato inválido. Envie um PDF."}), 400

    rotatemp = os.path.join("uploads", f"{uuid.uuid4().hex}.pdf")
    pdf.save(rotatemp)

    try:
        texto = extrair_texto(rotatemp)

        if len(texto) == 0:
            return jsonify({"error": "Texto vazio extraído do PDF."}), 400

        payload = {"inputs": texto}
        resposta = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)

        if resposta.status_code != 200:
            return jsonify({"error": "Erro na API da Hugging Face", "detalhes": resposta.text}), 500

        resumo = resposta.json()[0]['summary_text']
        return jsonify({"resumo": resumo})

    finally:
        os.remove(rotatemp)
