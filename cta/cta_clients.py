import requests


class CTABusClient:

    BASE_URL = "http://www.ctabustracker.com/bustime/api/v2/"

    cta_bus_api_key = None

    def __init__(self, api_key):

        if not api_key:
            raise ValueError("API Key cannot be None")

        self.cta_bus_api_key = api_key

    def _get_base_params(self):
        params = dict()
        params["key"] = self.cta_bus_api_key
        params["format"] = "json"
        return params

    def get_time(self):
        url = self.BASE_URL + "gettime"
        params = self._get_base_params()
        return requests.get(url, params)

    def get_vehicles(self, vid=None, rt=None, tmres=None):
        url = self.BASE_URL + "getvehicles"
        params = self._get_base_params()
        # TODO enforce conditional args
        params["vid"] = vid
        params["rt"] = rt
        params["tmres"] = tmres
        return requests.get(url, params)

    def get_routes(self):
        url = self.BASE_URL + "getroutes"
        params = self._get_base_params()
        return requests.get(url, params)

    def get_directions(self, rt):
        url = self.BASE_URL + "getdirections"
        params = self._get_base_params()
        params["rt"] = rt
        return requests.get(url, params)

    def get_stops(self, rt, dir):
        url = self.BASE_URL + "getstops"
        params = self._get_base_params()
        params["rt"] = rt
        params["dir"] = dir
        return requests.get(url, params)

    def get_patterns(self, pid=None, rt=None):
        url = self.BASE_URL + "getpatterns"
        params = self._get_base_params()
        # TODO enforce conditional args
        params["pid"] = pid
        params["rt"] = rt
        return requests.get(url, params)

    def get_predictions(self, stpid=None, rt=None, vid=None, top=None):
        url = self.BASE_URL + "getpredictions"
        params = self._get_base_params()
        # TODO enforce conditional args
        params["stpid"] = stpid
        params["rt"] = rt
        params["vid"] = vid
        params["top"] = top
        return requests.get(url, params)

    def get_service_bulletins(self, rt=None, rtdir=None, stpid=None):
        url = self.BASE_URL + "getservicebulletins"
        params = self._get_base_params()
        # TODO enforce conditional args
        params["rt"] = rt
        params["rtdir"] = rtdir
        params["stpid"] = stpid
        return requests.get(url, params)


class CTATrainClient:
    BASE_URL = "http://lapi.transitchicago.com/api/1.0/"

    cta_train_api_key = None

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key cannot be None")

        self.cta_train_api_key = api_key

    def _get_base_params(self):
        params = dict()
        params["key"] = self.cta_train_api_key
        params["outputType"] = "JSON"
        return params

    def get_arrivals(self, mapid=None, stpid=None, max=None, rt=None):
        url = self.BASE_URL + "ttarrivals.aspx"
        params = self._get_base_params()
        # TODO enforce conditional args
        params["mapid"] = mapid
        params["stpid"] = stpid
        params["max"] = max
        params["rt"] = rt
        return requests.get(url, params)

    def get_follow_train(self, runnumber):
        url = self.BASE_URL + "ttfollow.aspx"
        params = self._get_base_params()
        params["runnumber"] = runnumber
        return requests.get(url, params)

    def get_locations(self, rt):
        url = self.BASE_URL + "ttpositions.aspx"
        params = self._get_base_params()
        params["rt"] = rt
        return requests.get(url, params)
