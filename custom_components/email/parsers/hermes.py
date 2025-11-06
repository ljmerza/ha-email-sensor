import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT


_LOGGER = logging.getLogger(__name__)
ATTR_HERMES = 'hermes'
EMAIL_DOMAIN_HERMES = 'myhermes.de'


def parse_hermes(email):
    """Parse Hermes tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    # Hermes tracking patterns
    hermes_patterns = [
        r'Tracking-ID:\s*([A-Z0-9]{11,20})',
        r'Tracking\s+ID:\s*([A-Z0-9]{11,20})',
        r'Sendungsnummer:\s*([A-Z0-9]{11,20})',
        r'Sendungs-Nr\.:\s*([A-Z0-9]{11,20})',
        r'Paketnummer:\s*([A-Z0-9]{11,20})',
        r'Paket-Nr\.:\s*([A-Z0-9]{11,20})',
        r'Hermes\s+([A-Z0-9]{11,20})',
        r'([0-9]{11,20})',  # 11-20 digit numbers
    ]

    # Check body for tracking numbers
    for pattern in hermes_patterns:
        matches = re.findall(pattern, email[EMAIL_ATTR_BODY], re.IGNORECASE)
        for match in matches:
            tracking_number = match.strip()
            if tracking_number and tracking_number not in tracking_numbers:
                tracking_numbers.append(tracking_number)

    # Check subject for tracking numbers
    for pattern in hermes_patterns:
        matches = re.findall(pattern, email[EMAIL_ATTR_SUBJECT], re.IGNORECASE)
        for match in matches:
            tracking_number = match.strip()
            if tracking_number and tracking_number not in tracking_numbers:
                tracking_numbers.append(tracking_number)

    # Look for tracking numbers in links
    link_urls = [link.get('href') for link in soup.find_all('a')]
    for link in link_urls:
        if not link:
            continue
            
        # Look for tracking numbers in URLs
        url_patterns = [
            r'tracking-id=([A-Z0-9]{11,20})',
            r'track=([A-Z0-9]{11,20})',
            r'id=([A-Z0-9]{11,20})',
            r'/([A-Z0-9]{11,20})',
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, link)
            if match and match.group(1):
                tracking_number = match.group(1)
                if tracking_number not in tracking_numbers:
                    tracking_numbers.append({
                        'link': link,
                        'tracking_number': tracking_number
                    })
                break

    return tracking_numbers
