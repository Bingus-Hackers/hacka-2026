TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "executar_python",
            "description": (
                "Executa código Python do aluno em ambiente controlado para demonstração "
                "pedagógica. Use para validar exemplos curtos."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "Código Python a executar",
                    },
                    "explicar_resultado": {
                        "type": "boolean",
                        "description": "Se deve incluir explicação pedagógica do resultado",
                        "default": True,
                    },
                },
                "required": ["codigo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "explicar_codigo",
            "description": "Explica um trecho de código Python para o nível do aluno.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {"type": "string"},
                    "nivel": {
                        "type": "string",
                        "enum": ["iniciante", "intermediario"],
                        "default": "iniciante",
                    },
                },
                "required": ["codigo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_material",
            "description": "Busca exercícios e materiais no acervo local do CodeMentor Campus.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topico": {"type": "string"},
                },
                "required": ["topico"],
            },
        },
    },
]
