from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import httpx
import io

app = FastAPI()

PIXELCUT_API_URL = "https://api.pixelcut.ai/api/remove-background"

@app.post("/remover-fundo/")
async def remover_fundo(file: UploadFile = File(...)):
    # Lê a imagem enviada
    image_bytes = await file.read()

    # Faz a requisição para a API da Pixelcut
    async with httpx.AsyncClient() as client:
        response = await client.post(
            PIXELCUT_API_URL,
            files={"file": (file.filename, image_bytes, file.content_type)},
        )
        response.raise_for_status()
        result = response.content

    # Retorna a imagem final como PNG
    return StreamingResponse(io.BytesIO(result), media_type="image/png")
