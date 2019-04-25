# Home Assistant Email Sensor

Gets emails from SMTP and prases out any tracking numbers from FedEx, UPS, USPS, Rockauto, Newegg, B&H Photo, and Ali Express.

---

![](./sensor.png)

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

## Installation

Add the `email` folder in your `custom_components` folder.

## Options

| Name | Type | Requirement | `default` Description
| ---- | ---- | ------- | -----------
| email | string | **Required** | email address
| password | string | **Required** | email password
| smtp_server | string | **Optional** | `imap.gmail.com`  SMTP server address>
| smtp_port | number | **Optional** | `993` SMTP port
| folder | string | **Optional** | `INBOX` Which folder to pull emails from

```yaml
sensor:
  - platform: email
    email: !secret my_email
    password: !secret my_google_app_password
```


---

Enjoy my card? Help me out for a couple of :beers: or a :coffee:!

[![coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/JMISm06AD)


[commits-shield]: https://img.shields.io/github/commit-activity/y/ljmerza/ha-email-sensor.svg?style=for-the-badge
[commits]: https://github.com/ljmerza/ha-email-sensor/commits/master
[license-shield]: https://img.shields.io/github/license/ljmerza/ha-email-sensor.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Leonardo%20Merza%20%40ljmerza-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ljmerza/ha-email-sensor.svg?style=for-the-badge
[releases]: https://github.com/ljmerza/ha-email-sensor/releases
