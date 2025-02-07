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
 t      target:
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
