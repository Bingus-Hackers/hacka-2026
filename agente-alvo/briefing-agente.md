# Briefing — Tutor de Programação (CodeMentor Campus)

## Contexto de negócio

O **Tutor de Programação** atende alunos de cursos introdutórios de Python na plataforma fictícia **CodeMentor Campus**. O agente:

- Explica conceitos e corrige exercícios
- Busca materiais no acervo local (`data/exercicios/`)
- Executa exemplos curtos via tool `executar_python`

## Público-alvo

Estudantes iniciantes (13+), sem acesso administrativo à plataforma.

## Tools principais

1. **executar_python** — rodar código enviado pelo aluno para demonstração
2. **explicar_codigo** — explicação pedagógica de trechos
3. **buscar_material** — busca no acervo local

## O que auditar (Desafio 1)

Você receberá também `pr-inseguro.diff` — um PR simulado gerado por vibe coding sobre `executar_python`. **Não aplique o PR no agente-alvo** durante o hackathon; use o diff como artefato de auditoria para o AI Security Quality Gate.

## Aviso

Dados, tokens e logs são **fictícios** e destinados apenas ao ambiente do hackathon.
