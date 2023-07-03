import logging
import re
import math

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_THRIFT_BOOKS = 'thrift_books'
EMAIL_DOMAIN_THRIFT_BOOKS = 'thriftbooks'

track_copy_pattern = re.compile(r"track my package", re.IGNORECASE)
order_number_pattern = re.compile(r"Order #:\s+(\d+)")

def parse_thrift_books(email):
    """Parse thrift books tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    elements = soup.find_all('a')

    for element in elements:
        link = element.get('href')

        if not link:
            continue

        if 'spmailtechno' not in link:
            continue

        try:
            if re.search(track_copy_pattern, element.text):
              match = re.search(order_number_pattern, email[EMAIL_ATTR_BODY])
              if match:
                tracking_numbers.append({
                  'link': link,
                  'tracking_number': match.group(1)
                })
        except:
            pass

    return tracking_numbers
