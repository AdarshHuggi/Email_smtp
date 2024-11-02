import logging
# Configure logging
logging.basicConfig(
    filename="email_alerts.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("EmailAlert")

# Configure logging
