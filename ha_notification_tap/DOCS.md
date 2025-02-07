# HA Notification Tap

This add-on handles deep links from Home Assistant notification click actions and fires events on the event bus.

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

## Usage Example

1. Configure an automation to listen for the event:

```yaml
automation:
  trigger:
    platform: event
    event_type: notification_tap
    event_data:
      action_id: turn_on_lights
      room: living_room
  action:
    - service: scene.turn_on
      target:
        entity_id: scene.living_room_evening
```

2. Create a notification:

```yaml
service: notify.mobile_app_phone
data:
  message: "Tap to turn on lights"
  data:
    clickAction: "{% raw %}{{ 'deep-link-to-ha-notify-tap-addon/turn_on_lights' }}{% endraw %}"
```

When the notification is tapped:
1. The add-on receives the action ID ("turn_on_lights")
2. It looks up the configured data for that action
3. It fires an event with both the configured data and the action_id
4. Your automation can then handle the event

## Usage Examples

### Method 1: Using GET
```yaml
variables:
  deep_link: "http://192.168.86.124:8099/api/notify-tap/test_data"
```

### Method 2: Using POST (Recommended)
```bash
# Using curl
curl -X POST \
  http://192.168.86.124:8099/api/notify-tap \
  -H "Content-Type: application/json" \
  -d '{"data": "test_data"}'
```

```yaml
# In Home Assistant notification
service: notify.mobile_app_josh
data:
  message: Test Click
  data:
    url: "http://192.168.86.124:8099/api/notify-tap"  # POST endpoint
    method: "POST"
    headers:
      Content-Type: "application/json"
    payload: '{"data": "test_data"}'
```

## Notification Examples

### Using URL-encoded POST data:
```yaml
variables:
  # Encode the POST data in the URL
  deep_link: "http://192.168.86.124:8099/api/notify-tap?data=test_data&action=turn_on_lights"

data:
  message: Test Click
  data:
    clickAction: "{{ deep_link }}"
action: notify.mobile_app_josh
```

### Example URLs:
✅ `http://192.168.86.124:8099/api/notify-tap?data=test_data`
✅ `http://192.168.86.124:8099/api/notify-tap?data=turn_on_lights&room=living_room`

## Notification Example

```yaml
# In automations.yaml or scripts.yaml
service: notify.mobile_app_josh
data:
  message: "Test Click"
  data:
    # This opens directly in browser instead of HA app
    url: "http://192.168.86.124:8099/api/notify-tap/test_data"
```

### Alternative Methods

If the direct URL doesn't work, try:
```yaml
service: notify.mobile_app_josh
data:
  message: "Test Click"
  title: "Test Notification"
  data:
    actions:
      - action: "tap_action"
        title: "Tap Me"
        uri: "http://192.168.86.124:8099/api/notify-tap/test_data"
```

### Testing the Event

You can test if events are being fired using curl:
```bash
curl "http://192.168.86.124:8099/api/notify-tap/test_data"
```

Then check your Home Assistant logs for the `notification_tap_event`.
