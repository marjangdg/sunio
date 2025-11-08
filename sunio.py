import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)

    app.config["DEBUG"] = os.getenv("DEBUG", "false").lower() == "true"
    app.config["SERVICE_NAME"] = os.getenv("SERVICE_NAME", "sunio")

    # ---- Logging (no directory creation here) ----
    stdout_handler = logging.StreamHandler()
    fmt = '{"service":"%(service)s","level":"%(levelname)s","msg":"%(message)s","asctime":"%(asctime)s"}'
    stdout_handler.setFormatter(logging.Formatter(fmt=fmt))

    logger = logging.getLogger(app.config["SERVICE_NAME"])
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
    logger.propagate = False
    logger.addHandler(stdout_handler)

    # Try file handler only if path exists
    log_dir = "/logs/app"
    log_file = f"{log_dir}/app.log"
    if os.path.isdir(log_dir):
        file_handler = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5)
        file_handler.setFormatter(logging.Formatter(fmt=fmt))
        logger.addHandler(file_handler)
    else:
        # One-time notice to stdout; no directory creation here by design
        logger.warning("Log directory not found; file logging disabled", extra={"service": app.config["SERVICE_NAME"]})

    def get_logger():
        return logging.LoggerAdapter(logger, extra={"service": app.config["SERVICE_NAME"]})

    log = get_logger()

    @app.get("/sum")
    def sum():
        left = request.args.get("left", type=str)
        right = request.args.get("right", type=str)

        if left is None or right is None:
            log.warning("Missing params")
            return {"error": "Query params 'left' and 'right' are required"}, 400

        try:
            left_int = int(left)
            right_int = int(right)
        except ValueError:
            log.warning("Invalid integer params")
            return {"error": "'left' and 'right' must be integers"}, 400

        result = left_int + right_int
        log.info(f"Computed sum={result}")
        return {"sum": result}, 200

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "service": app.config["SERVICE_NAME"]}, 200

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return {"error": "Method not allowed"}, 405

    @app.errorhandler(500)
    def internal_error(e):
        log = get_logger()
        log.error(f"Internal server error: {e}")
        return {"error": "Internal server error"}, 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")),
            debug=os.getenv("DEBUG", "false").lower() == "true")
