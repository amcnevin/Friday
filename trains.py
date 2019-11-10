import sys
import requests
import xml.etree.ElementTree as elementTree
import json

class TrainStatus:

    CTA_STATUS_URL = "http://lapi.transitchicago.com/api/1.0/routes.aspx"
    LINES = ('Red Line', 'Brown Line', 'Purple Line', 'Irving Park', )

    def __init__(self):
        pass

    # get the statuses from the CTA API
    def get_status(self):
        """
        get Statuses of trains
        :return: list of statuses
        """
        statuses = []
        try:
            response = requests.get(self.CTA_STATUS_URL)
            root = elementTree.fromstring(response.text)
            for route in root.findall('RouteInfo'):
                route_text = route.find('Route').text
                if route_text in self.LINES:
                    status = route.find('RouteStatus').text
                    statuses.append((route_text, status,))
        except:
            print("Could not get trains due to {}".format(sys.exc_info()[0]))

        return self.decorate_status(statuses)

    @staticmethod
    def decorate_status(statuses):
        sections = []

        top_level = dict()
        top_level["type"] = "section"
        top_level["text"] = {}
        top_level["text"]["type"] = "mrkdwn"
        top_level["text"]["text"] = "Here are the CTA Statuses"

        divider = dict()
        divider["type"] = "divider"

        sections.append(top_level)
        sections.append(divider)

        for status in statuses:
            section = dict()
            section["type"] = "section"
            section["text"] = {}
            section["text"]["type"] = "mrkdwn"
            section["text"]["text"] = '*{}* - {}'.format(status[0], status[1])
            sections.append(section)
        print(json.dumps(sections))
        return json.dumps(sections)
