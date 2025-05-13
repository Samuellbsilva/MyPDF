from flask import Flask
from routes.extrairtxt import extrairbp
from routes.resumirtxt import resumir_bp
from routes.analisar import analisar_bp
import os

app = Flask(__name__)

# Cria a pasta de uploads, caso ela ainda não exista
os.makedirs("uploads", exist_ok=True)

# Puxa os blueprints
app.register_blueprint(analisar_bp, url_prefix="/api")
app.register_blueprint(extrairbp, url_prefix="/api")
app.register_blueprint(resumir_bp, url_prefix="/api")

# roda a API
@app.route("/")
def home():
    return {"message": "API de Resumo de PDF ativa!"}

if __name__ == "__main__":
    app.run(debug=True)
