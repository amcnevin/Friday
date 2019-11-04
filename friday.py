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
            response = train_status.getStatus()

        # add more commands

        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or self.default_response.format(caller)
        )

    def bot_it_up(self):
        while True:
            command, channel, caller = self.parse_event(self.slack_client.rtm_read())
            if command:
                self.handle_command(command, channel, caller)
            time.sleep(self.RTM_READ_DELAY)


if __name__ == "__main__":
    friday = Friday()
    print("Friday Online")
    friday.bot_it_up()
    print("Friday powering down...")

