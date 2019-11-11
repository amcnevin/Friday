import os
import sys
import requests
import xml.etree.ElementTree as elementTree
import json


class CTAStatus:

    CTA_STATUS_URL = "http://lapi.transitchicago.com/api/1.0/routes.aspx"
    LINES = ('Red Line', 'Brown Line', 'Purple Line', 'Irving Park', )

    SOUTHPORT_STOP = 5667
    IRVING_ROUTE = 80

    CTA_BUS_API_KEY = os.environ.get('CTA_BUS_API_KEY')

    CTA_BUS_URL = "http://www.ctabustracker.com/bustime/api/v2/getpredictions?key={}&rt={}&stpid={}"

    def __init__(self):
        pass

    # get the statuses from the CTA API
    def get_route_status(self):
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
        except Exception as ex:
            print("Could not get trains: {}".format(ex.message))

        return self.decorate_status(statuses)

    def get_bus_status(self):
        predictions = []
        try:
            response = requests.get(self.CTA_BUS_URL.format(self.CTA_BUS_API_KEY, self.IRVING_ROUTE, self.SOUTHPORT_STOP))
            root = elementTree.fromstring(response.text)
            for prediction in root.findall('prd'):
                stop_name = prediction.find("stpnm").text
                direction = prediction.find("rtdir").text
                prdtm = prediction.find("prdtm").text
                delay = prediction.find("dly").text
                predictions.append((stop_name, direction, prdtm, delay,))

        except Exception as ex:
            print("Could not get bus predictions: {}".format(ex.message))

        return self.decorate_bus_predictions(predictions)

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

    @staticmethod
    def decorate_bus_predictions(predictions):
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
        for prediction in predictions:
            section = dict()
            section["type"] = "section"
            section["text"] = {}
            section["text"]["type"] = "mrkdwn"
            section["text"]["text"] = '*{}* - {} at {}: is delayed? {}'.format(prediction[0], prediction[1], prediction[2], prediction[3])
            sections.append(section)
        print(json.dumps(sections))
        return json.dumps(sections)