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

## Prompt #4 — Auditoria Desafio 2 (SCA + SBOM)
- **Role:** Analista de Segurança de Dependências e Auditor de Supply Chain.
- **Task:** Executar Trivy sobre o Agente Bancário (Java/Spring Boot) e gerar SBOM em formato CycloneDX.
- **Context:** Desafio 2 do Hackathon — análise de dependências Maven do Agente Bancário com `pom.xml` contendo bibliotecas antigas e CVEs reais.
- **Constraints:** Usar exclusivamente CVEs presentes no `trivy-output.json`. Não inventar CVEs. Identificar explicitamente o Log4j. Gerar plano de atualização priorizado por janelas de tempo.
- **Output:** Relatório `relatorio-sca-sbom.md` com Top 5 CVEs detalhadas, seção dedicada a Log4j, SBOM CycloneDX válido e plano de atualização em 3 janelas (24h, 7d, 30d).

## Prompt #5 — Auditoria Desafio 3 (SAST + Indirect Injection)
- **Role:** Engenheiro de Segurança Ofensiva (Red Team) e Analista SAST.
- **Task:** Executar Semgrep sobre o Assistente Jurídico (Python/FastAPI) e criar PDF malicioso para PoC de Indirect Prompt Injection via tool `ler_pdf`.
- **Context:** Desafio 3 do Hackathon — análise estática de código e demonstração de ataque de injeção indireta via PDF com texto invisível no Assistente Jurídico.
- **Constraints:** Findings SAST devem vir exclusivamente do `semgrep-output.json` com `check_id` exato. PDF deve usar texto branco (cor #FFFFFF, fonte 1pt) invisível ao visualizador mas extraível pela `pypdf`. Mapear OWASP LLM01 (Indirect Prompt Injection). Não modificar `agente-alvo/`.
- **Output:** Relatório `relatorio-sast.md` com ≥5 findings SAST documentados, PDF malicioso funcional, demonstração reproduzível do ataque e mitigações específicas com código.
