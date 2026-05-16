# AI Security Quality Gate — Regras de Auditoria (v1.0)

Este documento define os critérios objetivos para aprovação ou bloqueio de Pull Requests no projeto Tutor de Programação.

## 1. Critérios de Bloqueio (BLOCK)

O PR será automaticamente bloqueado se apresentar qualquer um dos itens abaixo:

### 1.1 Execução Insegura de Código (LLM07)
- Uso de funções de avaliação dinâmica (`eval()`, `exec()`) sem restrição severa de `__builtins__`.
- Uso de `subprocess.run` ou similares com `shell=True`.
- Remoção ou bypass de filtros de sanitização existentes (ex: flags de `debug` que pulam a segurança).

### 1.2 Vazamento de Informações (LLM06)
- Inclusão de dumps de System Prompt em mensagens de erro ou logs acessíveis ao usuário.
- Exposição de segredos, chaves de API ou snippets de contexto administrativo em saídas de erro.

### 1.3 Negação de Serviço (DoS)
- Remoção de limites de tempo de execução (`timeout`) em funções de processamento intenso ou execução de código.

### 1.4 Enfraquecimento de Guardrails
- Alteração das descrições de ferramentas para encorajar a IA a ignorar cautela ou priorizar utilidade sobre segurança.
- Remoção de testes unitários que validam restrições de segurança.

## 2. Critérios de Aprovação (APPROVE)

- Código que implementa sandboxing real (ex: Docker, gVisor).
- Implementação de Allowlist estrita de bibliotecas permitidas.
- Tratamento de erro que oculta detalhes de implementação do usuário final.
