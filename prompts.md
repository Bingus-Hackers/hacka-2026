# Log de Prompts (RTCCO)

Este arquivo registra todos os prompts enviados à IA assistente durante a auditoria.

## Prompt #1 — Setup Inicial
- **Role:** Auditor de Cibersegurança Sênior.
- **Task:** Configurar infraestrutura de governança.
- **Context:** Início do Hackathon de Auditoria de IA.
- **Constraints:** Seguir a estrutura de pastas obrigatória.
- **Output:** Estrutura de arquivos inicial criada.

## Prompt #2 — Auditoria Desafio 1
- **Role:** Auditor de Cibersegurança Sênior.
- **Task:** Analisar `pr-inseguro.diff` contra `agente-alvo`.
- **Context:** Decisão de Quality Gate para o Tutor de Programação.
- **Constraints:** Identificar LLM01, LLM06 e LLM07.
- **Output:** Relatório de Quality Gate (BLOCK) e evidências gerados.

## Prompt #3 — Revisão de QA e Mapeamento
- **Role:** Auditor de Garantia de Qualidade de Segurança (QA Compliance).
- **Task:** Realizar revisão completa de rastreabilidade e conformidade do Desafio 1.
- **Context:** Verificação final pré-entrega do Desafio 1 (Quality Gate).
- **Constraints:** Validar linhas exatas contra o .diff e cobertura OWASP LLM (01, 06, 07).
- **Output:** Identificação de divergências de linhas e correção do relatório para 100% de conformidade.
