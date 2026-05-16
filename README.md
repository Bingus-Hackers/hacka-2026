# Desafio 1 

Materiais entregues pela comissão para o Hackathon Segurança Cibernética.

## Conteúdo

| Artefato | Descrição |
|----------|-----------|
| [`agente-alvo/`](agente-alvo/) | Tutor de Programação (Python + Flask) — **somente leitura** |
| [`pr-inseguro.diff`](pr-inseguro.diff) | PR simulado |

## Tarefa da equipe

1. Auditar o código em `agente-alvo/` e o diff `pr-inseguro.diff`
2. Construir quality gate (`quality-gate-rules.md`, relatório, evidências) na estrutura do projeto hackathon
3. Decidir **APPROVE** ou **BLOCK** com evidências reproduzíveis

**Não modifique** `agente-alvo/`. **Não aplique** o diff no repositório entregue — use-o como artefato de revisão.

## Início rápido (explorar o agente)

```bash
cd agente-alvo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app run:app run --port 5000
```
