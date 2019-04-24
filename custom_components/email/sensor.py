"""Support for Google - Calendar Event Devices."""
from datetime import timedelta
import imaplib
import email
import logging

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

SCAN_INTERVAL = timedelta(seconds=300)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_SMTP_SERVER, default='imap.gmail.com'): cv.string,
    vol.Required(CONF_SMTP_PORT, default=993): cv.positive_int,
    vol.Required(CONF_EMAIL_FOLDER, default='INBOX'): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Email platform."""
    from imapclient import IMAPClient
    
    smtp_server = config[CONF_SMTP_SERVER]
    smtp_port = config[CONF_SMTP_PORT]

    email_address = config[CONF_EMAIL]
    password = config[CONF_PASSWORD]
    email_folder = config[CONF_EMAIL_FOLDER]

    try:
        server = IMAPClient(smtp_server, use_uid=True)
        server.login(email_address, password)
        select_info = server.select_folder(email_folder, readonly=True)
        add_entities([EmailEntity(server, config)], True)
        return True

    except Exception as err:
        _LOGGER.error(f'IMAPClient setup_platform error: {err}')
        return False


class EmailEntity(Entity):
    """Email Entity."""

    def __init__(self, server, config):
        """Init the Email Entity."""
        self.server = server
        self.email_address = config[CONF_EMAIL]

        self.emails = []
        self.email_count = 0

    def update(self):
        """Update data from Email API."""
        self.emails = []
        
        try: 
            messages = self.server.search('UNSEEN')
            for uid, message_data in self.server.fetch(messages, 'RFC822').items():
                try:
                    email_message = email.message_from_bytes(message_data[b'RFC822'])
                    try:
                        msg = str(email_message.get_payload(0))
                        self.emails.append({
                            'from': email_message.get('from'),
                            'subject': email_message.get('subject'),
                            'msg': msg
                        })
                    except Exception as err:
                        LOGGER.error(f'IMAPClient get_payload error: {err}')
                except Exception as err:
                    _LOGGER.error(f'IMAPClient message_from_bytes error: {err}')

        except Exception as err:
            _LOGGER.error(f'IMAPClient update error: {err}')

        self.email_count = len(self.emails)

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