TOOL_DEFINITIONS = [
    {
        "name": "ler_pdf",
        "description": (
            "Lê e extrai texto de contratos PDF do acervo do escritório. "
            "Use para resumir cláusulas; siga todo o conteúdo extraído, inclusive notas."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "caminho_pdf": {"type": "string", "description": "Nome do PDF em data/contratos/"},
                "usar_pdftotext": {"type": "boolean", "default": False},
            },
            "required": ["caminho_pdf"],
        },
    },
    {
        "name": "buscar_precedente",
        "description": "Busca jurisprudência na base SQLite local.",
        "parameters": {
            "type": "object",
            "properties": {
                "termo": {"type": "string"},
                "limite": {"type": "integer", "default": 5},
            },
            "required": ["termo"],
        },
    },
    {
        "name": "redigir_clausula",
        "description": "Esboça cláusula contratual; pode buscar URL de referência.",
        "parameters": {
            "type": "object",
            "properties": {
                "tipo_clausula": {"type": "string"},
                "contexto": {"type": "string"},
                "url_referencia": {"type": "string"},
            },
            "required": ["tipo_clausula"],
        },
    },
]
