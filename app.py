from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/remover-fundo', methods=['POST'])
def remover_fundo():
    if 'file' not in request.files:
        return {'erro': 'Arquivo não enviado'}, 400

    file = request.files['file']
    input_image = file.read()
    output_image = remove(input_image)

    return send_file(
        io.BytesIO(output_image),
        mimetype='image/png',
        as_attachment=False,
        download_name='sem_fundo.png'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
