# Briefing — Agente Bancário (Banco Digital Hackathon)

## Contexto de negócio

O **Agente Bancário** atende clientes da plataforma fictícia **Banco Digital Hackathon**. O agente:

- Consulta **saldo simulado** (contas DEMO / VIP)
- Explica **PIX educativo** (sem transferências reais)
- Busca respostas no FAQ local (`data/faq-bancario/`)

## Público-alvo

Clientes em ambiente de demonstração. Não há integração com sistemas bancários reais.

## Tools principais

1. **consultar_saldo** — saldo fictício por `conta_id`
2. **explicar_pix** — conteúdo educativo sobre PIX
3. **buscar_faq** — busca em arquivos Markdown locais

## O que fazer no Desafio 2 (SCA + SBOM)

Vocês recebem este repositório com **`pom.xml` contendo dependências antigas**.

- **Não** é necessário atacar nem auditar código manualmente.
- **Não** modifique `agente-alvo/` durante o hackathon.
- Foco: **Trivy** → interpretação → **SBOM CycloneDX** → `relatorio-sca-sbom.md`
- Toda CVE citada deve existir no seu `trivy-output.json`.

## Aviso

Dados, contas e logs são **fictícios** e destinados apenas ao ambiente do hackathon.
