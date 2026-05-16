# Logs de exploração — Tutor de Programação

Arquivo `exploit-attempts.jsonl`: uma linha JSON por tentativa registrada no ambiente de testes da comissão.

## Campos

| Campo | Descrição |
|-------|-----------|
| `timestamp` | ISO-8601 UTC |
| `session_id` | Identificador da sessão |
| `user_message` | Mensagem do usuário (atacante simulado) |
| `tool_called` | Tool invocada, se houver |
| `tool_args_preview` | Prévia dos argumentos |
| `outcome` | `blocked`, `partial` ou `leaked` |
| `notes` | Observação técnica |

## Uso no Desafio 1

Correlacione entradas com vulnerabilidades no baseline (`B1`–`B5`) e com riscos introduzidos no `pr-inseguro.diff` (LLM01, LLM06, LLM07).
