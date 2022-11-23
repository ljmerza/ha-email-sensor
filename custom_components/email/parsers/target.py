import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_TARGET = 'target'
EMAIL_DOMAIN_TARGET = 'target.com'


def parse_target(email):
    """Parse Target tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    paragraphs = [paragraph.text for paragraph in soup.find_all('p')]
    for paragraph in paragraphs:
        if not paragraph:
            continue
        match = re.search('United Parcel Service Tracking # (\S{18})', paragraph)
        if match and match.group(1) not in tracking_numbers:
            tracking_numbers.append(match.group(1))

    return tracking_numbers
