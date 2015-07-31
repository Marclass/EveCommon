from BaseAPIConnector import BaseAPIConnector


class ZKillboard(BaseAPIConnector):

    def __init__(self, user_agent='', character_id=0, corporation_id=0, alliance_id=0, faction_id=0, ship_type_id=0,
                 group_id=0, solar_system_id=0, losses=False, kills=False, wspace=False, solo=False,
                 order_asc=False, limit=0, page=0, start_time=None, end_time=None,
                 year=0, month=0, week=0, before_kill_id=0, after_kill_id=0, no_items=False, no_attackers=False,
                 max_killmails=0, verbose=False):
        BaseAPIConnector.__init__(self, user_agent, verbose)

        self.character_id = character_id
        self.corporation_id = corporation_id
        self.alliance_id = alliance_id
        self.faction_id = faction_id

        self.ship_type_id = ship_type_id
        self.group_id = group_id
        self.solar_system_id = solar_system_id

        self.losses = losses
        self.kills = kills
        self.wspace = wspace
        self.solo = solo

        self.before_kill_id = before_kill_id
        self.after_kill_id = after_kill_id

        self.order_asc = order_asc
        self.no_items = no_items
        self.no_attackers = no_attackers

        self.limit = limit
        self.page = page

        self.start_time = start_time
        self.end_time = end_time

        self.year = year
        self.month = month
        self.week = week

        self.max_killmails = max_killmails

        self.killmails = []

    def construct_url(self):
        # Documentation: https://neweden-dev.com/ZKillboard_API
        url_parts = ['https://zkillboard.com/api']

        if self.character_id != 0:
            url_parts.append('characterID/%s' % self.character_id)

        if self.corporation_id != 0:
            url_parts.append('corporationID/%s' % self.corporation_id)

        if self.alliance_id != 0:
            url_parts.append('allianceID/%s' % self.alliance_id)

        if self.faction_id != 0:
            url_parts.append('factionID/%s' % self.faction_id)

        if self.ship_type_id != 0:
            url_parts.append('shipTypeID/%s' % self.ship_type_id)

        if self.group_id != 0:
            url_parts.append('groupID/%s' % self.group_id)

        if self.solar_system_id != 0:
            url_parts.append('solarSystemID/%s' % self.solar_system_id)

        if (self.losses is False) and (self.kills is True):
            url_parts.append('kills')

        if (self.losses is True) and (self.kills is False):
            url_parts.append('losses')

        if self.wspace:
            url_parts.append('w-space')

        if self.solo:
            url_parts.append('solo')

        if self.order_asc is True:
            url_parts.append('orderDirection/asc')

        if self.limit != 0:
            url_parts.append('limit/%s' % self.limit)

        if self.page != 0:
            url_parts.append('page/%s' % self.page)

        if self.start_time is not None:
            url_parts.append('startTime/%s' % self.start_time.strftime("%Y%m%d%H%I"))

        if self.end_time is not None:
            url_parts.append('endTime/%s' % self.end_time.strftime("%Y%m%d%H%I"))

        if self.year != 0:
            url_parts.append('year/{:0>4}'.format(self.year))

        if (self.month != 0) and (self.year == 0):
            raise UserWarning('Must include year when setting month!')

        if self.month != 0:
            url_parts.append('month/{:0>2}'.format(self.month))

        if (self.week != 0) and (self.year == 0):
            raise UserWarning('Must include year when setting week!')

        if self.week != 0:
            url_parts.append('week/{:0>2}'.format(self.week))

        if self.before_kill_id != 0:
            url_parts.append('beforeKillID/%s' % self.before_kill_id)

        if self.after_kill_id != 0:
            url_parts.append('afterKillID/%s' % self.after_kill_id)

        if self.no_items is True:
            url_parts.append('no-items')

        if self.no_attackers is True:
            url_parts.append('no-attackers')

        return '/'.join(url_parts) + '/'

    def get_killmails(self):
        while True:
            json_response = self.get_json_from_request()

            for killmail in json_response:
                if (self.max_killmails > 0) and (len(self.killmails) >= self.max_killmails):
                    return self.killmails
                try:
                    self.killmails.append(KillMail(killmail))
                except ValueError:
                    pass

            if self.killmails:
                if self.order_asc:
                    self.after_kill_id = self.killmails[-1].killID
                else:
                    self.before_kill_id = self.killmails[-1].killID
            if len(json_response) < 200:
                break

        return self.killmails


class KillMail(object):
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__dict__[key] = KillMail(value)