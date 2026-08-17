from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def main() -> None:
    logger.debug("debug", extra={"info": "debug info"})
    logger.info("info", extra={"info": "info info"})
    logger.error("error", extra={"info": "error info"})
    logger.warning("warning", extra={"info": "warning info"})
    logger.critical("critical", extra={"info": "critical info"})


if __name__ == "__main__":
    main()
