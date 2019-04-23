# UPS MQTT Tracking Numbers


## Description

This flow parses out tracking numbers from UPS emails and sends them back to Home Assistant via MQTT. You'll need `node-red-contrib-home-assistant-websocket` and `mqtt` setup in Node-RED along with a MQTT broker setup in Home Assistant. Add the flow to Node-RED and add the MQTT sensor in Home Assistant:

```yaml
sensor:
    - platform: mqtt
        name: UPS
        state_topic: "ups"
        value_template: '{{ value_json.count }}'
        json_attributes_topic: "email"
```
