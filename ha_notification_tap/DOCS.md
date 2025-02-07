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
