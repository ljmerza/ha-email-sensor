import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_PLEDGEBOX = 'pledgebox'
EMAIL_DOMAIN_PLEDGEBOX = 'pledgebox.com'


def parse_pledgebox(email):
    """Parse Pledge Box tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    lines = [element.text for element in soup.find_all('td')]
    for line in lines:
        if not line:
            continue
        match = re.search('^(\d{12})$', line)
        _LOGGER.error(match)

        if match and match.group(1) not in tracking_numbers:
            tracking_numbers.append(match.group(1))

    return tracking_numbers
