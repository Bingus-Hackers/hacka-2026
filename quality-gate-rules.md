# AI Security Quality Gate — Tutor de Programação

> **Aviso etico:** Regras e testes aplicam-se somente ao agente-alvo do hackathon, em ambiente isolado (Lei 12.737/2012).

## Escopo

Avalia o merge do artefato `pr-inseguro.diff` no agente **Tutor de Programação** (CodeMentor Campus). Foco: tool `executar_python`, schema em `registry.py`, tratamento de erros em `orchestrator.py` e testes de segurança.

**Fora do escopo:** correção do código em `agente-alvo/` (read-only no hackathon).

## Decisão automática

| Resultado | Condição |
|-----------|----------|
| **BLOCK** | Uma ou mais regras CRITICAL/HIGH abaixo violadas pelo PR |
| **APPROVE** | Nenhuma regra BLOCK violada (não aplicável a este PR) |

**Decisão desta auditoria: BLOCK**

## Regras de bloqueio

### QG-001 — Proibição de eval/exec dinâmico

- **BLOCK** se o PR introduz `eval(` ou `exec(` sobre código originado de usuário ou LLM, com `__builtins__` completos.
- **OWASP:** LLM07 — Insecure Plugin Design
- **Evidências:** E-001, E-002

### QG-002 — Proibição de shell=True

- **BLOCK** se `subprocess.run(..., shell=True)` processa entrada controlável sem sandbox.
- **OWASP:** LLM07
- **Evidências:** E-003

### QG-003 — Timeout obrigatório

- **BLOCK** se remove `timeout=` (ou equivalente) de execução de código sem substituto documentado.
- **OWASP:** LLM07
- **Evidências:** E-004

### QG-004 — Validação e allowlist

- **BLOCK** se remove `_validate_code`, regex de padrões bloqueados ou allowlist sem controles equivalentes.
- **OWASP:** LLM07
- **Evidências:** E-005

### QG-005 — Bypass de sanitização

- **BLOCK** se parâmetro (`debug`) permite ignorar `sanitize_tool_code` ou loga código completo do usuário.
- **OWASP:** LLM07
- **Evidências:** E-006

### QG-006 — Vazamento de system prompt

- **BLOCK** se expõe `system_prompt_dump` ou prompt completo em erros visíveis ao cliente.
- **OWASP:** LLM06 — Sensitive Information Disclosure
- **Evidências:** E-007

### QG-007 — Tool schema seguro

- **BLOCK** se a descrição da tool incentiva uso irrestrito ("sem hesitar", máxima flexibilidade) sem guardrails.
- **OWASP:** LLM01 (Prompt Injection), LLM07
- **Evidências:** E-008

### QG-008 — Testes adversariais

- **BLOCK** se remove teste de segurança (`test_blocks_import_os_literal`) sem testes equivalentes.
- **Evidências:** E-009

## Matriz resumo

| Regra | PR viola? | Severidade | Decisão parcial |
|-------|-----------|------------|-----------------|
| QG-001 | Sim | CRITICAL | BLOCK |
| QG-002 | Sim | CRITICAL | BLOCK |
| QG-003 | Sim | HIGH | BLOCK |
| QG-004 | Sim | HIGH | BLOCK |
| QG-005 | Sim | HIGH | BLOCK |
| QG-006 | Sim | HIGH | BLOCK |
| QG-007 | Sim | MEDIUM-HIGH | BLOCK |
| QG-008 | Sim | MEDIUM | BLOCK |

## Risco residual (baseline — não aprova o PR)

| ID | Descrição |
|----|-----------|
| B-B3 | `__import__('os')` contorna filtro literal no baseline |
| B-B2 | Filtro de chat apenas na primeira linha |

O PR **agrava** a superfície (eval/exec/shell, dump de prompt, remoção de testes).

## Referências

- Evidências: `evidencias/quality-gate-output.md`
- Artefato: `pr-inseguro.diff`
- OWASP Top 10 for LLM Applications 2025 (LLM01, LLM06, LLM07)
