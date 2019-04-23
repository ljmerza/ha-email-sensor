# USPS MQTT Tracking Numbers


## Description

This flow parses out tracking numbers from USPS emails and sends them back to Home Assistant via MQTT. Add the flow to Node-RED and add the MQTT sensor in Home assistant:

```yaml
sensor:
    - platform: mqtt
        name: Email
        state_topic: "email"
        value_template: '{{ value_json.count }}'
        json_attributes_topic: "email"
```
