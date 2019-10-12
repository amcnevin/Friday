import os
import time
import re
import sys
import trains as trains
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

friday_id = None

RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
COMMAND_LIST = ["get command list", "get cta status", ]


def parse_event(slack_events):
    """
    Parses the slack events to determine if bot needs to respond
    :param slack_events:
    :return: message, channel, caller
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == friday_id:
                caller = parse_caller(event)
                return message, event["channel"], caller
    return None, None, None


def parse_direct_mention(message_text):
    """
    determine if there's a direct mention
    TODO improve REGEX so it's not required at beginning of message
    :param message_text:
    :return: bot_id, message
    """
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def parse_caller(event):
    """
    find the caller of the message
    :param event:
    :return: user name
    """
    caller_id = event['user']
    caller = None
    try:
        response = (slack_client.api_call("users.info", user=caller_id))
        caller = response["user"]['name']
    except:
        print("Could not get name due to {}".format(sys.exc_info()[0]))
    return caller


def handle_command(command, channel, caller):
    """
    handle the command and respond
    :param command: string
    :param channel: the room where it happens
    :param caller: who called it
    :return:
    """
    default_response = "Not sure what you mean {}, try 'get command list'".format(caller)
    response = None

    # get command list
    if command.lower() == "get command list":
        response = COMMAND_LIST

    # get cta status
    if command.lower() == "get cta status":
        train_status = trains.TrainStatus()
        response = train_status.getStatus()

    # add more commands

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Friday connected and running!")
        friday_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, caller = parse_event(slack_client.rtm_read())
            if command:
                handle_command(command, channel, caller)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")