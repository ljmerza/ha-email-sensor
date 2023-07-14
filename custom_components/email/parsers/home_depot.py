import logging
import re
import math

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_HOME_DEPOT = 'home_depot'
EMAIL_DOMAIN_HOME_DEPOT = 'homedepot.com'


track_copy_pattern = re.compile(r"track my order", re.IGNORECASE)
order_number_pattern = re.compile(r"^[A-Za-z]{2}\d{8}$")

def parse_home_depot(email):
    """Parse home depot tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    elements = soup.find_all('a')

    for element in elements:
        link = element.get('href')

        if not link:
            continue

        if 'link.order.homedepot.com' not in link:
            continue

        match = re.search(order_number_pattern, element.text)

        if match:
            tracking_numbers.append({
                'link': link,
                'tracking_number': match.group()
            })


    return tracking_numbers
