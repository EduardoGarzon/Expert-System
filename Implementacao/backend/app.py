from flask import Flask, request, jsonify
from flask_cors import CORS
from clips_engine.motor_clips import processar_contrato
from gerador_html import gerar_html

app = Flask(__name__)
CORS(app)

@app.route('/gerar-contrato', methods=['POST'])
def gerar_contrato():
    try:
        dados_usuario = request.json
        resultado = processar_contrato(dados_usuario)

        html = gerar_html(resultado)

        return jsonify(html)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
