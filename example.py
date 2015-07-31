from EveCommon.EveCentral import EveCentral
from EveCommon.ZKillboard import ZKillboard
from EveCommon.SDEConnector import SDEConnector
from os import environ

from datetime import datetime, timedelta

end_time = datetime.now()
start_time = end_time - timedelta(days=3)
database_url = environ.get('ECL_DATABASE_URL', 'C:\Database\sqlite-latest.sqlite')
ec_useragent = environ.get('ECL_USERAGENT', 'Your USERAGENT')
target_alliance_id = int(environ.get('ECL_ALLIANCE_ID', '99003214'))
target_solar_system_id = int(environ.get('ECL_SOLAR_SYSTEM_ID', '30000142'))

sde = SDEConnector(db_name=database_url)

zKill = ZKillboard(user_agent=ec_useragent, alliance_id=target_alliance_id, losses=True, no_attackers=True,
                   start_time=start_time, end_time=end_time, solar_system_id=target_solar_system_id)
killmails = zKill.get_killmails()

items = []
for killmail in killmails:
    print('Pilot %s lost: %s' % (killmail.victim.characterName, sde.get_type_name_by_type_id(killmail.victim.shipTypeID)))
    for item in killmail.items:
        items.append(item['typeID'])

ec = EveCentral(user_agent=ec_useragent, type_id_list=items, system_id=target_solar_system_id)
prices_list = ec.get_prices_list()

for price in prices_list:
    print ('Price for %s: %s' % (sde.get_type_name_by_type_id(price.item_id), price.sell.percentile))