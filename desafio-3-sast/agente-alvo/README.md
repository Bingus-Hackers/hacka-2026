# Assistente Jurídico — LexAssist Hackathon

Agente-alvo do **Desafio 3** (Hackathon Segurança Cibernética). Assistente jurídico educacional em Python + FastAPI.

## Início rápido

```bash
cd agente-alvo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/gerar_contrato_demo_pdf.py
python run.py
```

Em outro terminal:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Resuma o contrato contrato-demo.pdf"}'
```

## Testes

```bash
pytest -q
```

## Estrutura

- `app/` — FastAPI, orquestrador, tools
- `data/contratos/` — PDFs de demonstração
- `prompts/system_prompt.txt` — instruções do agente
- `logs/` — tentativas de indirect injection (fictícias)

Uso exclusivamente educacional — Hackathon Segurança Cibernética.
