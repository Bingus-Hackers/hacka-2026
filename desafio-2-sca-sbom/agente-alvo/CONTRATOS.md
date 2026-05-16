# Contratos — Agente Bancário (Desafio 2)

Documento de interfaces do `agente-alvo/`. O Desafio 2 avalia **dependências** (`pom.xml`), não estes endpoints — servem apenas como contexto.

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `BANCO_USE_LLM_STUB` | Não (default via YAML `true`) | Respostas determinísticas offline |
| `OPENAI_API_KEY` | Não | Chave fake em `.env.example` |
| `ADMIN_TOKEN` | Não | Token administrativo fictício |

## Rotas HTTP

### `GET /health`

```json
{"status": "ok", "agent": "agente-bancario", "version": "1.0.0-baseline"}
```

### `POST /api/chat`

Corpo:

```json
{
  "message": "string (obrigatório)",
  "sessionId": "string (opcional)"
}
```

Resposta `200`:

```json
{
  "sessionId": "uuid",
  "reply": "string",
  "toolsUsed": [{"name": "string", "result_preview": "string"}]
}
```

### `POST /api/tools`

Lista schemas das tools (formato simplificado).

## Tools

### `consultar_saldo`

Parâmetros: `conta_id` (ex.: `DEMO-001`, `VIP-100`)

### `explicar_pix`

Parâmetros: `topico` (ex.: `limite`, `chave`, `geral`)

### `buscar_faq`

Parâmetros: `pergunta` — busca textual em `data/faq-bancario/*.md`

## Dependências (escopo SCA)

Arquivo principal: **`pom.xml`**. Equipes devem correlacionar CVEs do Trivy com coordenadas Maven `groupId:artifactId:version`.
