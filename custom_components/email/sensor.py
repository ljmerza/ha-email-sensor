"""Support for Google - Calendar Event Devices."""
from datetime import timedelta, date
import logging
import re

from imapclient import IMAPClient
from mailparser import parse_from_bytes
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

from .const import (
    CONF_EMAIL, CONF_PASSWORD, CONF_IMAP_SERVER,
    CONF_IMAP_PORT, CONF_SSL, CONF_EMAIL_FOLDER, CONF_DAYS_OLD,
    ATTR_TRACKING_NUMBERS, EMAIL_ATTR_FROM, EMAIL_ATTR_SUBJECT,
    EMAIL_ATTR_BODY, ATTR_COUNT)

from .parsers.ups import ATTR_UPS, EMAIL_DOMAIN_UPS, parse_ups
from .parsers.amazon import ATTR_AMAZON, EMAIL_DOMAIN_AMAZON, parse_amazon
from .parsers.fedex import ATTR_FEDEX, EMAIL_DOMAIN_FEDEX, parse_fedex
from .parsers.paypal import ATTR_PAYPAL, EMAIL_DOMAIN_PAYPAL, parse_paypal
from .parsers.usps import ATTR_USPS, EMAIL_DOMAIN_USPS, parse_usps
from .parsers.ali_express import ATTR_ALI_EXPRESS, EMAIL_DOMAIN_ALI_EXPRESS, parse_ali_express
from .parsers.newegg import ATTR_NEWEGG, EMAIL_DOMAIN_NEWEGG, parse_newegg
from .parsers.rockauto import ATTR_ROCKAUTO, EMAIL_DOMAIN_ROCKAUTO, parse_rockauto
from .parsers.bh_photo import ATTR_BH_PHOTO, EMAIL_DOMAIN_BH_PHOTO, parse_bh_photo
from .parsers.ebay import ATTR_EBAY, EMAIL_DOMAIN_EBAY, parse_ebay
from .parsers.dhl import ATTR_DHL, EMAIL_DOMAIN_DHL, parse_dhl
from .parsers.hue import ATTR_HUE, EMAIL_DOMAIN_HUE, parse_hue
from .parsers.google_express import ATTR_GOOGLE_EXPRESS, EMAIL_DOMAIN_GOOGLE_EXPRESS, parse_google_express
from .parsers.western_digital import ATTR_WESTERN_DIGITAL, EMAIL_DOMAIN_WESTERN_DIGITAL, parse_western_digital
from .parsers.monoprice import ATTR_MONOPRICE, EMAIL_DOMAIN_MONOPRICE, parse_monoprice
from .parsers.georgia_power import ATTR_GEORGIA_POWER, EMAIL_DOMAIN_GEORGIA_POWER, parse_georgia_power
from .parsers.best_buy import ATTR_BEST_BUY, EMAIL_DOMAIN_BEST_BUY, parse_best_buy
from .parsers.dollar_shave_club import ATTR_DOLLAR_SHAVE_CLUB, EMAIL_DOMAIN_DOLLAR_SHAVE_CLUB, parse_dollar_shave_club
from .parsers.nuleaf import ATTR_NULEAF, EMAIL_DOMAIN_NULEAF, parse_nuleaf
from .parsers.timeless import ATTR_TIMELESS, EMAIL_DOMAIN_TIMLESS, parse_timeless
from .parsers.dsw import ATTR_DSW, EMAIL_DOMAIN_DSW, parse_dsw
from .parsers.wyze import ATTR_WYZE, EMAIL_DOMAIN_WYZE, parse_wyze
from .parsers.reolink import ATTR_REOLINK, EMAIL_DOMAIN_REOLINK, parse_reolink
from .parsers.chewy import ATTR_CHEWY, EMAIL_DOMAIN_CHEWY, parse_chewy
from .parsers.groupon import ATTR_GROUPON, EMAIL_DOMAIN_GROUPON, parse_groupon
from .parsers.zazzle import ATTR_ZAZZLE, EMAIL_DOMAIN_ZAZZLE, parse_zazzle
from .parsers.home_depot import ATTR_HOME_DEPOT, EMAIL_DOMAIN_HOME_DEPOT, parse_home_depot
from .parsers.swiss_post import ATTR_SWISS_POST, EMAIL_DOMAIN_SWISS_POST, parse_swiss_post
from .parsers.bespoke_post import ATTR_DSW, EMAIL_DOMAIN_DSW, parse_bespoke_post
from .parsers.manta_sleep import ATTR_MANTA_SLEEP, EMAIL_DOMAIN_MANTA_SLEEP, parse_manta_sleep
from .parsers.prusa import ATTR_PRUSA, EMAIL_DOMAIN_PRUSA, parse_prusa
from .parsers.adam_eve import ATTR_ADAM_AND_EVE, EMAIL_DOMAIN_ADAM_AND_EVE, parse_adam_and_eve
from .parsers.target import ATTR_TARGET, EMAIL_DOMAIN_TARGET, parse_target
from .parsers.gamestop import ATTR_GAMESTOP, EMAIL_DOMAIN_GAMESTOP, parse_gamestop
from .parsers.litter_robot import ATTR_LITTER_ROBOT, EMAIL_DOMAIN_LITTER_ROBOT, parse_litter_robot
from .parsers.the_smartest_house import ATTR_SMARTEST_HOUSE, EMAIL_DOMAIN_SMARTEST_HOUSE, parse_smartest_house
from .parsers.ubiquiti import ATTR_UBIQUITI, EMAIL_DOMAIN_UBIQUITI, parse_ubiquiti
from .parsers.nintendo import ATTR_NINTENDO, EMAIL_DOMAIN_NINTENDO, parse_nintendo
from .parsers.pledgebox import ATTR_PLEDGEBOX, EMAIL_DOMAIN_PLEDGEBOX, parse_pledgebox
from .parsers.guitar_center import ATTR_GUITAR_CENTER, EMAIL_DOMAIN_GUITAR_CENTER, parse_guitar_center
from .parsers.sony import ATTR_SONY, EMAIL_DOMAIN_SONY, parse_sony


parsers = [
    (ATTR_UPS, EMAIL_DOMAIN_UPS, parse_ups),
    (ATTR_FEDEX, EMAIL_DOMAIN_FEDEX, parse_fedex),
    (ATTR_AMAZON, EMAIL_DOMAIN_AMAZON, parse_amazon),
    (ATTR_PAYPAL, EMAIL_DOMAIN_PAYPAL, parse_paypal),
    (ATTR_USPS, EMAIL_DOMAIN_USPS, parse_usps),
    (ATTR_ALI_EXPRESS, EMAIL_DOMAIN_ALI_EXPRESS, parse_ali_express),
    (ATTR_NEWEGG, EMAIL_DOMAIN_NEWEGG, parse_newegg),
    (ATTR_ROCKAUTO, EMAIL_DOMAIN_ROCKAUTO, parse_rockauto),
    (ATTR_BH_PHOTO, EMAIL_DOMAIN_BH_PHOTO, parse_bh_photo),
    (ATTR_EBAY, EMAIL_DOMAIN_EBAY, parse_ebay),
    (ATTR_DHL, EMAIL_DOMAIN_DHL, parse_dhl),
    (ATTR_HUE, EMAIL_DOMAIN_HUE, parse_hue),
    (ATTR_GOOGLE_EXPRESS, EMAIL_DOMAIN_GOOGLE_EXPRESS, parse_google_express),
    (ATTR_WESTERN_DIGITAL, EMAIL_DOMAIN_WESTERN_DIGITAL, parse_western_digital),
    (ATTR_MONOPRICE, EMAIL_DOMAIN_MONOPRICE, parse_monoprice),
    (ATTR_GEORGIA_POWER, EMAIL_DOMAIN_GEORGIA_POWER, parse_georgia_power),
    (ATTR_BEST_BUY, EMAIL_DOMAIN_BEST_BUY, parse_best_buy),
    (ATTR_DOLLAR_SHAVE_CLUB, EMAIL_DOMAIN_DOLLAR_SHAVE_CLUB, parse_dollar_shave_club),
    (ATTR_NULEAF, EMAIL_DOMAIN_NULEAF, parse_nuleaf),
    (ATTR_TIMELESS, EMAIL_DOMAIN_TIMLESS, parse_timeless),
    (ATTR_DSW, EMAIL_DOMAIN_DSW, parse_dsw),
    (ATTR_WYZE, EMAIL_DOMAIN_WYZE, parse_wyze),
    (ATTR_REOLINK, EMAIL_DOMAIN_REOLINK, parse_reolink),
    (ATTR_CHEWY, EMAIL_DOMAIN_CHEWY, parse_chewy),
    (ATTR_GROUPON, EMAIL_DOMAIN_GROUPON, parse_groupon),
    (ATTR_ZAZZLE, EMAIL_DOMAIN_ZAZZLE, parse_zazzle),
    (ATTR_HOME_DEPOT, EMAIL_DOMAIN_HOME_DEPOT, parse_home_depot),
    (ATTR_SWISS_POST, EMAIL_DOMAIN_SWISS_POST, parse_swiss_post),
    (ATTR_DSW, EMAIL_DOMAIN_DSW, parse_bespoke_post),
    (ATTR_MANTA_SLEEP, EMAIL_DOMAIN_MANTA_SLEEP, parse_manta_sleep),
    (ATTR_PRUSA, EMAIL_DOMAIN_PRUSA, parse_prusa),
    (ATTR_ADAM_AND_EVE, EMAIL_DOMAIN_ADAM_AND_EVE, parse_adam_and_eve),
    (ATTR_TARGET, EMAIL_DOMAIN_TARGET, parse_target),
    (ATTR_GAMESTOP, EMAIL_DOMAIN_GAMESTOP, parse_gamestop),
    (ATTR_LITTER_ROBOT, EMAIL_DOMAIN_LITTER_ROBOT, parse_litter_robot),
    (ATTR_SMARTEST_HOUSE, EMAIL_DOMAIN_SMARTEST_HOUSE, parse_smartest_house),
    (ATTR_UBIQUITI, EMAIL_DOMAIN_UBIQUITI, parse_ubiquiti),
    (ATTR_NINTENDO, EMAIL_DOMAIN_NINTENDO, parse_nintendo),
    (ATTR_PLEDGEBOX, EMAIL_DOMAIN_PLEDGEBOX, parse_pledgebox),
    (ATTR_GUITAR_CENTER, EMAIL_DOMAIN_GUITAR_CENTER, parse_guitar_center),
    (ATTR_SONY, EMAIL_DOMAIN_SONY, parse_sony),
]

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'email'
SCAN_INTERVAL = timedelta(seconds=5*60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_DAYS_OLD, default='30'): cv.positive_int,
    vol.Required(CONF_IMAP_SERVER, default='imap.gmail.com'): cv.string,
    vol.Required(CONF_IMAP_PORT, default=993): cv.positive_int,
    vol.Required(CONF_SSL, default=True): cv.boolean,
    vol.Required(CONF_EMAIL_FOLDER, default='INBOX'): cv.string,
})

TRACKING_NUMBER_URLS = {
  'ups': "https://www.ups.com/track?loc=en_US&tracknum=",
  'usps': "https://tools.usps.com/go/TrackConfirmAction?tLabels=",
  'fedex': "https://www.fedex.com/apps/fedextrack/?tracknumbers=",
  'dhl': 'https://www.logistics.dhl/us-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=',
  'swiss_post': 'https://www.swisspost.ch/track?formattedParcelCodes=',
  'unknown': 'https://www.google.com/search?q=',
}

   
usps_pattern = [
    '^(94|93|92|94|95)[0-9]{20}$',
    '^(94|93|92|94|95)[0-9]{22}$',
    '^(70|14|23|03)[0-9]{14}$',
    '^(M0|82)[0-9]{8}$',
    '^([A-Z]{2})[0-9]{9}([A-Z]{2})$'
]

ups_pattern = [
    '^(1Z)[0-9A-Z]{16}$',
    '^(T)+[0-9A-Z]{10}$',
    '^[0-9]{9}$',
    '^[0-9]{26}$'
]

fedex_pattern = [
    '^[0-9]{20}$',
    '^[0-9]{15}$',
    '^[0-9]{12}$',
    '^[0-9]{22}$'
]

usps_regex = "(" + ")|(".join(usps_pattern) + ")"
fedex_regex = "(" + ")|(".join(fedex_pattern) + ")"
ups_regex = "(" + ")|(".join(ups_pattern) + ")"

def find_carrier(tracking_number, email_domain):

    # we may have the carrier/link already parsed from parser
    if type(tracking_number) is dict:
        return {
            'tracking_number': tracking_number['tracking_number'],
            'carrier': email_domain,
            'origin': email_domain,
            'link': tracking_number['link'],
        }

    link = ""
    carrier = ""

    # if tracking number is a url then use that
    if tracking_number.startswith('http'):
        link = tracking_number
        carrier = email_domain

    # if from carrier themself then use that
    elif email_domain == EMAIL_DOMAIN_UPS:
        link = TRACKING_NUMBER_URLS["ups"]
        carrier = "UPS"
    elif email_domain == EMAIL_DOMAIN_FEDEX:
        link = TRACKING_NUMBER_URLS["fedex"]
        carrier = "FedEx"
    elif email_domain == EMAIL_DOMAIN_USPS:
        link = TRACKING_NUMBER_URLS["usps"]
        carrier = "USPS"
    elif email_domain == EMAIL_DOMAIN_DHL:
        link = TRACKING_NUMBER_URLS["dhl"]
        carrier = "DHL"
    elif email_domain == EMAIL_DOMAIN_SWISS_POST:
        link = TRACKING_NUMBER_URLS["swiss_post"]
        carrier = "Swiss Post"
    
    # regex tracking number
    elif re.search(usps_regex, tracking_number) != None:
        link = TRACKING_NUMBER_URLS["usps"]
        carrier = 'USPS'
    elif re.search(ups_regex, tracking_number) != None:
        link = TRACKING_NUMBER_URLS["ups"]
        carrier = 'UPS'
    elif re.search(fedex_regex, tracking_number) != None:
        link = TRACKING_NUMBER_URLS["fedex"]
        carrier = 'FedEx'
        
    # try one more time
    else:
        isNumber = tracking_number.isnumeric()
        length = len(tracking_number)

        if (isNumber and (length == 12 or length == 15 or length == 20)):
            link = TRACKING_NUMBER_URLS["fedex"]
            carrier = "FedEx"
        elif (isNumber and length == 22):
            link = TRACKING_NUMBER_URLS["usps"]
            carrier = "USPS"
        elif (length > 25):
            link = TRACKING_NUMBER_URLS["dhl"]
            carrier = "DHL"
        else:
            link = TRACKING_NUMBER_URLS["unknown"]
            carrier = email_domain

    return {
        'tracking_number': tracking_number,
        'carrier': carrier,
        'origin': email_domain,
        'link': f'{link}{tracking_number}',
    }

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Email platform."""
    add_entities([EmailEntity(config)], True)


class EmailEntity(Entity):
    """Email Entity."""

    def __init__(self, config):
        """Init the Email Entity."""
        self._attr = {
            ATTR_TRACKING_NUMBERS: {},
	        ATTR_COUNT: 0
        }

        self.imap_server = config[CONF_IMAP_SERVER]
        self.imap_port = config[CONF_IMAP_PORT]
        self.email_address = config[CONF_EMAIL]
        self.password = config[CONF_PASSWORD]
        self.email_folder = config[CONF_EMAIL_FOLDER]
        self.ssl = config[CONF_SSL]
        self.days_old = int(config[CONF_DAYS_OLD])

        self.flag = [u'SINCE', date.today() - timedelta(days=self.days_old)]

    def update(self):
        """Update data from Email API."""
        self._attr = {
            ATTR_TRACKING_NUMBERS: {},
	        ATTR_COUNT: 0
        }

        # update to current day
        self.flag = [u'SINCE', date.today() - timedelta(days=self.days_old)]
        _LOGGER.debug(f'flag: {self.flag}')

        emails = []
        server = IMAPClient(self.imap_server, port=self.imap_port, use_uid=True, ssl=self.ssl)

        try:
            server.login(self.email_address, self.password)
            server.select_folder(self.email_folder, readonly=True)
        except Exception as err:
            _LOGGER.error('IMAPClient login error {}'.format(err))
            return False

        try:
            messages = server.search(self.flag)
            for uid, message_data in server.fetch(messages, 'RFC822').items():
                try:
                    mail = parse_from_bytes(message_data[b'RFC822'])
                    
                    emails.append({
                        EMAIL_ATTR_FROM: mail.from_,
                        EMAIL_ATTR_SUBJECT: mail.subject,
                        EMAIL_ATTR_BODY: mail.body
                    })
                except Exception as err:
                    _LOGGER.warning(
                        'mailparser parse_from_bytes error: {}'.format(err))

        except Exception as err:
            _LOGGER.error('IMAPClient update error: {}'.format(err))

        # empty out all parser arrays
        for ATTR, EMAIL_DOMAIN, parser in parsers:
            self._attr[ATTR_TRACKING_NUMBERS][ATTR] = []

        # for each email run each parser and save in the corresponding ATTR
        for email in emails:
            email_from = email[EMAIL_ATTR_FROM]
            if isinstance(email_from, (list, tuple)):
                email_from = list(email_from)
                email_from = ''.join(list(email_from[0]))
            
            # run through all parsers for each email if email domain matches
            for ATTR, EMAIL_DOMAIN, parser in parsers:
                try:
                    if EMAIL_DOMAIN in email_from:
                        self._attr[ATTR_TRACKING_NUMBERS][ATTR] = self._attr[ATTR_TRACKING_NUMBERS][ATTR] + parser(email=email)
                except Exception as err:
                    _LOGGER.error('{} error: {}'.format(ATTR, err))

        counter = 0                    
        # remove duplicates
        for ATTR, EMAIL_DOMAIN, parser in parsers:
            tracking_numbers = self._attr[ATTR_TRACKING_NUMBERS][ATTR]
            if len(tracking_numbers) > 0 and isinstance(tracking_numbers[0], str):
                self._attr[ATTR_TRACKING_NUMBERS][ATTR] = list(
                    dict.fromkeys(tracking_numbers))

        # format tracking numbers to add carrier type
        for ATTR, EMAIL_DOMAIN, parser in parsers:
            tracking_numbers = self._attr[ATTR_TRACKING_NUMBERS][ATTR]
            self._attr[ATTR_TRACKING_NUMBERS][ATTR] = list(map(lambda x: find_carrier(x, EMAIL_DOMAIN), tracking_numbers))
            _LOGGER.debug(self._attr[ATTR_TRACKING_NUMBERS][ATTR])
        counter = counter + len(tracking_numbers)

        self._attr[ATTR_COUNT] = counter
        server.logout()

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'email_{}'.format(self.email_address)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._attr[ATTR_COUNT]

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attr

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return 'mdi:email'
