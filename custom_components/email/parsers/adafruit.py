import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_ADAFRUIT = 'adafruit'
EMAIL_DOMAIN_ADAFRUIT = 'adafruit.com'


def parse_adafruit(email):
    """Parse Adafruit tracking numbers."""
    tracking_numbers = []

    matches = re.findall(r'Delivery Confirmation ID is (.*?) ', email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    return tracking_numbers
