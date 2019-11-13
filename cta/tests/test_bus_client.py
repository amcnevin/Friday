import os
from cta import cta_clients
import json

CTA_BUS_API_KEY = os.environ.get('CTA_BUS_API_KEY')

bus_client = cta_clients.CTABusClient(CTA_BUS_API_KEY)


def test_get_time():
    response = bus_client.get_time()
    assert response is not None
    assert response.status_code == 200
    output = json.loads(response.text)
    assert output["bustime-response"]["tm"] is not None


def test_get_routes():
    response = bus_client.get_routes()
    assert response is not None
    assert response.status_code == 200
    output = json.loads(response.text)
    assert 124 == len(output["bustime-response"]["routes"])
