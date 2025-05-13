from flask import Blueprint, request, jsonify , Response
import os
import uuid
import requests
import aspose.pdf as ap

analisar_bp = Blueprint('analisar', __name__)

# Substitua pela sua chave da Hugging Face
HUGGINGFACE_API_URL = os.getenv("HUGGINGFACE_API_URL")
API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Função para extrair texto do PDF
def extrair_texto_pdf(caminho_pdf):
    doc = ap.Document(caminho_pdf)
    texto_extraido = ""
    for page in doc.pages:
        text_absorber = ap.text.TextAbsorber()
        page.accept(text_absorber)
        texto_extraido += text_absorber.text
    return texto_extraido.strip()
# Rota principal para análise do PDF
@analisar_bp.route('/analisarpdf', methods=['POST'])
def analisar_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'Arquivo PDF não enviado.'}), 400

    arquivo = request.files['file']
    if not arquivo.filename.endswith('.pdf'):
        return jsonify({'error': 'Formato inválido. Envie um PDF.'}), 400

    caminho_temporario = os.path.join('uploads', f"{uuid.uuid4().hex}.pdf")
    arquivo.save(caminho_temporario)
    try:
        texto = extrair_texto_pdf(caminho_temporario)
        if not texto:
            return jsonify({'error': 'Nenhum texto extraído do PDF.'}), 400

        prompt = f"""
        Você é um assistente de dados. Analise o seguinte conteúdo extraído de um PDF e gere insights úteis:

        \"\"\"
        {texto}
        \"\"\"

        Responda com um texto estruturado contendo:
        - Um resumo geral
        - Padrões ou tendências detectadas
        - Alertas ou pontos críticos
        - Principais tópicos abordados
        """

        resposta = requests.post(
            HUGGINGFACE_API_URL,
            headers=HEADERS,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 512}}
        )

        if resposta.status_code != 200:
            return jsonify({"error": "Erro ao acessar Hugging Face", "detalhes": resposta.text}), 500
        print(resposta.json())
        output = resposta.json()
        print(output)
        texto_gerado = output[0].get('generated_text', '').strip()
        print(texto_gerado)
        return Response(texto_gerado, status=200, mimetype='text/plain')
    finally:
        os.remove(caminho_temporario)
