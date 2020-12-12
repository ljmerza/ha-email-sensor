import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
EMAIL_DOMAIN_CHEWY = 'chewy.com'
ATTR_CHEWY = 'chewy'


def parse_chewy(email):
    """Parse chewy tracking numbers."""
    tracking_numbers = []

    _LOGGER.error(email[EMAIL_ATTR_BODY])

    matches = re.findall(r'tracknumber_list=([0-9]+)', email[EMAIL_ATTR_BODY])
    _LOGGER.error(matches)
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    return tracking_numbers
