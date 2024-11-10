import pandas as pd
from project import User

items = {'office' : {"name" : 'office',"category" : '+income',"value" : 300,"freq_input" : 'day','freq_alias' : 'D'},
                  'home' : {"name" : 'home',"category" : '-expenses',"value" : 900,"freq_input" : 'week','freq_alias' : 'W'},
        }

df = pd.DataFrame(columns = items, index = pd.date_range('2022-01-01','2022-02-31'))

for i in items:
    item_df = pd.DataFrame(data=items[i]['value'],columns=[items[i]['name']],
                           index = pd.date_range('2022-01-01','2023-01-31',freq = items[i]['freq_alias']))
    df = df.combine_first(item_df)


user = pd.read_json('Zbudget.json')
user['total'] = user.sum(axis=1,numeric_only=True)