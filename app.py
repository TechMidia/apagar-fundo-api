from fastapi import FastAPI, File, UploadFile
from backgroundremover.bg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remover-fundo/")
async def remover_fundo(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    result = remove(image)
    
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    buf.seek(0)

    return {
        "status": "ok",
        "message": "Fundo removido com sucesso!"
        # Para testes com front, você pode base64-encodear aqui se quiser exibir a imagem direto.
    }
