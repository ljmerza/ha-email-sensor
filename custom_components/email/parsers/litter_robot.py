import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_LITTER_ROBOT= 'litter_robot'
EMAIL_DOMAIN_LITTER_ROBOT = 'litter-robot.com'


def parse_litter_robot(email):
    """Parse Litter Robot tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    elements = soup.find_all('a')
    for element in elements:
        link = element.get('href')
        if not link:
            continue
        if 'shipping/tracking' in link:
            tracking_number = element.text
            if tracking_number and tracking_number not in tracking_numbers:
                tracking_numbers.append(tracking_number.strip())

    return tracking_numbers
