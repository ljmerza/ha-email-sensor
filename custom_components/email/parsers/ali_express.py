import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
ATTR_ALI_EXPRESS = 'ali_express'
EMAIL_DOMAIN_ALI_EXPRESS = 'aliexpress.com'


def parse_ali_express(email):
    """Parse Ali Express tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    
    lines = [p_element.text for p_element in soup.find_all('p')]
    for line in lines:
        if not line:
            continue
        match = re.search('TRACKING NUMBER :(.*?)\.', line)
        if match and match.group(1) not in tracking_numbers:
            tracking_numbers.append(match.group(1))
    
    link_urls = [link.get('href') for link in soup.find_all('a')]
    for link in link_urls:
        if not link:
            continue
        order_number_match = re.search('orderId=(.*?)&', link)

        if order_number_match and order_number_match.group(1):
            order_number = order_number_match.group(1)
            order_numbers = list(map(lambda x: x['tracking_number'], tracking_numbers))
            if order_number not in order_numbers:
                tracking_numbers.append({
                    'link': link,
                    'tracking_number': order_number
                })

    return tracking_numbers
