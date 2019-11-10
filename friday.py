from slackclient.server import SlackConnectionError

from basebot import BaseBot
import time
import trains as trains

class Friday(BaseBot):

    friday_id = None
    COMMAND_LIST = ["get command list", "get cta status", ]
    default_response = "Not sure what you mean {}, try 'get command list'"

    def __init__(self):
        super().__init__()

    def get_bot_id(self):
        if self.friday_id is None:
            self.friday_id = self.slack_client.api_call("auth.test")["user_id"]
        return self.friday_id

    def handle_command(self, command, channel, caller):
        response = None
        # get command list
        if command.lower() == "get command list":
            response = self.COMMAND_LIST

        # get cta status
        if command.lower() == "get cta status":
            train_status = trains.TrainStatus()
            response = train_status.get_status()

        # add more commands

        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text="" or self.default_response.format(caller),
            blocks=response
        )

    def bot_it_up(self):
        while True:
            try:
                command, channel, caller = self.parse_event(self.slack_client.rtm_read())
                if command:
                    self.handle_command(command, channel, caller)
                time.sleep(self.RTM_READ_DELAY)
            except SlackConnectionError as sce:
                print("Connection Error: {}".format(sce.message))
                self.connect_client()
            except ConnectionResetError as cre:
                print("Connection Reset Error: {}".format(cre.message))
                self.connect_client()
            except Exception as ex:
                print("Generic Exception Caught: {}".format(ex.message))
                self.connect_client()



if __name__ == "__main__":
    friday = Friday()
    print("Friday Online")
    friday.bot_it_up()
    print("Friday powering down...")

