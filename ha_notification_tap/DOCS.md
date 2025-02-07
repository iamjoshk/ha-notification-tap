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
  # The deep link must use homeassistant:// scheme
  deep_link: "homeassistant://192.168.86.124:8099/api/notify-tap/"
  event_data: "test_data"

data:
  message: Test Click
  data:
    clickAction: "{{ deep_link }}{{ event_data }}"
action: notify.mobile_app_josh
```

The full URL will be: `homeassistant://192.168.86.124:8099/api/notify-tap/test_data`

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

## Usage Examples

### For Android Using HTTP Request Shortcuts:
```yaml
# Method 1: Direct URL
variables:
  deep_link: "http://192.168.86.124:8099/api/notify-tap/"
  event_data: "test_data"

# Method 2: Using http:// scheme (alternative)
variables:
  deep_link: "http://192.168.86.124:8099/api/notify-tap/"
  event_data: "test_data"

data:
  message: Test Click
  data:
    clickAction: "{{ deep_link }}{{ event_data }}"
action: notify.mobile_app_josh
```

### For iOS or Home Assistant App:
```yaml
variables:
  deep_link: "homeassistant://navigate/192.168.86.124:8099/api/notify-tap/"
  event_data: "test_data"

data:
  message: Test Click
  data:
    clickAction: "{{ deep_link }}{{ event_data }}"
action: notify.mobile_app_josh
```

## Note on URL Schemes
- Use `http://` for direct web requests (Android)
- Use `homeassistant://` for Home Assistant app navigation
- The add-on listens on standard HTTP, so direct HTTP calls will work
