import os
import re
import sys
from abc import abstractmethod
from slackclient import SlackClient


class BaseBot:

    RTM_READ_DELAY = 1
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    def __init__(self):
        self.connect_client()

    @abstractmethod
    def get_bot_id(self):
        pass

    @abstractmethod
    def handle_command(self, command, channel, caller):
        pass

    def connect_client(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Connected")
        else:
            print("Failed to connect")

    def parse_event(self, slack_events):
        """
        Parses the slack events to determine if bot needs to respond
        :param slack_events:
        :return: message, channel, caller
        """
        for event in slack_events:
            if event["type"] == "goodbye":
                print("Server is saying goodbye, trying to reconnect")
                self.connect_client()
            if event["type"] == "hello":
                print("Hello from Server")
            if event["type"] == "message" and "subtype" not in event:
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.get_bot_id():
                    return message, event["channel"], self.parse_caller(event)
        return None, None, None

    def parse_direct_mention(self, message_text):
        """
        determine if there's a direct mention
        TODO improve REGEX so it's not required at beginning of message
        :param message_text:
        :return: bot_id, message
        """
        matches = re.search(self.MENTION_REGEX, message_text)
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def parse_caller(self, event):
        """
        find the caller of the message
        :param event:
        :return: user name
        """
        caller_id = event['user']
        caller = None
        try:
            response = (self.slack_client.api_call("users.info", user=caller_id))
            caller = response["user"]['name']
        except:
            print("Could not get name due to {}".format(sys.exc_info()[0]))
        return caller
