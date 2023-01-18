import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT


_LOGGER = logging.getLogger(__name__)
ATTR_UBIQUITI  = 'ubiquiti'
EMAIL_DOMAIN_UBIQUITI = 'shopifyemail.com'


def parse_ubiquiti(email):
    """Parse Ubiquiti tracking numbers."""
    tracking_numbers = []
    _LOGGER.error(email)

    # see if it's an shipped order email
    order_number_match = re.search('A shipment from order #(.*?) is on the way', email[EMAIL_ATTR_SUBJECT])
    _LOGGER.error(order_number_match)
    if not order_number_match:
        return tracking_numbers
    
    order_number = order_number_match.group(1)

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    links = [link.href for link in soup.find_all('a')]
    for link in links:
        if not link:
            continue
        match = re.search('/(\d{26})/orders/', link)
        if match and link not in tracking_numbers:
            tracking_numbers.append({
              "tracking_number": order_number,
              "link": link,
            })

    return tracking_numbers
