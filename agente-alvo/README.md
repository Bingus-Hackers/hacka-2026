# Tutor de Programação — CodeMentor Campus

Agente-alvo do **Desafio 1** (Hackathon Segurança Cibernética). Assistente educacional em Python + Flask para alunos de introdução a Python.

> **Atenção (participantes):** este diretório é **somente leitura**. Não modifique `agente-alvo/`. Audite o código baseline e o arquivo `../pr-inseguro.diff`.

## Requisitos

- Python 3.11+
- pip

## Instalação e execução

```bash
cd agente-alvo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export FLASK_APP=run:app
flask run --port 5000
```

Modo offline (padrão): `USE_LLM_STUB=true` no `.env`.

## Endpoints

- `GET /health` — status do serviço
- `POST /chat` — `{"message": "...", "session_id": "opcional"}`

Exemplo:

```bash
curl -s http://127.0.0.1:5000/health
curl -s -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explique list comprehensions"}'
```

## Estrutura

| Pasta/arquivo | Descrição |
|---------------|-----------|
| `app/agent/tools/executar_python.py` | Tool de execução de código (foco do PR) |
| `prompts/system_prompt.txt` | Instruções internas do agente |
| `data/exercicios/` | Dataset fictício educacional |
| `logs/exploit-attempts.jsonl` | Histórico de tentativas de exploração |
| `CONTRATOS.md` | Contratos de API e tools |

## Testes

```bash
pytest tests/ -q
```

## Docker (opcional)

```bash
docker compose up --build
```

## Licença

Uso exclusivamente educacional — Hackathon Segurança Cibernética.
