from BaseAPIConnector import BaseAPIConnector


class GuildWars2(BaseAPIConnector):
    def __init__(self, user_agent='', verbose=False, api='', api_version=2, item_id=0, id_list=None):
        BaseAPIConnector.__init__(self, user_agent, verbose)

        self.id = item_id
        self.id_list = id_list

        self.api = api
        self.api_version = api_version

        if self.id_list is not None:
            self.internal_id_list = list(self.id_list)
        else:
            self.internal_id_list = None

        self.items = []

    def construct_url(self):
        # documentation: http://wiki.guildwars2.com/wiki/API
        if self.api == '':
            raise UserWarning('Must include API endpoint!')

        base_url = 'https://api.guildwars2.com/v%s/%s' % (self.api_version, self.api)
        url_parts = []

        if self.id != 0:
            url_parts.append('/' + str(self.id))
        elif self.internal_id_list is not None:
            base_url += '?ids='
            for i in range(0, len(self.internal_id_list)):
                item_id = self.internal_id_list[0]
                url_parts.append(str(item_id))
                self.internal_id_list.pop(0)
                if i >= 100:
                    break

        return base_url + ','.join(url_parts)

    def get_api_response_list(self):
        while True:
            if self.internal_id_list and self.verbose:
                print('Getting Items starting at %s' % str(self.internal_id_list[0]))

            json_response = self.get_json_from_request()

            if self.internal_id_list is not None:
                for item in json_response:
                    try:
                        self.items.append(GW2Response(item))
                    except ValueError:
                        pass
            else:
                self.items.append(GW2Response(json_response))

            if len(self.internal_id_list) == 0:
                break

        return self.items


class GW2Response(object):
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__dict__[key] = GW2Response(value)