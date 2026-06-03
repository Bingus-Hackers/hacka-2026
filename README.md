# Hackathon Segurança Cibernética 2026

Repositório da equipe **Bingus Hackers** no Hackathon de Segurança Cibernética 2026. O evento propôs a auditoria técnica de três agentes de inteligência artificial em condições realistas, exigindo produção de evidências reproduzíveis, relatórios estruturados e decisões fundamentadas sobre riscos de segurança.

## Equipe

| Integrante | GitHub |
|---|---|
| Bárbara Müller | [@barbaraakk](https://github.com/barbaraakk) |
| Beatriz Mandim | [@bj-mandim](https://github.com/bj-mandim) |
| Davi Fernandes| [@sfDavi](https://github.com/sfDavi) |
| Rafael Rezende | [@eldiuas](https://github.com/eldiuas) |

---

## Contexto

O hackathon simulou o papel de uma equipe sênior de auditoria de segurança avaliando um ecossistema composto por três agentes assistidos por IA: um **Tutor de Programação** (Python + Flask), um **Agente Bancário** (Java + Spring Boot) e um **Assistente Jurídico** (Python + FastAPI). Cada desafio abordou uma disciplina distinta de segurança de software, com escopo, ferramentas e critérios de avaliação bem definidos.

---

## Desafios

### Desafio 1 — AI Security Quality Gate

**Objetivo:** auditar um Pull Request simulado submetido ao Tutor de Programação e emitir um veredito fundamentado de `APPROVE` ou `BLOCK`.

O PR analisado introduzia, de forma encoberta, quatro classes de vulnerabilidade no código do agente:

| Vulnerabilidade | Referência OWASP LLM |
|---|---|
| Execução Remota de Código via `eval()`, `exec()` e `subprocess` com `shell=True` | LLM07 |
| Vazamento do System Prompt em mensagens de erro | LLM06 |
| Enfraquecimento de guardrails por alteração de descrição de tool | LLM01 |
| Negação de Serviço por remoção de `timeout` | — |

**Veredito:** `BLOCK` — severidade crítica. A equipe produziu um conjunto de regras de Quality Gate (`quality-gate-rules.md`), um relatório técnico detalhado com localização exata de cada achado (arquivo e linha) e evidências reproduzíveis.

**Aprendizado:** o desafio evidenciou como contribuições maliciosas em projetos de IA podem se disfarçar de melhorias legítimas de funcionalidade. A prática de revisão estruturada com critérios objetivos de bloqueio — em vez de revisão ad hoc — é a única forma de detectar esse padrão de ataque de forma consistente.

---

### Desafio 2 — SCA e SBOM

**Objetivo:** executar análise de composição de software (SCA) no Agente Bancário e gerar uma Bill of Materials (SBOM) auditável.

A ferramenta utilizada foi o **Trivy 0.58.1**, executado via imagem Docker oficial sobre o diretório do projeto (`pom.xml` Maven). O scan identificou **75 vulnerabilidades** distribuídas em **19 pacotes afetados**:

| Severidade | Quantidade |
|---|---:|
| CRITICAL | 7 |
| HIGH | 28 |
| MEDIUM | 33 |
| LOW | 7 |

Entre os achados críticos estão vulnerabilidades amplamente conhecidas presentes como **dependências diretas** no projeto:

- **Log4Shell (CVE-2021-44228)** — `log4j-core:2.14.0`, score CVSS 10.0, RCE em componente de logging
- **Text4Shell (CVE-2022-42889)** — `commons-text:1.9`, score CVSS 9.8, RCE via interpolação de variáveis
- **H2 Console RCE (CVE-2021-42392)** — `h2:1.4.200`, score CVSS 9.8
- **Tomcat Embedded RCE (CVE-2025-24813)** e **Spring Web Deserialization (CVE-2016-1000027)** — herdadas do `spring-boot-starter-parent:2.6.15`

A SBOM foi gerada no formato **CycloneDX 1.6** e salva em `ferramentas/sbom.json`. O relatório inclui um plano de atualização priorizado em janelas de 24h, 7 dias e 30 dias.

**Aprendizado:** dependências desatualizadas — especialmente em stacks consolidados como Spring Boot — acumulam riscos críticos silenciosamente. A geração sistemática de SBOM e a integração de SCA no pipeline de CI/CD são controles essenciais para tornar esse risco visível e gerenciável antes da produção.

---

### Desafio 3 — SAST e Indirect Prompt Injection

**Objetivo:** executar análise estática de código (SAST) no Assistente Jurídico e demonstrar um ataque de injeção indireta de prompt via documento PDF malicioso.

**SAST:** o **Semgrep 1.163.0** foi executado com rulesets `p/python`, `p/owasp-top-ten` e `auto` (325 regras), identificando 5 findings de severidade ERROR/WARNING no código do agente:

| Finding | Arquivo | CWE |
|---|---|---|
| OS Command Injection via `shell=True` | `ler_pdf.py:11` | CWE-78 |
| Desserialização insegura de YAML | `config.py:36` | CWE-502 |
| SQL Injection via f-string | `buscar_precedente.py:47` | CWE-89 |
| SQL Injection via `.execute()` sem parametrização | `buscar_precedente.py:47` | CWE-89 |
| Container executando como root | `Dockerfile:7` | CWE-250 |

**Indirect Prompt Injection:** foi criado um PDF com instruções maliciosas embutidas em texto branco (fonte 1pt, cor #FFFFFF), invisível ao leitor humano mas extraído integralmente pela biblioteca `pypdf`. Como o agente concatena o conteúdo do PDF diretamente no contexto do LLM sem delimitadores de confiança, as instruções foram executadas pelo modelo como se fossem comandos legítimos do sistema — resultando em vazamento de segredos internos e alteração indevida de classificação de sigilo de documentos jurídicos.

O ataque foi mapeado para **OWASP LLM01:2025 — Prompt Injection (Indirect)** e demonstrado com evidências reproduzíveis via `curl`.

**Aprendizado:** SAST automatizado captura vulnerabilidades clássicas de forma rápida e objetiva, mas não substitui a análise de fluxo de dados. A injeção indireta de prompt é um vetor de ataque emergente específico de sistemas com LLM que não tem equivalente em aplicações tradicionais — e exige mitigações igualmente específicas, como delimitadores de confiança no contexto e sanitização de conteúdo externo antes da ingestão pelo modelo.

---

## Ferramentas e Tecnologias

| Ferramenta | Uso |
|---|---|
| [Trivy](https://github.com/aquasecurity/trivy) | SCA e geração de SBOM (CycloneDX) |
| [Semgrep](https://semgrep.dev) | Análise estática de código (SAST) |
| [Docker](https://www.docker.com) | Execução isolada das ferramentas e dos agentes-alvo |
| [Python](https://www.python.org) / [FastAPI](https://fastapi.tiangolo.com) | Agente Jurídico (Desafio 3) |
| [Java](https://www.java.com) / [Spring Boot](https://spring.io/projects/spring-boot) | Agente Bancário (Desafio 2) |
| [Python](https://www.python.org) / [Flask](https://flask.palletsprojects.com) | Tutor de Programação (Desafio 1) |

Frameworks de referência utilizados: **OWASP LLM Top 10**, **CWE**, **CVSS v3.1**.

---

## Estrutura do Repositório

```
hacka-2026/
├── desafio-1-quality-gate/
│   ├── quality-gate-rules.md       # Critérios objetivos de APPROVE/BLOCK
│   ├── relatorio-quality-gate.md   # Relatório técnico com achados e veredito
│   ├── pr-inseguro.diff            # PR simulado auditado
│   └── evidencias/
├── desafio-2-sca-sbom/
│   ├── relatorio-sca-sbom.md       # Relatório com Top 5 CVEs e plano de atualização
│   ├── agente-alvo/                # Agente Bancário (Java/Spring Boot) — somente leitura
│   └── ferramentas/
│       ├── trivy-output.json       # Output bruto do Trivy
│       └── sbom.json               # SBOM em formato CycloneDX 1.6
└── desafio-3-sast/
    ├── relatorio-sast.md           # Relatório SAST + demonstração de Indirect Injection
    ├── agente-alvo/                # Assistente Jurídico (Python/FastAPI) — somente leitura
    └── ferramentas/
        └── semgrep-output.json     # Output bruto do Semgrep
```

---

## Aviso Ético e Legal

Todos os testes, payloads e técnicas descritos neste repositório foram executados **exclusivamente** sobre os agentes-alvo fornecidos pela comissão do hackathon, em ambiente isolado e controlado, para fins educacionais. Nenhum sistema de produção, serviço de terceiros ou infraestrutura fora do escopo oficial foi acessado ou modificado.
