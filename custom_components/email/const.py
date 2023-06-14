"""Constants for Email Platform."""

DOMAIN = 'email'

CONF_EMAIL = 'email'
CONF_PASSWORD = 'password'
CONF_IMAP_SERVER = 'imap_server'
CONF_IMAP_PORT = 'imap_port'
CONF_EMAIL_FOLDER = 'folder'
CONF_SSL = 'ssl'
CONF_DAYS_OLD = 'days_old'

ATTR_COUNT = 'count'
ATTR_TRACKING_NUMBERS = 'tracking_numbers'

EMAIL_ATTR_FROM = 'from'
EMAIL_ATTR_SUBJECT = 'subject'
EMAIL_ATTR_BODY = 'body'

USPS_TRACKING_NUMBER_REGEX = r"\b(94\d{20}|\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{2})\b"
UPS_TRACKING_NUMBER_REGEX = r"\b(1Z[A-HJ-NP-Z0-9]{16})\b"
FEDEX_TRACKING_NUMBER_REGEX = r"\b(\d{12})\b"

EMAIL_DOMAIN_REGEX = r"@([\w.-]+)"