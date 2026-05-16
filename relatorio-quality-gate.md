# Relatório — AI Security Quality Gate (Desafio 1)

> **Aviso ético:** Payloads, comandos e testes deste relatório são **exclusivos** para o agente-alvo do hackathon Segurança Cibernética, em ambiente local isolado. Não utilizar em produção, sistemas de terceiros ou outras equipes. No Brasil, acesso não autorizado a dispositivo alheio é crime (Lei 12.737/2012).

## Resumo executivo

| Campo | Valor |
|-------|-------|
| Artefato avaliado | `pr-inseguro.diff` |
| Agente | Tutor de Programação (Python + Flask) |
| **Decisão do gate** | **BLOCK** |
| Regras violadas | QG-001 a QG-008 (todas aplicáveis) |
| OWASP LLM | LLM01, LLM06, LLM07 |

## Contexto

A equipe recebeu o código baseline em `agente-alvo/` (somente leitura) e um PR simulado de *vibe coding* que altera a tool `executar_python` para priorizar flexibilidade pedagógica em detrimento de controles de segurança. O PR não foi mergeado no repositório entregue; a análise combina revisão estática do diff e PoCs em worktree `poc-pr-inseguro` (branch `pr-vibe-inseguro`).

## Metodologia

1. Inventário estático linha a linha do diff (`evidencias/quality-gate-output.md`, E-001–E-009).
2. PoCs dinâmicos em worktree isolada (`run_pocs.py`, pytest).
3. PoC de integração LLM01 via `POST /chat` (stub Flask).
4. Verificação lógica LLM06 do caminho de erro pós-PR.
5. Regras normativas em `quality-gate-rules.md`.

## Achados principais

### LLM07 — Insecure Plugin Design (CRITICAL)

O PR substitui execução subprocess restrita por três caminhos perigosos:

- **eval** para expressões de uma linha (`pr-inseguro.diff`, linhas 91-98).
- **exec** com builtins completos (linhas 134-136).
- **subprocess** com `shell=True` sem timeout (linhas 106-114).

**PoCs reproduzidos:** E-001 (stdout `EVAL_POC`), E-002 (`EXEC_POC` via exec), E-003 (`SHELL_POC`), E-006 (bypass com `debug=True`).

**Impacto:** execução arbitrária no processo do servidor — equivalente a RCE no contexto do tutor.

### LLM06 — Sensitive Information Disclosure (HIGH)

O PR adiciona `system_prompt_dump={prompt_full}` na mensagem de `RuntimeError` em `orchestrator.py` (diff linhas 12-16), expondo instruções internas e possivelmente tokens fictícios do prompt.

**Evidência:** estática + simulação no worktree (`HAS_DUMP True`).

### LLM01 — Prompt Injection (MEDIUM-HIGH)

- Descrição da tool no PR incentiva uso agressivo ("use sem hesitar") — E-008.
- Baseline B-B2: filtro de mensagem só na primeira linha; PoC com injeção na linha 2 ainda acionou tool via stub.

## Severidade e mitigação

| Achado | Severidade | Mitigação recomendada |
|--------|------------|------------------------|
| eval/exec/shell | CRITICAL | Remover eval/exec; subprocess sem shell; timeout; sandbox (container/wasm) |
| Sem timeout/allowlist | HIGH | Restaurar `EXEC_TIMEOUT_SEC` e `_validate_code` |
| debug bypass | HIGH | Remover flag `debug` que ignora sanitize; logs redigidos |
| system_prompt_dump | HIGH | Erro genérico ao cliente; log interno sem prompt completo |
| Tool description | MEDIUM-HIGH | Descrição com limites explícitos; negar parâmetros perigosos no schema |
| Teste removido | MEDIUM | Restaurar e ampliar testes adversariais (`__import__`, shell, eval) |

## Risco residual (baseline)

Mesmo sem o PR, o baseline apresenta B-B3 (`__import__('os')`) e B1/B4 (vazamento em erros). Isso **não** justifica aprovar o PR — o diff **piora** materialmente o perfil de risco.

## Conclusão

Recomenda-se **BLOCK** do `pr-inseguro.diff` até implementação das correções acima e re-execução do quality gate com evidências de re-teste.

## Anexos

- `quality-gate-rules.md`
- `evidencias/quality-gate-output.md`
- `pr-inseguro.diff`
