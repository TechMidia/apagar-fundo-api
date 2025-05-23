from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from backgroundremover import remove
import io

app = FastAPI()

@app.post("/remover-fundo/")
async def remover_fundo(file: UploadFile = File(...)):
    # Lê o arquivo enviado
    image = Image.open(io.BytesIO(await file.read()))

    # Remove o fundo da imagem
    result = remove(image)

    # Salva a imagem em um buffer
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    buf.seek(0)

    # Retorna como uma resposta de streaming (imagem diretamente)
    return StreamingResponse(buf, media_type="image/png")
