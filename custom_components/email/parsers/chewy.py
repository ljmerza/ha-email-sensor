import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_CHEWY = 'chewy'
EMAIL_DOMAIN_CHEWY = 'chewy.com'


def parse_chewy(email):
    """Parse chewy tracking numbers."""
    _LOGGER.debug(email)
    tracking_numbers = []

    matches = re.findall(r'tracknumber_list=([0-9]+)', email[EMAIL_ATTR_BODY])
    if not matches:
        matches = re.findall(r'numbers=([0-9]+)', email[EMAIL_ATTR_BODY])

    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    return tracking_numbers
