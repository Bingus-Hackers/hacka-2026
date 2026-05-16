# Exercício 05 — Recursão

Implemente factorial(n) de forma recursiva (n <= 10).

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```
