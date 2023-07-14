import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT


_LOGGER = logging.getLogger(__name__)
ATTR_LOWES = 'lowes'
EMAIL_DOMAIN_LOWES = 'lowes.com'

def parse_lowes(email):
    """Parse Lowes tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    elements = soup.find_all('span')

    for element in elements:
        if 'Tracking #' in element.text:
          anchor = element.findChild("a" , recursive=False)
          link = anchor.get('href')

          order_number = re.search(r'#(\d+)', email[EMAIL_ATTR_SUBJECT])
          if order_number:
              tracking_numbers.append({
                'link': link,
                'tracking_number': order_number.group(1)
              })

    return tracking_numbers
