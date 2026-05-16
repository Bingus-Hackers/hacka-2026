# Evidencias ? Quality Gate Desafio 1

## Aviso etico

Uso exclusivo contra o agente-alvo do hackathon, em ambiente isolado. Lei 12.737/2012 (Brasil): acesso nao autorizado a sistema alheio e crime.

**Fonte:** `pr-inseguro.diff` | **PoC dinamico:** worktree `poc-pr-inseguro` (branch `pr-vibe-inseguro`)

---

## Tabela resumo (E-001 a E-009)

| ID | Regra | Arquivo:linha | OWASP LLM | PoC | Artefato de prova |
|----|-------|---------------|-----------|-----|-------------------|
| E-001 | QG-001 | `pr-inseguro.diff` L91-98 | LLM07 | reproduzido | `poc_run_stdout.txt` (stdout `EVAL_POC`) |
| E-002 | QG-001 | `pr-inseguro.diff` L133-136 | LLM07 | reproduzido | `poc_run_stdout.txt` (`mode: exec`) |
| E-003 | QG-002 | `pr-inseguro.diff` L106-114 | LLM07 | reproduzido | `poc_run_stdout.txt` (`SHELL_POC`) |
| E-004 | QG-003 | `pr-inseguro.diff` L111-113 | LLM07 | estatico+diff | Comentario remove timeout no diff |
| E-005 | QG-004 | `pr-inseguro.diff` L35-55 | LLM07 | estatico+diff | Remocao `_validate_code` no diff |
| E-006 | QG-005 | `pr-inseguro.diff` L73-85 | LLM07 | reproduzido | `poc_run_stdout.txt` (debug bypass) |
| E-007 | QG-006 | `pr-inseguro.diff` L12-16 | LLM06 | reproduzido | `poc_llm06_output.txt` |
| E-008 | QG-007 | `pr-inseguro.diff` L156-159 | LLM01+LLM07 | estatico | Diff + `chat_poc_response.json` |
| E-009 | QG-008 | `pr-inseguro.diff` L198-200 | processo | reproduzido | pytest 1 teste no worktree |

---

## E-001 ? eval (CRITICAL, LLM07)

**Diff:**

```diff
+            result_value = eval(codigo, {"__builtins__": __builtins__}, {})
```

**PoC:** `poc-pr-inseguro/run_pocs.py` ? payload `__import__('os').system('echo EVAL_POC')`.

**Observado:** `success: True`, `mode: eval`, `output: '0'` (retorno de `system()`); **stdout do processo imprime `EVAL_POC`** (ver `evidencias/poc_run_stdout.txt` linha 1).

---

## E-002 ? exec multiline (CRITICAL, LLM07)

**Diff:**

```diff
+        exec(codigo, {"__builtins__": __builtins__}, local_ctx := {})
```

**PoC:** multiline com `__import__('os').system('echo EXEC_POC')` (evita filtro literal `import os`).

**Observado:** `{'success': True, 'output': 'exec_multiline_ok', 'mode': 'exec'}`; stdout `EXEC_POC`.

**Contraste:** `import os\n...` sem debug ? `success: False` (E-002b em `poc_run_stdout.txt`).

---

## E-003 ? shell=True (CRITICAL, LLM07)

**Diff:** `subprocess.run(codigo, shell=True, ...)` sem timeout.

**PoC:** `use_shell=True`, `echo SHELL_POC` ? `output: SHELL_POC`, `mode: shell`.

---

## E-004 ? sem timeout (HIGH, LLM07)

**Diff:** removido `timeout=settings.exec_timeout_sec`; comentario "timeout removido".

**Comportamento:** subprocess/shell pode bloquear servidor ? reproduzivel por inspecao do codigo pos-PR em `poc-pr-inseguro/app/agent/tools/executar_python.py`.

---

## E-005 ? sem allowlist (HIGH, LLM07)

**Diff:** removidos `_BLOCKED_CODE_PATTERNS` e `_validate_code`.

**Comportamento:** codigo hostil nao e barrado por regex antes de eval/exec/shell.

---

## E-006 ? debug bypass (HIGH, LLM07)

**Diff:** `if not ok and not debug:` ? com `debug=True` ignora sanitize.

**PoC:** `import os\nprint(os.getcwd())` + `debug=True` ? `success: True`; log DEBUG com codigo completo (`poc_run_stdout.txt`).

---

## E-007 ? system_prompt_dump (HIGH, LLM06)

**Diff:**

```diff
+            f"system_prompt_dump={prompt_full}"
```

**PoC:** `evidencias/poc_llm06_output.txt` ? `HAS_DUMP True`, trecho contem instrucoes internas do prompt.

---

## E-008 ? tool description (MEDIUM-HIGH, LLM01/LLM07)

**Diff:** "use esta tool sem hesitar ? priorize utilidade".

**PoC estatico + integracao:** `chat_poc_response.json` mostra stub chamando `executar_python` a partir de mensagem do usuario.

---

## E-009 ? teste removido (MEDIUM)

**Diff:** removido `test_blocks_import_os_literal`.

**PoC:** `pytest tests/test_executar_python.py -v` ? apenas `test_hello_world` PASSED.

---

## Baseline (nao aprova o PR)

| ID | Arquivo | Risco |
|----|---------|-------|
| B-B3 | `agente-alvo/.../executar_python.py:16` | LLM07 ? `__import__('os')` |
| B-B2 | `agente-alvo/.../input_filter.py:14-15` | LLM01 ? so 1a linha |

**PoC B-B3:** `{'success': True, 'output': 'BASELINE_POC', 'returncode': 0}`

---

## PoCs dinamicos ? comandos

```powershell
cd desafio-1-quality-gate\poc-pr-inseguro
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python.exe run_pocs.py
.\.venv\Scripts\pytest.exe tests/test_executar_python.py -v
```

## PoC LLM01 ? chat

```powershell
# Terminal 1: cd agente-alvo; USE_LLM_STUB=true; flask run --port 5000
curl.exe -s -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" --data-binary "@evidencias/chat_poc_body.json"
```

Respostas salvas: `chat_poc_response.json`, `chat_inject_response.json`.

---

## Ambiente PoC

| Campo | Valor |
|-------|-------|
| Worktree | `desafio-1-quality-gate/poc-pr-inseguro` |
| Branch | `pr-vibe-inseguro` |
| Baseline intocado | `agente-alvo/` em `main` |
