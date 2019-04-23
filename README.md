# Home Assistant Email Sensor

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

## Installation

Add the `sensor.py` file to an `email` folder in your `custom_components` folder.

## Options

| Name | Type | Requirement | `default` Description
| ---- | ---- | ------- | -----------
| email | string | **Required** | email address
| password | string | **Required** | email password
| smtp_server | string | **Optional** | `imap.gmail.com`  SMTP server address>
| smpt_port | number | **Optional** | `993` SMTP port
| folder | string | **Optional** | `INBOX` Which folder to pull emails from

```yaml
sensor:
  - platform: email
    email: !secret my_email
    password: !secret my_google_app_password
```

## Node-RED

`node-red` folder contains Node-RED flows for parsing emails from this email sensor such as parsing tracking numbers from USPS emails. Users can contribute or update flows via pull requests. Each flow has it's own folder with the flow JSON file and a README describing what it does and any `yaml` needed for home assistant.

---

Enjoy my card? Help me out for a couple of :beers: or a :coffee:!

[![coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/JMISm06AD)


[commits-shield]: https://img.shields.io/github/commit-activity/y/ljmerza/hass-email-sensor.svg?style=for-the-badge
[commits]: https://github.com/ljmerza/hass-email-sensor/commits/master
[license-shield]: https://img.shields.io/github/license/ljmerza/hass-email-sensor.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Leonardo%20Merza%20%40ljmerza-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ljmerza/hass-email-sensor.svg?style=for-the-badge
[releases]: https://github.com/ljmerza/hass-email-sensor/releases
