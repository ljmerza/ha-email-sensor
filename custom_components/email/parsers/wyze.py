import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_WYZE = 'wyze'
EMAIL_DOMAIN_WYZE = 'wyze.com'


def parse_wyze(email):
    """Parse Wyze tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    for link in links:
        if not link:
            continue
        match = re.search('tracking_numbers=(.*?)&', link)
        if match and match.group(1) not in tracking_numbers:
            tracking_numbers.append(match.group(1))

    matches = re.findall(r'tracking_numbers=(.*?)&', email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)


    return tracking_numbers
