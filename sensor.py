"""Support for Google - Calendar Event Devices."""
from datetime import timedelta
import imaplib
import email
import json
import logging
import smtplib

import voluptuous as vol

from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity


_LOGGER = logging.getLogger(__name__)

DOMAIN = 'email'

CONF_SMTP_SERVER = 'smtp_server'
CONF_SMTP_PORT = 'smpt_port'
CONF_EMAIL_FOLDER = 'folder'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_SMTP_SERVER, default='imap.gmail.com'): cv.string,
    vol.Required(CONF_SMTP_PORT, default=993): cv.positive_int,
    vol.Required(CONF_EMAIL_FOLDER, default='INBOX'): cv.string,
})

SCAN_INTERVAL = timedelta(minutes=3)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Email platform."""
    email_address = config[CONF_EMAIL]
    password = config[CONF_PASSWORD]
    smtp_server = config[CONF_SMTP_SERVER]
    smtp_port = config[CONF_SMTP_PORT]
    email_folder = config[CONF_EMAIL_FOLDER]

    try:
        imap = imaplib.IMAP4_SSL(smtp_server)
        imap.login(email_address, password)
        
        rv, data = imap.select(email_folder, readonly=True)
        if rv != 'OK':
            _LOGGER.error(f'IMAP4 error: {err}')
            return False

        add_entities([EmailEntity(imap, email_address)], True)
        return True

    except imaplib.IMAP4.error as err:
        _LOGGER.error(f'IMAP4 error: {err}')
        return False


class EmailEntity(Entity):
    """Email Entity."""

    def __init__(self, imap, email_address):
        """Init the Email Entity."""
        self.imap = imap
        self.email_address = email_address
        self.emails = []
        self.email_count = 0

    @property
    def name(self):
        """Return the name of the sensor."""
        return f'email_{self.email_address}'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.email_count

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            'emails': self.emails,
            'count': self.email_count
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return 'mdi:email'

    def update(self):
        """Update data from Email API."""
        self.emails = []
        self.email_count = 0
        
        try: 
            status, sdata = self.imap.search(None, 'UNSEEN')
        except imaplib.IMAP4.error as err:
            _LOGGER.error(f'IMAP4 search error: {err}')

        mail_ids = sdata[0]

        id_list = mail_ids.split()
        self.email_count = len(id_list)
        
        for i in id_list:
            try:
                typ, data = self.imap.fetch(i, '(RFC822)')
                if typ != 'OK':
                    _LOGGER.error(f'IMAP4 fetch error: {data}')
                    continue
            except imaplib.IMAP4.error as err:
                _LOGGER.error(f'IMAP4 fetch error: {err}')

            try:
                msg = email.message_from_string(data[0][1].decode('UTF-8'))
                self.emails.append({
                    'from': msg.get('from'),
                    'subject': msg.get('subject'),
                    'msg': str(msg.get_payload(0))
                })
            except TypeError as err:
                _LOGGER.error(f'IMAP4 update error: {err}')