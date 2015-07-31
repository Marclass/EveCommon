from BaseAPIConnector import BaseAPIConnector


class EveCentral(BaseAPIConnector):
    def __init__(self, user_agent='', type_id=0, type_id_list=None, system_id=0, region_id=0, hours=0, min_quantity=0):
        BaseAPIConnector.__init__(self, user_agent)

        self.type_id = type_id
        self.type_id_list = type_id_list
        self.internal_type_id_list = None
        if self.type_id_list is not None:
            self.internal_type_id_list = list(self.type_id_list)
        self.system_id = system_id
        self.region_id = region_id
        self.hours = hours
        self.min_quantity = min_quantity

        self.items = []

    def construct_url(self):
        base_url = 'http://api.eve-central.com/api/marketstat?'
        url_parts = []

        if self.type_id != 0:
            url_parts.append('typeid=%s' % self.type_id)

        if self.internal_type_id_list is not None:
            for i in range(0, len(self.internal_type_id_list)):
                type_id = self.internal_type_id_list[0]
                url_parts.append('typeid=%s' % type_id)
                self.internal_type_id_list.pop(0)
                if i >= 100:
                    break

        if self.system_id != 0:
            url_parts.append('usesystem=%s' % self.system_id)

        if self.region_id != 0:
            url_parts.append('regionlimit=%s' % self.region_id)

        if self.hours != 0:
            url_parts.append('hours=%s' % self.hours)

        if self.min_quantity != 0:
            url_parts.append('minQ=%s' % self.min_quantity)

        return base_url + '&'.join(url_parts)

    def get_prices_list(self):
        def _get_item_prices(item_node):
            return EveItemPrices(volume=item_node.find('volume').text,
                                 average=item_node.find('avg').text,
                                 maximum=item_node.find('max').text,
                                 minimum=item_node.find('min').text,
                                 standard_deviation=item_node.find('stddev').text,
                                 median=item_node.find('median').text,
                                 percentile=item_node.find('percentile').text)

        while True:
            tree = self.get_xml_from_request()

            if tree is None:
                continue

            if self.internal_type_id_list and self.verbose:
                print('Getting Items starting at %s' % str(self.internal_type_id_list[0]))

            for item_type in tree.iter('type'):
                item = EveItem(item_id=item_type.attrib.get('id'))

                item.sell = _get_item_prices(item_type.find('sell'))
                item.buy = _get_item_prices(item_type.find('buy'))
                item.all = _get_item_prices(item_type.find('all'))

                self.items.append(item)

            if (self.internal_type_id_list is None) or (self.internal_type_id_list == []):
                break

        return self.items


class EveItem(object):
    def __init__(self, item_id=0):
        self.item_id = item_id
        self.buy = None
        self.sell = None
        self.all = None


class EveItemPrices(object):
    def __init__(self, volume=0, average=0, maximum=0, minimum=0, standard_deviation=0, median=0, percentile=0):
        self.volume = volume
        self.average = average
        self.maximum = maximum
        self.minimum = minimum
        self.standard_deviation = standard_deviation
        self.median = median
        self.percentile = percentile