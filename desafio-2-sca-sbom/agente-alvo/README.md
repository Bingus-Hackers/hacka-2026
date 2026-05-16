# Agente Bancário — Banco Digital Hackathon

Agente-alvo do **Desafio 2** (Hackathon Segurança Cibernética). Assistente bancário educacional em Java + Spring Boot.

> **Atenção (participantes):** este diretório é **somente leitura**. Não modifique `agente-alvo/`. O escopo do Desafio 2 é análise de dependências com **Trivy** e **SBOM CycloneDX**.

## Requisitos

- Java 17+
- Maven (incluído: `./mvnw`)

## Instalação e execução

```bash
cd agente-alvo
./mvnw spring-boot:run
```

Modo demo: `banco.use-llm-stub=true` em `application.yml` (padrão).

## Endpoints

- `GET /health` — status do serviço
- `POST /api/chat` — `{"message": "...", "session_id": "opcional"}`
- `POST /api/tools` — lista schemas das tools fictícias

Exemplo:

```bash
curl -s http://127.0.0.1:8080/health
curl -s -X POST http://127.0.0.1:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explique PIX limite"}'
```

## Estrutura

| Caminho | Descrição |
|---------|-----------|
| `pom.xml` | **Artefato central do Desafio 2** — dependências Maven |
| `briefing-agente.md` | Contexto de negócio |
| `CONTRATOS.md` | APIs e tools |
| `data/faq-bancario/` | FAQ fictício |
| `logs/` | Tentativas de exploração (narrativa) |

## Desafio 2

Use Trivy e SBOM conforme [`../README.md`](../README.md). Não é necessário auditar código linha a linha.

Uso exclusivamente educacional — Hackathon Segurança Cibernética.
