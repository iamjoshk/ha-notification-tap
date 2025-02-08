# HA Notification Tap

Unlike action buttons and swiping away a notification, there is no event that is fired when you tap the notification. All it does is take you to the mobile companion app OR nothing at all (if you use `clickAction: noAction`). This add-on works around that and utilizes the `clickAction` from the Android mobile app notifications to fire an event called `notification_tap_event` from which you can trigger automations using an event trigger. This means you don't need to expand the notification to expose the action buttons and instead can just tap the notification to fire the event.

The event data is configurable so you can have triggers for any notification.

The add-on uses a `clickAction` URL to send an HTTP POST API call which then fires the event. The end point is `http://<your-ha-hostname or IP>:8099/api/notify-tap/<your event_data>`.

`event_data` can be defined by a variable in your script or automation prior to the notification action. This will define the data in the `notification_tap_event` that you can use as an event trigger.

## Installation
I wouldn't install this if I were you.
But if you are so inclined, copy the URL for the repo (https://github.com/iamjoshk/ha-notification-tap) and go to Add Ons, then go to Add On Store, then click the 3 dots in the upper right corner, then Repositories, then paste the URL in the box and click Add. It should add the repo. You might need to refresh the browser, restart Home Assistant, spin around three times, and refresh the browser again before it shows up in the Add On Store after adding the repo. It's weird sometimes. When it's there, click the Add On and then install. But again, I wouldn't install this.

## Configuration

+ After installing the add-on you need to create a long-lived access token.
  + In Home Assistant, navigate to your profile, then select the Security tab, then scroll down to Long-lived Access Tokens.
  + Click Create Token
  + Give the token a name and click OK
  + COPY the token and paste it somewhere safe. You'll need it later and if you lose it, you will need to do this again.

  From this point, you can choose to put the token directly in the `ha_token` field under the add-on's Configuration screen. Or (and the better option) is to [use `secrets.yaml`](https://www.home-assistant.io/docs/configuration/secrets/) and add your token there. Then in the configuration `ha_token` field, you would enter `!secret <your_token_name>` 

  In `ha_host` add the hostname of your Home Assistant. Some people use custom names instead of homeassistant.

  You can choose to enable or disable the debug logger.

Under `Network` you can change the exposed port. 

Saving either `Options` or `Network` will require the add-on to restart if it is running. Sometimes browsers can cache the settings and it might look like they haven't updated after saving. Try refreshing the page.


## Notification Format

Once you've got the add-on configured, it's time to set up a notification. The example below is using a script for the notification. Once you've created your first notification, you can test it by clicking the three dots and clicking Run Action.

```
sequence:
  - variables:
      event_data: THIS_EVENT
    enabled: true
  - data:
      message: Test Click
      data:
        clickAction: http://homeassistant:8099/api/notify-tap/{{ event_data }}
    action: notify.mobile_app_your_device
alias: example clickAction
```

+ Additional options, like action buttons, are still available to use in your notification: https://companion.home-assistant.io/docs/notifications/notifications-basic#general-options


## IMPORTANT NOTE
The nature of an HTTP POST API call is that it wants to send you a response. This add-on tries to work around that by redirecting you to the companion app, instead of the web browser where you would (hopefully) get the `OK` response from your API call. Most major mobile web browsers will allow an app to open a link. Some mobile browsers (like Edge and Chrome) will ask if you want to allow the companion app to open the link, ask if you want to do it all the time, and then still ask you to confirm every time after that. I haven't found a way around that extra confirmation step. Currently (as of Feb 7 2025) Mobile Firefox asks the first time, and then you can adjust the settings to automatically open the companion app in the future.

This is not an ideal solution, but it essentially replicates the typical `clickAction` behavior of opening the companion app by tapping on the notification.

The event is fired regardless of whether you complete the redirect to the companion app or not.


# DISCLAIMER
I wouldn't use this add-on if I were you. I don't really know what I'm doing, but I know enough to break things. This will likely never get out of alpha and I may get distracted and never touch it again. I don't even know if I will use it myself, it was just a challenge that I felt inclined to attack. It would probably have been easier to open Pull Requests for changes in the mobile app and notifications to fire an action on `clickAction` than create this add-on, but...
Anyway, I wouldn't use this. Consider yourself warned. I am not responsible for any damage to your Home Assistant.
