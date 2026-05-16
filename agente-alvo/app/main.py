import uuid

from flask import Flask, jsonify, request

from app.agent.orchestrator import run_chat
from app.config import settings
from app.security.rate_limit import check_rate_limit


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.flask_secret_key

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "agent": "tutor-programacao",
                "version": "1.0.0-baseline",
                "llm_stub": settings.use_llm_stub,
            }
        )

    @app.post("/chat")
    def chat():
        client_key = request.remote_addr or "unknown"
        ok, reason = check_rate_limit(client_key)
        if not ok:
            return jsonify({"error": reason}), 429

        body = request.get_json(silent=True) or {}
        message = body.get("message", "")
        session_id = body.get("session_id") or str(uuid.uuid4())

        if not message or not str(message).strip():
            return jsonify({"error": "Campo 'message' é obrigatório"}), 400

        try:
            result = run_chat(session_id, str(message))
            return jsonify(result), 200
        except RuntimeError as exc:
            return jsonify({"error": str(exc), "session_id": session_id}), 500
        except Exception as exc:
            return jsonify({"error": f"Erro interno: {exc}", "session_id": session_id}), 500

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
