import logging
import re
import math

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_HOME_DEPOT = 'home_depot'
EMAIL_DOMAIN_HOME_DEPOT = 'homedepot.com'


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

        try:
            tracking_number = element.text
            _LOGGER.error(tracking_number)
            isNan = math.isnan(int(tracking_number))

            if not isNan and tracking_number not in tracking_numbers:
                tracking_numbers.append(tracking_number)
        except:
            pass

    return tracking_numbers
