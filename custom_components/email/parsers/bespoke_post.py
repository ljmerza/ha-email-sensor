import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_DSW = 'BESPOKE_POST'
EMAIL_DOMAIN_DSW = 'bespokepost.com'


def parse_bespoke_post(email):
    """Parse bespoke post tracking numbers."""
    tracking_numbers = []

    matches = re.findall(r'Tracking Number (.*?) ', email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    return tracking_numbers
