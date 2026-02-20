from datetime import datetime, timezone

from flask import Flask, jsonify, request
from postgrest.exceptions import APIError

from db import get_supabase_client

app = Flask(__name__)

TABLE_NAME = "produtos_imagem"


def testar_supabase() -> str:
    """Executa uma query simples para validar conexão com o Supabase."""
    try:
        supabase = get_supabase_client()
        supabase.table(TABLE_NAME).select("id", count="exact").limit(1).execute()
        return "Supabase conectado com sucesso"
    except Exception as error:  # noqa: BLE001 - retornamos erro no healthcheck
        return f"Erro Supabase: {error}"


@app.route("/")
def home():
    return jsonify({"status": "API ativa", "supabase": testar_supabase()})


@app.get("/produtos")
def listar_produtos():
    supabase = get_supabase_client()

    response = (
        supabase.table(TABLE_NAME)
        .select("id,nome,slug,imagem_url,imagem_fundo_removido_url,origem,criado_em")
        .order("criado_em", desc=True)
        .execute()
    )

    return jsonify(response.data)


@app.post("/produtos")
def criar_produto():
    payload = request.get_json(silent=True) or {}

    required_fields = ["nome", "slug", "imagem_url"]
    missing_fields = [field for field in required_fields if not payload.get(field)]
    if missing_fields:
        return (
            jsonify(
                {
                    "erro": "Campos obrigatórios ausentes",
                    "campos": missing_fields,
                }
            ),
            400,
        )

    novo_produto = {
        "nome": payload["nome"],
        "slug": payload["slug"],
        "imagem_url": payload["imagem_url"],
        "imagem_fundo_removido_url": payload.get("imagem_fundo_removido_url"),
        "origem": payload.get("origem"),
        "criado_em": datetime.now(timezone.utc).isoformat(),
    }

    try:
        supabase = get_supabase_client()
        response = supabase.table(TABLE_NAME).insert(novo_produto).execute()
        return jsonify(response.data[0]), 201
    except APIError as error:
        return jsonify({"erro": "Falha ao inserir produto", "detalhes": error.message}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
