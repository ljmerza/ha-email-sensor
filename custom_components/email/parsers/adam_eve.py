import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_ADAM_AND_EVE  = 'adam_and_eve'
EMAIL_DOMAIN_ADAM_AND_EVE = 'adamandeve.com'


def parse_adam_and_eve(email):
    """Parse Adam & Eve tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    linkTexts = [link.text for link in soup.find_all('a')]
    for linkText in linkTexts:
        if not linkText:
            continue
        match = re.search('(\d{26})', linkText)
        if match and match.group(1).isnumeric() and match.group(1) not in tracking_numbers:
            tracking_numbers.append(match.group(1))

    return tracking_numbers
