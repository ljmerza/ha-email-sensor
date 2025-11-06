import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT


_LOGGER = logging.getLogger(__name__)
ATTR_ALI_EXPRESS = 'ali_express'
EMAIL_DOMAIN_ALI_EXPRESS = 'aliexpress.com'


def parse_ali_express(email):
    """Parse AliExpress tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')
    
    # Look for tracking numbers in various formats
    # German patterns
    tracking_patterns = [
        r'TRACKING NUMBER\s*:\s*(.*?)\.',
        r'Paket\s+(\d{20,24})',
        r'Paket\s+([A-Z0-9]{12,24})',
        r'Tracking-Nummer\s*:\s*(.*?)\.',
        r'Tracking\s*:\s*(.*?)\.',
        r'TRACKING\s*:\s*(.*?)\.',
        r'Tracking\s+Number\s*:\s*(.*?)\.',
        r'Tracking\s+Number\s*:\s*(.*?)\.',
    ]
    
    # Check body for tracking numbers
    for pattern in tracking_patterns:
        matches = re.findall(pattern, email[EMAIL_ATTR_BODY], re.IGNORECASE)
        for match in matches:
            tracking_number = match.strip()
            if tracking_number and tracking_number not in tracking_numbers:
                tracking_numbers.append(tracking_number)
    
    # Check subject for tracking numbers
    for pattern in tracking_patterns:
        matches = re.findall(pattern, email[EMAIL_ATTR_SUBJECT], re.IGNORECASE)
        for match in matches:
            tracking_number = match.strip()
            if tracking_number and tracking_number not in tracking_numbers:
                tracking_numbers.append(tracking_number)
    
    # Look for order numbers in links
    link_urls = [link.get('href') for link in soup.find_all('a')]
    for link in link_urls:
        if not link:
            continue
            
        # Various order ID patterns
        order_patterns = [
            r'orderId=([^&]+)',
            r'order_id=([^&]+)',
            r'order=([^&]+)',
            r'id=([^&]+)',
        ]
        
        for pattern in order_patterns:
            order_number_match = re.search(pattern, link)
            if order_number_match and order_number_match.group(1):
                order_number = order_number_match.group(1)
                
                # Check if we already have this order number
                existing_numbers = []
                for item in tracking_numbers:
                    if isinstance(item, dict):
                        existing_numbers.append(item.get('tracking_number', ''))
                    else:
                        existing_numbers.append(item)
                        
                if order_number not in existing_numbers:
                    tracking_numbers.append({
                        'link': link,
                        'tracking_number': order_number
                    })
                break

    return tracking_numbers
