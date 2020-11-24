import  requests
from bs4 import  BeautifulSoup
import json


class CovidStatistics:
    response = None
    url = "https://covid-193.p.rapidapi.com/statistics"
    headers = {
        'x-rapidapi-key': "ee4b03408emsh90b4fd12ab758e3p1374afjsnd06e99773d3b",
        'x-rapidapi-host': "covid-193.p.rapidapi.com"
    }

    poland_statistics = {
        'country' : None,
        'new_cases': None,
        '1M_pop': None,
        '1M_tests_pop': None,
        'date': None
    }

    def get_statistics(self):

        response = requests.request("GET", self.url, headers=self.headers)
        site_json = json.loads(response.text)
        for country in site_json['response']:
            if country['country'] == 'Poland':
                self.poland_statistics['country'] = country['country']
                self.poland_statistics['new_cases'] = country['cases']['new']
                self.poland_statistics['1M_pop'] = country['cases']['1M_pop']
                self.poland_statistics['1M_tests_pop'] = country['tests']['1M_pop']
                self.poland_statistics['date'] = country['day']

        return self.poland_statistics

    def get_country_stats(self, country_name):
        response = requests.request("GET", self.url, headers=self.headers)
        site_json = json.loads(response.text)
        for country in site_json['response']:
            if country['country'] == country_name:
                return country

    def get_highiest_cases_count(self):
        active_cases = 0
        found_country = None
        response = requests.request("GET", self.url, headers=self.headers)
        site_json = json.loads(response.text)
        for country in site_json['response']:
            if country['cases']['active'] < active_cases:
                continue
            if country['population'] is None:
                continue
            else:
                active_cases = country['cases']['active']
                found_country = country

        return [found_country, active_cases]
