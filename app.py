from fastapi import FastAPI, File, UploadFile
from backgroundremover import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remover-fundo/")
async def remover_fundo(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    result = remove(image)
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    return {"status": "ok"}
