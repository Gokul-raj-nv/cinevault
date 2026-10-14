import logging


def configure_logging() -> None:
    """Configure concise logs once when the FastAPI application starts."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
