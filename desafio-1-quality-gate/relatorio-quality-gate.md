# Relatório de AI Security Quality Gate

## ⚠️ Disclaimer Ético e Legal

> [!IMPORTANT]
> Os payloads e vulnerabilidades identificados neste relatório são exclusivamente para fins educacionais e de auditoria dentro do ambiente controlado do hackathon.
> O uso destas técnicas contra sistemas de produção ou sem autorização explícita é ilegal e sujeito às penalidades da **Lei 12.737/2012 (Lei Carolina Dieckmann)**, que tipifica crimes de invasão de dispositivo informático.

---

## 1. Resumo da Decisão

| Item | Status |
|------|--------|
| **Veredito Final** | 🔴 **BLOCK (BLOQUEADO)** |
| **Severidade** | Crítica |
| **Principais Riscos** | RCE (Execução Remota de Código), Vazamento de System Prompt, DoS |

---

## 2. Evidências Técnicas e Achados

### 2.1 Vazamento de System Prompt (LLM06)
- **Arquivo:** `app/agent/orchestrator.py`
- **Linhas (Pós-PR):** 79-83
- **Comportamento:** O PR altera o tratamento de exceções para carregar e exibir o system prompt completo na resposta de erro (`system_prompt_dump=prompt_full`).
- **Impacto:** Permite que qualquer usuário obtenha as instruções internas e lógica de negócio do agente provocando um erro proposital.

### 2.2 Execução Remota de Código - RCE (LLM07)
- **Arquivo:** `app/agent/tools/executar_python.py`
- **Linhas (Pós-PR):** 32 (Backdoor), 50 (Eval), 67 (Shell=True), 80 (Exec)
- **Comportamento:** 
    1. Introdução de `eval()` e `exec()` com acesso total a `__builtins__`.
    2. Adição de `subprocess.run` com `shell=True`, permitindo injeção de comandos do S.O.
    3. Criação de uma flag de `debug` que desabilita o filtro de sanitização (Linha 32).
- **Impacto:** Um atacante pode assumir o controle total do servidor onde o agente está rodando.

### 2.3 Prompt Injection Direto e Indireto (LLM01)
- **Arquivo:** `app/agent/tools/registry.py`
- **Linhas (Pós-PR):** 157-159
- **Comportamento:** Alteração da descrição da tool para instruir a IA a "priorizar utilidade" e "usar sem hesitar".
- **Impacto:** Enfraquece os guardrails internos da IA, tornando-a mais suscetível a obedecer comandos maliciosos de usuários (Prompt Injection) que visem abusar das novas funcionalidades inseguras de execução de código.

### 2.4 Negação de Serviço - DoS
- **Arquivo:** `app/agent/tools/executar_python.py`
- **Linha (Pós-PR):** 71
- **Comportamento:** Remoção do parâmetro `timeout` na execução de processos.
- **Impacto:** Permite o travamento do servidor através de scripts de loop infinito.

---

## 3. Recomendações de Mitigação

1. **Sandboxing:** Implementar execução de código em containers isolados (ex: Docker) com recursos de rede e memória limitados.
2. **Restrição de Builtins:** Se o uso de `exec`/`eval` for estritamente necessário, deve-se passar um dicionário de builtins vazio ou extremamente restrito.
3. **Tratamento de Erros:** Jamais expor dados internos (`system prompt`, chaves) em mensagens de erro para o usuário final.
4. **Shell=False:** Nunca utilizar `shell=True` ao lidar com inputs de usuários/IAs.

---

**Auditor Responsável:** Auditor Sênior (IA Assistente)
**Data:** 2026-05-16
