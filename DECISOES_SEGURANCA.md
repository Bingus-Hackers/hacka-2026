# Registro de Decisões de Segurança

Este arquivo documenta todas as decisões críticas tomadas durante a auditoria dos três desafios do hackathon.

| Data | Desafio | Decisão | Justificativa | Status |
|------|---------|---------|---------------|--------|
| 2026-05-16 | Global | Setup de Governança | Implementação de travas anti-escrita no `.cursorrules` para evitar penalidades. | Concluído |
| 2026-05-16 | Desafio 1 | Bloqueio do PR Inseguro | Decisão de BLOCK baseada em RCE crítico (LLM07), Vazamento de Prompt (LLM06) e vulnerabilidade de Prompt Injection (LLM01) por enfraquecimento de guardrails. | Concluído |
| 2026-05-16 | Desafio 2 | Priorização do Log4Shell | CVE-2021-44228 (score 10.0) priorizada como correção de Janela 24h por ser dependência direta com exploit público. Plano de atualização escalonado em 3 janelas (24h, 7d, 30d). Todas as CVEs extraídas exclusivamente do `trivy-output.json`. | Concluído |
| 2026-05-16 | Desafio 3 | Comprovação de Indirect Injection | Criação de PDF com texto branco invisível (1pt, #FFFFFF) para demonstrar que o agente segue instruções injetadas via documento externo. Decisão de não usar payloads destrutivos — apenas exfiltração demonstrativa. Findings SAST vinculados ao `semgrep-output.json`. | Concluído |
