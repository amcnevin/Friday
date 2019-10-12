import sys
import requests
import xml.etree.ElementTree as elementTree


class TrainStatus:

    CTA_STATUS_URL = "http://lapi.transitchicago.com/api/1.0/routes.aspx"
    LINES = ('Red Line', 'Brown Line', 'Purple Line', 'Irving Park', 'Ashland Express', )

    def __init__(self):
        pass

    # get the statuses from the CTA API
    def getStatus(self):
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

        return statuses
