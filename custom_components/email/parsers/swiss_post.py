import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY

_LOGGER = logging.getLogger(__name__)
ATTR_SWISS_POST = 'swiss_post'
EMAIL_DOMAIN_SWISS_POST = 'post.ch'


def parse_swiss_post(email):
    """Parse Swiss Post tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    for link in links:
        if not link:
            continue
        match = re.search('formattedParcelCodes=(\d+)', link)
        if match and match.group(1) not in tracking_numbers:
            tracking_numbers.append(match.group(1))

    return tracking_numbers
