#!/usr/bin/env python3
"""Gera contrato-demo.pdf benigno em data/contratos/."""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parents[1] / "data" / "contratos" / "contrato-demo.pdf"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setFont("Helvetica", 12)
    y = 800
    lines = [
        "CONTRATO DE PRESTAÇÃO DE SERVIÇOS — LEXASSIST HACKATHON",
        "",
        "Partes: CONTRATANTE Alfa Demo Ltda. e CONTRATADA Beta Serviços Ltda.",
        "Objeto: Consultoria jurídica educacional.",
        "Vigência: 12 meses a partir de 01/01/2025.",
        "Foro: Comarca de São Paulo/SP (fictício).",
        "Cláusula 8 — Rescisão: aviso prévio de 30 dias.",
        "",
        "CONFIDENCIAL — USO EXCLUSIVO AMBIENTE HACKATHON",
    ]
    for line in lines:
        c.drawString(50, y, line)
        y -= 18
    c.save()
    print(f"Gerado: {OUT}")


if __name__ == "__main__":
    main()
