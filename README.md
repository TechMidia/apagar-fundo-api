# apagar-fundo-api

API Flask inicial para cadastro e consulta de produtos com imagens, usando **Supabase** como base de dados.

## Requisitos

- Python 3.11+
- Projeto Supabase criado
- Tabela `produtos_imagem` criada no banco

## Variáveis de ambiente

Crie um arquivo `.env` com:

```env
SUPABASE_URL=https://<seu-projeto>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<sua-service-role-key>
# opcional como fallback:
# SUPABASE_ANON_KEY=<sua-anon-key>
```

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Rodando localmente

```bash
flask --app app run --host 0.0.0.0 --port 8080
```

## Endpoints

- `GET /` → healthcheck da API e conexão Supabase
- `GET /produtos` → lista produtos ordenados por data de criação (mais novos primeiro)
- `POST /produtos` → cria produto

### Exemplo de payload `POST /produtos`

```json
{
  "nome": "Cafeteira Elétrica",
  "slug": "cafeteira-eletrica",
  "imagem_url": "https://cdn.exemplo.com/cafeteira.jpg",
  "imagem_fundo_removido_url": "https://cdn.exemplo.com/cafeteira-sem-fundo.png",
  "origem": "upload-manual"
}
```

## SQL sugerido para o Supabase

```sql
create extension if not exists "pgcrypto";

create table if not exists public.produtos_imagem (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  slug text not null unique,
  imagem_url text not null,
  imagem_fundo_removido_url text,
  origem text,
  criado_em timestamptz not null default now()
);
```
