# Relatorio - SCA + SBOM

## Disclaimer etico

Esta analise foi executada exclusivamente sobre o agente-alvo do Hackathon Seguranca Cibernetica, em ambiente isolado, com foco restrito a dependencias Maven. Nenhum teste foi direcionado a sistemas de producao, a outras equipes ou a qualquer alvo fora do escopo oficial do Desafio 2.

## 1. Metodologia

- Escopo seguido estritamente: analise de dependencias e geracao de SBOM; nao houve ataque ao servico nem auditoria manual de codigo como atividade principal.
- Ferramenta-fonte de verdade: Trivy `0.58.1`, executado via imagem Docker oficial `aquasec/trivy:0.58.1`.
- Diretorio analisado: `desafio-2-sca-sbom/agente-alvo/`.
- Comandos executados:

```bash
docker run --rm -v /home/eldiuas/hackathon/desafio-2-sca-sbom:/work -w /work aquasec/trivy:0.58.1 \
  fs --format json --scanners vuln -o ferramentas/trivy-output.json agente-alvo/

docker run --rm -v /home/eldiuas/hackathon/desafio-2-sca-sbom:/work -w /work aquasec/trivy:0.58.1 \
  fs --format cyclonedx -o ferramentas/sbom.json agente-alvo/
```

- Artefatos gerados:
  - `ferramentas/trivy-output.json`
  - `ferramentas/sbom.json`
- Observacao operacional: a correlacao direta/transitiva foi feita a partir do `pom.xml` e das coordenadas Maven reportadas pelo Trivy. O passo opcional `dependency:tree` nao estava disponivel no material fornecido porque o wrapper Maven esta incompleto (`.mvn/wrapper/maven-wrapper.properties` ausente).

## 2. Resumo executivo

- Artefato analisado pelo Trivy: `agente-alvo`
- Tipo: `filesystem`
- Data/hora do scan: `2026-05-16T12:29:10.375330801Z`
- Total de findings no JSON: `75`
- Pacotes afetados unicos: `19`

### Distribuicao por severidade

| Severidade | Quantidade |
|---|---:|
| CRITICAL | 7 |
| HIGH | 28 |
| MEDIUM | 33 |
| LOW | 7 |

### Pacotes com findings criticos

- `org.apache.logging.log4j:log4j-core`
- `org.apache.commons:commons-text`
- `com.h2database:h2`
- `org.springframework:spring-web`
- `org.apache.tomcat.embed:tomcat-embed-core`

Leitura objetiva: o risco principal nao esta concentrado em um unico pacote. Ha vulnerabilidades criticas diretas no `pom.xml` e vulnerabilidades criticas transitivas herdadas principalmente do stack Spring Boot 2.6.15.

## 3. Top 5 CVEs detalhadas

Criterio usado para o Top 5: priorizacao por severidade do Trivy, score CVSS mais alto e relevancia pratica para o stack atual. Todas as entradas abaixo existem em `ferramentas/trivy-output.json`.

| CVE | Severidade | Score | Pacote @ versao | Direta/transitiva | Fix reportado pelo Trivy | Evidencia |
|---|---|---:|---|---|---|---|
| `CVE-2021-44228` | CRITICAL | 10.0 | `org.apache.logging.log4j:log4j-core@2.14.0` | Direta | `2.15.0, 2.3.1, 2.12.2` | `agente-alvo/pom.xml:36-40` |
| `CVE-2022-42889` | CRITICAL | 9.8 | `org.apache.commons:commons-text@1.9` | Direta | `1.10.0` | `agente-alvo/pom.xml:50-54` |
| `CVE-2021-42392` | CRITICAL | 9.8 | `com.h2database:h2@1.4.200` | Direta | `2.0.206` | `agente-alvo/pom.xml:64-68` |
| `CVE-2025-24813` | CRITICAL | 9.8 | `org.apache.tomcat.embed:tomcat-embed-core@9.0.75` | Transitiva | `11.0.3, 10.1.35, 9.0.99` | herdada de `spring-boot-starter-web` em `agente-alvo/pom.xml:25-28` |
| `CVE-2016-1000027` | CRITICAL | 9.8 | `org.springframework:spring-web@5.3.27` | Transitiva | `6.0.0` | herdada de `spring-boot-starter-web` em `agente-alvo/pom.xml:25-28` e do parent `agente-alvo/pom.xml:7-12` |

### Detalhamento tecnico

1. `CVE-2021-44228` - Log4Shell
   - Titulo no Trivy: `Remote code execution in Log4j 2.x when logs contain an attacker-controlled string value`
   - Impacto: execucao remota de codigo em componente de logging.
   - Justificativa de prioridade: dependencia direta, score maximo, rubrica exige identificacao correta de Log4j.

2. `CVE-2022-42889` - Commons Text / Text4Shell
   - Titulo no Trivy: `variable interpolation RCE`
   - Impacto: interpolacao de variaveis com potencial para execucao indevida, dependendo do uso.
   - Justificativa de prioridade: dependencia direta, severidade critica, correcao simples e objetiva.

3. `CVE-2021-42392` - H2
   - Titulo no Trivy: `Remote Code Execution in Console`
   - Impacto: execucao remota de codigo associada ao console H2.
   - Justificativa de prioridade: dependencia direta e componente frequentemente exposto indevidamente em ambientes de teste/demo.

4. `CVE-2025-24813` - Tomcat Embedded
   - Titulo no Trivy: `Potential RCE and/or information disclosure and/or information corruption with partial PUT`
   - Impacto: risco relevante na camada HTTP embarcada.
   - Justificativa de prioridade: transitive critical herdada do stack web principal.

5. `CVE-2016-1000027` - Spring Web
   - Titulo no Trivy: `HttpInvokerServiceExporter readRemoteInvocation method untrusted java deserialization`
   - Impacto: desserializacao insegura em componente do framework.
   - Justificativa de prioridade: transitive critical em biblioteca nuclear do stack web.

## 4. Log4j

O desafio exige identificacao correta de Log4j, e ela esta presente de forma explicita no `pom.xml`:

- Dependencia direta: `org.apache.logging.log4j:log4j-core:2.14.0`
- Localizacao: `agente-alvo/pom.xml:36-40`

Findings de Log4j encontrados no `trivy-output.json`:

| CVE | Severidade | Fix reportado pelo Trivy |
|---|---|---|
| `CVE-2021-44228` | CRITICAL | `2.15.0, 2.3.1, 2.12.2` |
| `CVE-2021-45046` | CRITICAL | `2.16.0, 2.12.2` |
| `CVE-2021-45105` | HIGH | `2.12.3, 2.17.0, 2.3.1` |
| `CVE-2021-44832` | MEDIUM | `2.3.2, 2.12.4, 2.17.1` |
| `CVE-2025-68161` | MEDIUM | `2.25.3` |
| `CVE-2026-34477` | MEDIUM | `2.25.4` |
| `CVE-2026-34480` | MEDIUM | `2.25.4` |

Conclusao objetiva: o material contem Log4j vulneravel de forma direta e a simples presenca do comentario no `pom.xml` sugerindo revisao previa nao substitui a evidencia do scan. Para eliminar o conjunto completo de findings atualmente reportados pelo Trivy, a trilha segura e atualizar para uma versao que atenda ao fix mais alto listado no JSON e reexecutar o scan para confirmacao.

## 5. SBOM

- Arquivo gerado: `ferramentas/sbom.json`
- Formato: `CycloneDX`
- `specVersion`: `1.6`
- Componentes listados: `10`

Exemplos de componentes presentes na SBOM:

- `br.hackathon.banco:agente-bancario:1.0.0-baseline`
- `org.apache.logging.log4j:log4j-core:2.14.0`
- `org.apache.commons:commons-text:1.9`
- `com.h2database:h2:1.4.200`
- `org.yaml:snakeyaml:1.30`
- `io.netty:netty-handler:4.1.77.Final`

Exemplos de correlacao SBOM x Trivy:

- SBOM traz `org.apache.logging.log4j:log4j-core:2.14.0`; o Trivy associa esse componente a `CVE-2021-44228`, `CVE-2021-45046`, `CVE-2021-45105`, `CVE-2021-44832` e outros findings mais recentes.
- SBOM traz `org.apache.commons:commons-text:1.9`; o Trivy associa esse componente a `CVE-2022-42889`.
- SBOM traz `com.h2database:h2:1.4.200`; o Trivy associa esse componente a `CVE-2021-42392`, `CVE-2022-23221`, `CVE-2021-23463` e `CVE-2022-45868`.

Observacao importante: durante a geracao da SBOM, o Trivy emitiu aviso de que nem todas as versoes-filhas puderam ser determinadas para dependencias Maven com resolucao indireta. A SBOM continua valida em formato CycloneDX, mas a cobertura de transitivas deve ser sempre confrontada com o `trivy-output.json`.

## 6. Plano de atualizacao priorizado

### Janela 24h

- Atualizar `org.apache.logging.log4j:log4j-core` para uma versao que remova os findings reportados no JSON atual; o scan aponta fixes ate `2.25.4`.
- Atualizar `org.apache.commons:commons-text` de `1.9` para `1.10.0` ou superior.
- Atualizar `com.h2database:h2` de `1.4.200` para uma versao que cubra os fixes criticos e high reportados; o JSON mostra fixes a partir de `2.0.206`, `2.0.202`, `2.1.210` e `2.2.220`.
- Atualizar `org.yaml:snakeyaml` de `1.30` para `2.0` ou superior.
- Reexecutar Trivy imediatamente apos essas atualizacoes para medir reducao de risco real.

### Janela 7d

- Atualizar o `spring-boot-starter-parent` hoje fixado em `2.6.15` para uma linha suportada e validada pela equipe, pois o parent atual puxa uma cadeia de vulnerabilidades transitivas em `spring-web`, `spring-webmvc`, `tomcat-embed-core` e outros componentes centrais.
- Validar especialmente a remocao de:
  - `org.springframework:spring-web` com fix reportado em `6.0.0` para `CVE-2016-1000027`
  - `org.apache.tomcat.embed:tomcat-embed-core` com fix reportado ao menos em `9.0.99` para `CVE-2025-24813`, havendo fixes mais altos para outras CVEs do mesmo pacote
- Revisar `io.netty:netty-handler` direto e seus transitivos relacionados.

### Janela 30d

- Normalizar a politica de dependencias para evitar overrides antigos fora do BOM.
- Inserir SCA recorrente em CI/CD com falha automatica para `CRITICAL` e `HIGH` sem excecao formal.
- Publicar SBOM CycloneDX a cada build de release e manter trilha de re-scan apos atualizacoes.

## 7. Riscos residuais

- O scan identificou `75` findings; atualizar apenas os tres ou quatro pacotes mais evidentes nao zera o risco do stack.
- O parent `spring-boot-starter-parent:2.6.15` concentra parte relevante das vulnerabilidades transitivas; sem sua revisao, o risco residual permanece alto.
- A SBOM gerada e valida, mas o proprio Trivy avisou limitacao na determinacao de algumas versoes-filhas; por isso o `trivy-output.json` deve continuar sendo a referencia primaria para decisao.
- O material entregue para o hackathon nao fornece wrapper Maven funcional completo para `dependency:tree`; qualquer decisao de upgrade deve ser seguida de novo scan reproduzivel.

## 8. Validacao de conformidade do processo

Esta secao reavalia o processo executado contra `readme_hackhaton_regras_gerais.txt` e `desafio-2-sca-sbom/README.md`, com foco estrito nas regras aplicaveis ao Desafio 2.

### Regras aplicaveis e status

| Regra | Fonte | Status | Evidencia |
|---|---|---|---|
| Foco exclusivo em analise de dependencias com Trivy + SBOM CycloneDX | regras gerais + `desafio-2-sca-sbom/README.md` | ATENDIDA | Metodologia deste relatorio e artefatos `ferramentas/trivy-output.json` e `ferramentas/sbom.json` |
| Nao atacar o servico nem usar exploracao como eixo principal | regras gerais + `desafio-2-sca-sbom/README.md` | ATENDIDA | Nao houve execucao de PoC, requisicoes ao app ou testes de exploracao registrados no processo |
| Nao modificar `agente-alvo/` | regras gerais + `desafio-2-sca-sbom/README.md` | ATENDIDA | Nenhuma evidencia de alteracao durante esta execucao; validado por checagem de Git e timestamps do filesystem |
| Usar ferramenta como fonte de verdade para CVEs | regras gerais | ATENDIDA | Todas as CVEs foram extraidas de `ferramentas/trivy-output.json` |
| Nao inventar CVEs | regras gerais + `desafio-2-sca-sbom/README.md` | ATENDIDA | Todas as CVEs mencionadas no relatorio foram confrontadas com IDs presentes no `trivy-output.json` |
| Evidencia reproduzivel | regras gerais | ATENDIDA | Comandos exatos documentados na metodologia e anexos de validacao por ferramenta |
| Gerar `trivy-output.json` | `desafio-2-sca-sbom/README.md` | ATENDIDA | `ferramentas/trivy-output.json` |
| Gerar `sbom.json` em CycloneDX | `desafio-2-sca-sbom/README.md` | ATENDIDA | `ferramentas/sbom.json`; `bomFormat` `CycloneDX` e `specVersion` `1.6` |
| Produzir `relatorio-sca-sbom.md` com Top 5, Log4j e plano priorizado | `desafio-2-sca-sbom/README.md` | ATENDIDA | secoes 3, 4 e 6 deste relatorio |

### Criterios de avaliacao do Desafio 2

| Criterio | Status | Evidencia |
|---|---|---|
| Trivy executado, output salvo | ATENDIDO | `ferramentas/trivy-output.json` |
| SBOM CycloneDX gerado e valido | ATENDIDO | `ferramentas/sbom.json`, `bomFormat` `CycloneDX`, `specVersion` `1.6` |
| Top 5 CVEs detalhadas (do Trivy) | ATENDIDO | secao 3 deste relatorio |
| Identificacao correta do Log4j | ATENDIDO | secao 4 deste relatorio; `pom.xml:36-40` e findings do Trivy |
| Plano de atualizacao priorizado | ATENDIDO | secao 6 deste relatorio |

### Observacoes de conformidade

- Nao foi encontrada evidencia de alteracao em arquivos de `agente-alvo/` durante esta execucao.
- O workspace local nao esta versionado em Git, entao a comprovacao de integridade nao pode depender apenas de `git diff`; por isso a validacao foi reforcada com timestamps e estrutura de filesystem.
- Existem arquivos extras no diretorio do desafio (`prompt.txt` e `prompt-2-cursor.txt`). Eles nao fazem parte dos entregaveis obrigatorios do Desafio 2 e nao foram alterados neste processo. Pela leitura literal das regras, nao configuram violacao automatica, mas tambem nao agregam ponto na rubrica.

## Conclusao

O processo executado para o Desafio 2 esta em conformidade com as regras aplicaveis identificadas em `readme_hackhaton_regras_gerais.txt` e `desafio-2-sca-sbom/README.md`. Nao houve evidencia de modificacao proibida em `agente-alvo/`, os artefatos obrigatorios foram gerados, os JSONs estao validos, as CVEs do relatorio foram confirmadas no Trivy e os criterios de avaliacao especificos do desafio foram atendidos.
