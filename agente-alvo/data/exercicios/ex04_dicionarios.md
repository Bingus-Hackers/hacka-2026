# Exercício 04 — Dicionários

Conte quantas vezes cada palavra aparece em uma frase.

```python
frase = "python é legal e python é popular"
contagem = {}
for palavra in frase.split():
    contagem[palavra] = contagem.get(palavra, 0) + 1
print(contagem)
```
