import xml.etree.ElementTree as ET
import time
import requests


class BaseAPIConnector(object):
    def __init__(self, user_agent='', verbose=False):

        self.user_agent = user_agent
        self.verbose = verbose

    def construct_url(self):
        return ''

    def html_request(self):
        if self.user_agent == '':
            raise UserWarning('Please specify a user agent.')
        user_agent = 'CommonAPILibrary, made by https://github.com/Depre; Custom User-Agent: %s' % self.user_agent

        url = self.construct_url()
        if self.verbose:
            print(url)

        request = self.get_request_from_url(url=url, user_agent=user_agent)

        return request

    def get_xml_from_request(self):
        try:
            return ET.fromstring(self.html_request().text)
        except:
            return None

    def get_json_from_request(self):
        return self.html_request().json()

    @staticmethod
    def get_request_from_url(url='', user_agent=''):
        request = None
        exception_count = 0
        while exception_count < 10:
            try:
                request = requests.get(url, headers={'User-Agent': user_agent})
            except Exception as e:
                print("Exception '%s' while querying url: '%s', trying again..." % (e, url))
                time.sleep(10)
                exception_count += 1
            else:
                if request.status_code >= 400:
                    print("HTTP-code: %s, Reason: %s" % (request.status_code, request.reason))
                    time.sleep(10)
                    exception_count += 1
                else:
                    break

        return request