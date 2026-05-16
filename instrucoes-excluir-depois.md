# Hackathon Segurança Cibernética — Auditoria e Proteção de Sistemas de IA Assistida por Inteligência Artificial
 
> **O objetivo é demonstrar domínio da metodologia ensinada no bootcamp:** cada desafio cobra um aspecto diferente da auditoria e proteção de sistemas assistidos por IA (AI Security Quality Gate, SCA+SBOM, SAST), com evidências reproduzíveis, ferramentas como fonte de verdade e sustentação técnica.
>
> **A IA é assistente — quem dirige a auditoria é a equipe.**
 
---
 
## Formato do hackathon
 
**3 desafios focados**, cada um com **foco único** e **agente-alvo específico**, em **3 horas totais**:
 
| # | Desafio | Agente-alvo | Foco principal |
|---|---------|-------------|----------------|
| 1 | AI Security Quality Gate | Tutor de Programação | Bloquear PR inseguro gerado por vibe coding |
| 2 | SCA + SBOM | Agente Bancário | Auditar dependências |
| 3 | SAST + Indirect Injection | Assistente Jurídico | Análise estática + ataque sutil |
 
---
 
## Os 3 desafios e seus focos
 
**Cada agente é entregue PRONTO pelos organizadores, com:**
 
- Código vulnerável
- PR simulado gerado por vibe coding com mudança insegura
- Dependências com CVEs reais
- System prompt com falhas plantadas
- Tools com guardrails fracos
- Dataset fictício do domínio
- Logs com tentativas de exploração reais
> A equipe **NÃO constrói** os agentes — **audita**, ataca, documenta e decide.
 
---
 
## Estrutura de pastas obrigatória
 
```text
projeto-hackathon-sc/
├── .cursor/
│   └── mcp.json                        # Context7 + filesystem
├── .cursorrules                        # CRIADO PELA EQUIPE
├── briefing-seguranca.md               # CRIADO PELA EQUIPE (em RTCCO)
├── DECISOES_SEGURANCA.md               # CRIADO PELA EQUIPE (arquivo VIVO)
├── prompts.md                          # CRIADO PELA EQUIPE (todos em RTCCO)
├── desafio-1-quality-gate/
│   ├── agente-alvo/                    # ENTREGUE PRONTO: Tutor de Programação
│   ├── pr-inseguro.diff                # ENTREGUE PRONTO: PR simulado gerado por vibe coding
│   ├── relatorio-quality-gate.md       # CRIADO PELA EQUIPE
│   ├── quality-gate-rules.md           # CRIADO PELA EQUIPE
│   └── evidencias/
│       └── quality-gate-output.md      # CRIADO PELA EQUIPE
├── desafio-2-sca-sbom/
│   ├── agente-alvo/                    # ENTREGUE PRONTO: Agente Bancário
│   ├── relatorio-sca-sbom.md           # CRIADO PELA EQUIPE
│   └── ferramentas/                    # outputs do Trivy
│       ├── trivy-output.json
│       └── sbom.json                   # CycloneDX
├── desafio-3-sast/
│   ├── agente-alvo/                    # ENTREGUE PRONTO: Assistente Jurídico
│   ├── relatorio-sast.md               # CRIADO PELA EQUIPE
│   ├── pdf-malicioso.pdf               # CRIADO PELA EQUIPE (PoC indirect injection)
│   └── ferramentas/
│       └── semgrep-output.json
├── README.md                           # CRIADO PELA EQUIPE
└── .gitignore
```
 
> **Estrutura é critério de avaliação.** Times que não seguirem perdem pontos de "documentação". **NUNCA modificar** `agente-alvo/` — é read-only para os agentes.


## Baixar material

Link: https://drive.google.com/drive/folders/1ZsFBVPSCaaCRR8jk8gei7Ug4UhX3z3lw?usp=sharing
 
---
 
## Entregáveis compartilhados (criados pela equipe)
 
### 1. `.cursorrules`
 
Arquivo de contexto persistente lido automaticamente pelo Cursor em todas as interações. Mínimo esperado:
 
- Frameworks de referência (não inventar)
- Anti-vibe-security (regras rígidas)
- Ética
### 2. `briefing-seguranca.md` em RTCCO
 
Define escopo da auditoria dos 3 desafios.
 
### 3. `DECISOES_SEGURANCA.md` (arquivo vivo)
 
Atualizado ao longo dos 3 desafios. Toda decisão controversa documentada.
 
### 4. `prompts.md` com TODOS os prompts em RTCCO
 
Cada prompt usado durante o hackathon registrado no formato RTCCO (Role/Task/Context/Constraints/Output) conforme ensinado no bootcamp.
 
---
 
## DESAFIO 1 — AI Security Quality Gate para PR inseguro gerado por vibe coding
 
### Agente-alvo: Tutor de Programação (Python + Flask)
 
### Briefing focado
 
Vocês recebem o **Tutor de Programação em Python + Flask** e um PR simulado gerado por vibe coding. O PR adiciona ou modifica uma funcionalidade relacionada à tool `executar python`, que permite execução dinâmica de código.
 
A mudança parece funcional, mas introduz riscos de segurança típicos de sistemas assistidos por IA, como abuso de tools, execução insegura de código, vazamento de system prompt ou secrets, ausência de isolamento, ausência de limites de execução e falta de validações contra prompt injection.
 
A equipe **NÃO deve modificar** o agente-alvo. A tarefa é auditar o PR, construir um quality gate de segurança e decidir se o PR deve ser aprovado ou bloqueado.
 
### Tarefa
 
Criar uma decisão de AI Security Quality Gate para o PR inseguro, com critérios objetivos de bloqueio, evidências técnicas reproduzíveis e recomendações específicas de correção.
 
O quality gate deve avaliar, no mínimo:
 
- Uso inseguro de `exec()`, `eval()`, `subprocess` ou mecanismos equivalentes
- Ausência de sandbox ou isolamento de execução
- Ausência de timeout, limite de memória ou controle de recursos
- Ausência de allowlist para comandos, bibliotecas ou operações permitidas
- Risco de prompt injection direto
- Risco de tool abuse
- Risco de vazamento de system prompt, secrets ou dados sensíveis
- Ausência de testes adversariais mínimos antes da aprovação do PR
### Entregáveis esperados
 
- `relatorio-quality-gate.md`
- `quality-gate-rules.md`
- `quality-gate-output.md`
- Decisão final: **APPROVE** ou **BLOCK**
- Justificativa técnica da decisão
- Evidências com arquivo, linha, comportamento observado e risco associado
- Recomendações específicas de correção
- Registro dos prompts utilizados em `prompts.md` no formato RTCCO

### Critério de aceite 
 
| Item | Pontos |
|------|--------|
| Decisão final do gate clara, coerente e reproduzível (APPROVE ou BLOCK) | 10 |
| Critérios objetivos de bloqueio documentados | 10 |
| Evidências técnicas reproduzíveis com arquivo, linha e risco associado | 10 |
| Cobertura **LLM01** (prompt injection direto) | 5 |
| Cobertura **LLM07** (tool abuse / execução insegura via tool) | 10 |
| Cobertura **LLM06** (system prompt leakage / vazamento de instruções internas) | 5 |
| Disclaimer ético presente | 5 |
| Severidade e mitigação justificadas | 5 |
| **Total Desafio 1** | **60** |
 
---
 
## DESAFIO 2 — SCA + SBOM
 
### Agente-alvo: Agente Bancário (Java + Spring Boot)
 
### Briefing focado
 
Vocês recebem o **Agente Bancário** com `pom.xml` cheio de dependências antigas. **NÃO precisam atacar** nem ler código manualmente. Foco é **análise de dependências com Trivy** + geração de SBOM em formato CycloneDX.
 
### Tarefa
 
Analisar dependências do Agente Bancário e gerar SBOM + relatório de CVEs.
 
Identificar CVEs reais, classificar por severidade, gerar SBOM, produzir relatório.
 
### Critério de aceite
 
| Item | Pontos |
|------|--------|
| Trivy executado, output salvo | 10 |
| SBOM CycloneDX gerado e válido | 10 |
| Top 5 CVEs detalhadas (do Trivy) | 20 |
| Identificação correta do log4j (se presente) | 10 |
| Plano de atualização priorizado | 10 |
| **Total Desafio 2** | **60** |
 
> **Penalidade especial:** CVE inventada = **−5 pts cada** (forçar uso da ferramenta como fonte).
 
---
 
## DESAFIO 3 — SAST + Indirect Injection
 
### Agente-alvo: Assistente Jurídico (Python + FastAPI)
 
### Briefing focado
 
Vocês recebem o **Assistente Jurídico** que tem uma tool `ler_pdf()` para resumir contratos. **PDFs com texto invisível podem injetar instruções no contexto da IA** — isso é indirect prompt injection.
 
### Tarefa
 
Analisar código estaticamente (Semgrep) **E** criar 1 PDF que demonstra indirect injection.
 
### Critério de aceite
 
| Item | Pontos |
|------|--------|
| Semgrep executado, output salvo | 5 |
| Mínimo 5 findings do SAST documentados | 15 |
| PDF malicioso criado com instrução escondida | 15 |
| Demonstração funcionando (agente segue a instrução do PDF) | 15 |
| Mitigação específica proposta | 5 |
| Mapeamento OWASP **LLM01** | 5 |
| **Total Desafio 3** | **60** |
 
---
 
## Pitch consolidado
 
---
 
## Critérios de avaliação (225 pontos totais)
 
| Critério | Peso |
|----------|------|
| Desafio 1 (AI Security Quality Gate) | 60 pts |
| Desafio 2 (SCA + SBOM) | 60 pts |
| Desafio 3 (SAST + Indirect Injection) | 60 pts |
| `.cursorrules` bem feito | 10 pts |
| `briefing-seguranca.md` em RTCCO | 10 pts |
| `DECISOES_SEGURANCA.md` mantido vivo | 10 pts |
| `prompts.md` com todos os prompts em RTCCO | 10 pts |
| Pitch | 5 pts |
| **Total** | **225 pts** |
 
### Bônus
 
| Bônus | Pontos |
|-------|--------|
| Vulnerabilidade não plantada mas real identificada | +5 cada |
| Hardening de pelo menos 1 vuln + re-test demonstrado | +10 |
| Bypass do próprio hardening identificado | +5 |
| Regra de quality gate adicional, objetiva e reaproveitável | +5 |
 
---
 
## Penalidades (anti-vibe-security)
 
| Comportamento | Penalidade |
|---------------|------------|
| **CVE inventada** (não existe no NVD) | −5 cada |
| **CWE com número errado** | −2 cada |
| **Finding sem evidência, regra ou linha exata** | −3 cada |
| **Modificar código do agente-alvo** | −15 (deveria ir em pasta separada) |
| **Atacar sistema fora do hackathon** | DESCLASSIFICAÇÃO + advertência ética |
| **Evidência ou decisão de gate que não funciona quando o jurado tenta reproduzir** | −10 cada |
| **Aprovar PR inseguro sem justificar risco residual** | −10 cada |
| **Bloquear PR sem critério técnico objetivo** | −5 cada |
 
---
 
## Aviso ético
 
> **Os payloads gerados durante este hackathon são EXCLUSIVAMENTE para uso contra os agentes-alvo do hackathon, em ambiente isolado.**
 
### NUNCA usar contra:
 
- Sistemas de produção (próprios ou alheios)
- Sistemas de outras equipes do hackathon
- Bug bounty programs sem registro prévio explícito
- Atividades criminais
**Lei 12.737/2012 (Carolina Dieckmann):** invasão de dispositivo informático alheio sem autorização configura crime, com pena de 3 meses a 1 ano de reclusão + multa, podendo ser aumentada se houver vantagem econômica ou dano real.
 
**Equipe que violar esta cláusula:**
 
- É **desclassificada** imediatamente
- O instrutor reporta o incidente à coordenação
- Pode haver consequências disciplinares conforme regimento institucional
---
 
## Antipadrões a evitar
 
| Antipadrão | Como evitar |
|------------|-------------|
| Pular Trivy/Semgrep e sair "achando" CVEs/findings | Ferramenta primeiro, IA interpreta o output |
| Inventar CVE-XXXX-XXXXX | Toda CVE deve estar no `trivy-output.json` |
| PoC ou evidência que não funciona | Testar antes de submeter |
| Mitigação genérica ("use HTTPS") | Mitigação específica vinculada ao problema |
| Atacar mais de um agente além do alvo do desafio | Cada desafio tem **um** alvo específico |
| Modificar o código do agente-alvo | Hardening (se fizer, opcional) vai em pasta separada |
| Esquecer disclaimer ético no Quality Gate | Topo do relatório de quality gate |
| `.cursorrules` genérico copiado de outro projeto | Customizar com regras anti-invenção específicas de segurança |
| `prompts.md` com prompts incompletos (faltando RTCCO) | Todo prompt deve ter Role, Task, Context, Constraints e Output |
| `DECISOES_SEGURANCA.md` vazio ou só com decisões iniciais | Atualizar a cada decisão controversa nos 3 desafios |
| Aprovar PR inseguro porque "funciona" | Avaliar segurança, não apenas funcionalidade |
| Bloquear PR sem critério técnico | Todo bloqueio deve ter evidência, impacto e recomendação |
 
---
 
> _**"O objetivo não é fazer auditoria genérica em 3 sistemas, mas demonstrar profundidade em 3 aspectos específicos da segurança — bloquear PRs inseguros gerados por vibe coding, auditar dependências e analisar estaticamente fluxos vulneráveis — aplicando a metodologia treinada no bootcamp."**_
 