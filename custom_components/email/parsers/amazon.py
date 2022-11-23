import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY
from ..const import EMAIL_ATTR_SUBJECT

_LOGGER = logging.getLogger(__name__)
ATTR_AMAZON = 'amazon'
EMAIL_DOMAIN_AMAZON = 'amazon.com'


def parse_amazon(email):
    """Parse Amazon tracking numbers."""
    tracking_numbers = []
 
    match = re.search('Your AmazonSmile order #(.*?) has shipped', email[EMAIL_ATTR_SUBJECT])
    if match and match.group(1) not in tracking_numbers:
        tracking_numbers.append(match.group(1))
    
    return tracking_numbers
