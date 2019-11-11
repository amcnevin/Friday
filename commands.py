import trains as trains

default_response = "Not sure what you mean {}, try 'get command list'"


def get_command_list(slack_client, channel, caller, command_list):

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=command_list or default_response.format(caller)
    )


def get_cta_status(slack_client, channel, caller):
    train_status = trains.CTAStatus()
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="" or default_response.format(caller),
        blocks=train_status.get_route_status()
    )


def get_bus_status(slack_client, channel, caller):
    bus_status = trains.CTAStatus()
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text="" or default_response.format(caller),
        blocks=bus_status.get_bus_status()
    )

