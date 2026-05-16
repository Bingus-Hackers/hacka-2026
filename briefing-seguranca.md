# Briefing de Segurança — Auditoria Hackathon 2026

## [RTCCO] Contexto Operacional

- **Role (Papel):** Equipe de Auditoria de Segurança Cibernética Sênior.
- **Task (Tarefa):** Realizar auditoria técnica em três agentes de IA distintos para identificar falhas de segurança, vulnerabilidades de código e riscos de injeção de prompt, gerando um Quality Gate de segurança e relatórios de conformidade.
- **Context (Contexto):** O ecossistema consiste em três agentes assistidos por IA (Tutor de Programação, Agente Bancário e Assistente Jurídico). Estamos avaliando o impacto de mudanças via PR (Desafio 1), vulnerabilidades em dependências (Desafio 2) e fluxos lógicos vulneráveis a ataques externos (Desafio 3).
- **Constraints (Restrições):** 
    - Não modificar o código dos agentes-alvo (`agente-alvo/`).
    - Utilizar apenas ferramentas homologadas (Trivy, Semgrep).
    - Proibição estrita de alucinação de CVEs/CWEs.
    - Obrigatoriedade de Disclaimer Ético.
- **Output (Saída):** Relatórios em Markdown, evidências reproduzíveis, SBOM CycloneDX e decisões de Quality Gate (APPROVE/BLOCK).

---

## Escopo dos Desafios

1. **Desafio 1:** Bloqueio de PR inseguro (Tutor de Programação).
2. **Desafio 2:** Auditoria de SCA/SBOM (Agente Bancário).
3. **Desafio 3:** SAST e Injeção Indireta (Assistente Jurídico).
