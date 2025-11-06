import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, USPS_TRACKING_NUMBER_REGEX, UPS_TRACKING_NUMBER_REGEX, FEDEX_TRACKING_NUMBER_REGEX

_LOGGER = logging.getLogger(__name__)
ATTR_GENERIC = 'generic'
EMAIL_DOMAIN_GENERIC = ''

def parse_generic(email):
    """Tries to parse tracking numbers for any type of email."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    # Original patterns
    matches = re.findall(UPS_TRACKING_NUMBER_REGEX, email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    matches = re.findall(USPS_TRACKING_NUMBER_REGEX, email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    # German tracking number patterns
    german_patterns = [
        # DHL patterns
        r'\b(DE[0-9]{10,})\b',
        r'\b([0-9]{20})\b',
        r'\b([0-9]{10,11})\b',
        
        # Hermes patterns
        r'\b([0-9]{11,20})\b',
        
        # GLS patterns
        r'\b([0-9]{11,12})\b',
        
        # DPD patterns
        r'\b([0-9]{11,20})\b',
        
        # Generic German patterns
        r'Sendungsnummer:\s*([A-Z0-9]{10,20})',
        r'Paketnummer:\s*([A-Z0-9]{10,20})',
        r'Tracking-ID:\s*([A-Z0-9]{10,20})',
        r'Tracking\s+ID:\s*([A-Z0-9]{10,20})',
    ]

    # Check for German tracking patterns
    for pattern in german_patterns:
        matches = re.findall(pattern, email[EMAIL_ATTR_BODY], re.IGNORECASE)
        for match in matches:
            tracking_number = match.strip()
            if tracking_number and tracking_number not in tracking_numbers:
                tracking_numbers.append(tracking_number)

    return tracking_numbers
