# HA Notification Tap

Fires events on Home Assistant's event bus from notification taps.

## Configuration

Example configuration:

```yaml
event_type: notification_tap
actions:
  turn_on_lights:
    room: living_room
    scene: evening
  movie_mode:
    room: living_room
    scene: movie
```

### Options

- `event_type`: The type of event to fire on the event bus
- `actions`: A dictionary of action IDs and their associated event data
- `debug`: Enable debug logging (default: false)

## Usage Example

1. Create a notification with a deep link:
```yaml
variables:
  deep_link: "deep-link://192.168.1.123:8099/api/notify-tap/"  # Replace IP with your HA IP
  event_data: "turn_on_lights"

service: notify.mobile_app_phone
data:
  message: "Tap to trigger action"
  data:
    clickAction: "{{ deep_link }}{{ event_data }}"
```

2. Create an automation that listens for the event:
```yaml
automation:
  trigger:
    platform: event
    event_type: notification_tap_event
    event_data:
      data: turn_on_lights  # Match the string from your deep link
  action:
    service: light.turn_on
    target:
      entity_id: light.living_room
```

## Deep Link Format

The deep link format is:
```
notify-tap/YOUR_DATA_HERE
```

This will fire a `notification_tap_event` with:
```json
{
  "data": "YOUR_DATA_HERE"
}
```
