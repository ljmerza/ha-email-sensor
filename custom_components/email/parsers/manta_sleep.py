import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_MANTA_SLEEP = 'manta_sleep'
EMAIL_DOMAIN_MANTA_SLEEP = 'mantasleep.com'


def parse_manta_sleep(email):
    """Parse Manta Sleep tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    link_urls = [link.get('href') for link in soup.find_all('a')]
    for link in link_urls:
        if not link:
            continue
        match = re.search('trackingnumber=(.*?)$', link)
        if match and match.group(1) not in tracking_numbers:
            tracking_numbers.append(match.group(1))

    return tracking_numbers
