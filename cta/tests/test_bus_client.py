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


def test_get_vehicles_rt():
    response = bus_client.get_vehicles(rt=80)
    assert response is not None
    assert response.status_code == 200
    output = json.loads(response.text)
    assert output["bustime-response"]["vehicle"] is not None


def test_get_vehicles_vid():
    response1 = bus_client.get_vehicles(rt=80)
    output1 = json.loads(response1.text)
    vehicle = output1["bustime-response"]["vehicle"][0]
    vid = vehicle["vid"]

    response2 = bus_client.get_vehicles(vid=vid)
    assert response2 is not None
    assert response2.status_code == 200
    output2 = json.loads(response2.text)
    assert output2["bustime-response"]["vehicle"] is not None


def test_get_directions():
    response = bus_client.get_directions(rt=80)
    assert response is not None
    assert response.status_code == 200
    output = json.loads(response.text)
    assert 2 == len(output["bustime-response"]["directions"])


def test_get_stops_eastbound():
    response = bus_client.get_stops(rt=80, dir="Eastbound")
    assert response is not None
    assert response.status_code == 200
    output = json.loads(response.text)
    assert 87 == len(output["bustime-response"]["stops"])


def test_get_stops_westbound():
    response = bus_client.get_stops(rt=80, dir="Westbound")
    assert response is not None
    assert response.status_code == 200
    output = json.loads(response.text)
    assert 80 == len(output["bustime-response"]["stops"])


def test_get_patterns_rt():
    response = bus_client.get_patterns(rt=80)
    assert response is not None
    assert response.status_code == 200
    output = json.loads(response.text)
    assert 0 < len(output["bustime-response"]["ptr"])


def test_get_patterns_pid():
    response1 = bus_client.get_patterns(rt=80)
    output1 = json.loads(response1.text)
    pid = output1["bustime-response"]["ptr"][0]["pid"]
    assert pid is not None

    response = bus_client.get_patterns(pid=pid)
    assert response is not None
    assert response.status_code == 200
    output = json.loads(response.text)
    assert output is not None
    assert output["bustime-response"]["ptr"][0]["pid"] == pid


def test_get_predictions_rt():
    pass


def test_get_predictions_stpid():
    pass


def test_get_predictions_vid():
    pass


def test_service_bulletins_rt():
    pass


def test_service_bulletins_stpid():
    pass

