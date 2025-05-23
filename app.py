from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from backgroundremover import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remover-fundo/")
async def remover_fundo(file: UploadFile = File(...)):
    # Lê a imagem enviada
    image = Image.open(io.BytesIO(await file.read()))

    # Remove o fundo
    result = remove(image)

    # Prepara buffer de resposta
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    buf.seek(0)

    # Retorna a imagem já processada
    return StreamingResponse(buf, media_type="image/png")
