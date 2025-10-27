import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT


_LOGGER = logging.getLogger(__name__)
ATTR_AMAZON_DE = 'amazon_de'
EMAIL_DOMAIN_AMAZON_DE = 'amazon.de'

def parse_amazon_de(email):
    """Parse Amazon.de tracking numbers."""
    tracking_numbers = []
 
    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    # German order number patterns
    order_number_match = re.search(r'Order: #(.*?)\n', email[EMAIL_ATTR_BODY])
    if not order_number_match:
        order_number_match = re.search(r'Bestellnr\.\s*(.*?)\s', email[EMAIL_ATTR_BODY])
    if not order_number_match:
        order_number_match = re.search(r'Bestellung\s*(.*?)\s', email[EMAIL_ATTR_BODY])
    if not order_number_match:
        # Check subject for German patterns
        order_number_match = re.search(r'Bestellung\s*(.*?)\s', email[EMAIL_ATTR_SUBJECT])
    if not order_number_match:
        order_number_match = re.search(r'Bestellnr\.\s*(.*?)\s', email[EMAIL_ATTR_SUBJECT])
    if not order_number_match:
        # Check for order ID in URLs
        order_number_match = re.search(r'orderId=([^&]+)', email[EMAIL_ATTR_BODY])
    if not order_number_match:
        # Check for shipment ID
        order_number_match = re.search(r'shipmentId=([^&]+)', email[EMAIL_ATTR_BODY])

    if order_number_match:
        order_number = order_number_match.group(1).strip()
        
        # Find tracking links (German and English)
        linkElements = soup.find_all('a')
        tracking_link = None
        
        for linkElement in linkElements:
            link_text = linkElement.text.lower()
            if any(keyword in link_text for keyword in ['track', 'verfolgen', 'paket verfolgen', 'lieferung verfolgen']):
                tracking_link = linkElement.get('href')
                break
        
        # If no specific tracking link found, look for any Amazon tracking URL
        if not tracking_link:
            for linkElement in linkElements:
                href = linkElement.get('href', '')
                if 'amazon.de' in href and ('track' in href or 'progress-tracker' in href):
                    tracking_link = href
                    break

        # Make sure we don't have duplicates
        order_numbers = []
        for item in tracking_numbers:
            if isinstance(item, dict):
                order_numbers.append(item.get('tracking_number', ''))
            else:
                order_numbers.append(item)
                
        if order_number not in order_numbers:
            tracking_numbers.append({
                'link': tracking_link or f'https://www.amazon.de/gp/your-account/order-history',
                'tracking_number': order_number
            })

    return tracking_numbers