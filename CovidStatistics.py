import  requests
from bs4 import  BeautifulSoup
import json


class CovidStatistics:
    
    response = None
    poland_statistics = {
        'country' : None,
        'new_cases': None,
        '1M_pop': None,
        '1M_tests_pop': None,
        'date': None
    }

    def get_response(self):
        url = "https://covid-193.p.rapidapi.com/statistics"

        headers = {
            'x-rapidapi-key': "ee4b03408emsh90b4fd12ab758e3p1374afjsnd06e99773d3b",
            'x-rapidapi-host': "covid-193.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        site_json = json.loads(response.text)
        for country in site_json['response']:
            if country['country'] == 'Poland':
                self.poland_statistics['country'] = country['country']
                self.poland_statistics['new_cases'] = country['cases']['new']
                self.poland_statistics['1M_pop'] = country['cases']['1M_pop']
                self.poland_statistics['1M_tests_pop'] = country['tests']['1M_pop']
                self.poland_statistics['date'] = country['day']

    def get_statistics(self):
        return self.poland_statistics