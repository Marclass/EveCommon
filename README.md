# EveCommonLibrary #

# Notes #

This was originally posted on github by Depre, however that repo has since been deleted. Since it was released under the MIT License and because 
EveIntel requires it, I am reuploading it. This is the state of the repo as of aprox 2/5/2015. I do not plan on maintaining it barring a change in 
the api for https://zkillboard.com 

-Marclass

## Requirements ##

* Python 2.7
* Python [Requests](http://docs.python-requests.org/en/latest/) library
* Eve Online SDE as SQLite Database (you can get it from [Fuzzwork](https://www.fuzzwork.co.uk/))

## Usage ##

There are four easy to use modules available.
Please include a user agent when requesting data from any service.

### SDEConnector ###

The SDEConnector is a wrapper to extract data out of the Eve Online SDE.
It can easily be expanded to include more complex queries.
```
from EveCommon.SDEConnector import SDEConnector

sde = SDEConnector(db_name='C:\Database\sqlite-latest.sqlite')
types = sde.get_types_with_market_group()
print('There are %d Items on the market.' % len(types))
```

### ZKillboard ###

The ZKillboard class extracts Killmails form [ZKillboard](https://zkillboard.com/) using the provided [API](https://neweden-dev.com/ZKillboard_API). 

```
from EveCommon.ZKillboard import ZKillboard
from datetime import datetime, timedelta

end_time = datetime.now()
start_time = end_time - timedelta(days=3)

zKill = ZKillboard(user_agent='Your USERAGENT', alliance_id=99003214, losses=True, no_attackers=True,
                   start_time=start_time, end_time=end_time, solar_system_id=30000142)
killmails = zKill.get_killmails()
print('The Brave Collective had %d losses in Jita during the last three days' % len(killmails))
```

### EveCentral ###

The EveCentral class extracts prices from [Eve-Central](https://eve-central.com/) using the provided [API](https://eve-central.com/home/develop.html).

```
from EveCommon.EveCentral import EveCentral

ec = EveCentral(user_agent='Your USERAGENT', type_id=34, system_id=30000142)
price = ec.get_prices_list()
print('The lowest price for Tritanium in Jita is %s ISK.' % price[0].sell.minimum)
```

### Combining all Eve classes ###

A simple example on how to combine all three Classes can be found in `example.py`

### GuildWars2 ###

The GuildWars2 Class gets Data from the official Guild Wars 2 [API](http://wiki.guildwars2.com/wiki/API).

```
from EveCommon.GuildWars2 import GuildWars2

items = GuildWars2.get_request_from_url('https://api.guildwars2.com/v1/items.json').json()
items = items['items']

gw2 = GuildWars2(user_agent='Your USERAGENT', id_list=items, api='items')

item_detail_list = gw2.get_api_response_list()

for item_details in item_detail_list:
    print(item_details.id, item_details.name)

```