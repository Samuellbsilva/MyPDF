from flask import Blueprint, request, jsonify
import aspose.pdf as ap
import os
from werkzeug.utils import secure_filename

extrairbp = Blueprint('extrairtxt', __name__)

@extrairbp.route('/extrairtxt', methods=['POST'])
def extrair():
    # Verifica se o arquivo foi enviado
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400

    # Armazena o arquivo na pasta uploads
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)

    # Extrai o texto do PDF
    doc = ap.Document(filepath)
    txt_extraido = ""
    
    # Usando o TextAbsorber para extrair o texto de cada página
    text_absorber = ap.text.TextAbsorber()
    for page in doc.pages:
        page.accept(text_absorber)
        txt_extraido += text_absorber.text

    return jsonify({'texto': txt_extraido})
