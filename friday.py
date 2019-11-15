from slackclient.server import SlackConnectionError

from basebot import BaseBot
import time
import trains as trains
import commands
class Friday(BaseBot):

    friday_id = None
    COMMAND_LIST = ["get command list", "get cta status", "get bus times", ]

    def __init__(self):
        super().__init__()

    def get_bot_id(self):
        if self.friday_id is None:
            self.friday_id = self.slack_client.api_call("auth.test")["user_id"]
        return self.friday_id

    def handle_command(self, command, channel, caller):
        # get command list
        if command.lower() == "get command list":
            commands.get_command_list(self.slack_client, channel, caller, self.COMMAND_LIST)

        # get cta status
        if command.lower() == "get cta status":
            commands.get_cta_status(self.slack_client, channel, caller)

        if command.lower() == "get bus times":
            commands.get_bus_status(self.slack_client, channel, caller)

        # add more commands



    def bot_it_up(self):
        while True:
            try:
                command, channel, caller = self.parse_event(self.slack_client.rtm_read())
                if command:
                    self.handle_command(command, channel, caller)
                time.sleep(self.RTM_READ_DELAY)
            except SlackConnectionError as sce:
                print("Connection Error: {}".format(sce))
                self.connect_client()
            except ConnectionResetError as cre:
                print("Connection Reset Error: {}".format(cre))
                self.connect_client()
            except Exception as ex:
                print("Generic Exception Caught: {}".format(ex))
                self.connect_client()


if __name__ == "__main__":
    friday = Friday()
    print("Friday Online")
    friday.bot_it_up()
    print("Friday powering down...")

