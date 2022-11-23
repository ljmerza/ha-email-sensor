import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT


_LOGGER = logging.getLogger(__name__)
ATTR_AMAZON = 'amazon'
EMAIL_DOMAIN_AMAZON = 'amazon.com'

def parse_amazon(email):
    """Parse Amazon tracking numbers."""
    tracking_numbers = []
 
    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    # see if it's an shipped order email
    order_number_match = re.search('Your AmazonSmile order #(.*?) has shipped', email[EMAIL_ATTR_SUBJECT])
    if not order_number_match:
        order_number_match = re.search('Your Amazon.com order #(.*?) has shipped', email[EMAIL_ATTR_SUBJECT])
    if not order_number_match:
        return tracking_numbers

    order_number = order_number_match.group(1)

    # find the link that has 'track package' text
    linkElements = soup.find_all('a')
    for linkElement in linkElements:
        if not re.search(r'track package', linkElement.text, re.IGNORECASE):
            continue
        
        # if found we no get url and check for duplicates
        link = linkElement.get('href')

        # make sure we dont have dupes
        order_numbers = list(map(lambda x: x['tracking_number'], tracking_numbers))
        if order_number not in order_numbers:
            tracking_numbers.append({
                'link': link,
                'tracking_number': order_number
            })

    return tracking_numbers
