# Load the Pandas libraries with alias 'pd'
from collections import defaultdict

import pandas as pd

# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
data15 = pd.read_csv("players_15.csv").sort_values(by="sofifa_id")
data16 = pd.read_csv("players_16.csv").sort_values(by="sofifa_id")
data17 = pd.read_csv("players_17.csv").sort_values(by="sofifa_id")
data18 = pd.read_csv("players_18.csv").sort_values(by="sofifa_id")
data19 = pd.read_csv("players_19.csv").sort_values(by="sofifa_id")
data20 = pd.read_csv("players_20.csv").sort_values(by="sofifa_id")
data21 = pd.read_csv("players_21.csv").sort_values(by="sofifa_id")

data15["data_year"] = 2015
data16["data_year"] = 2016
data17["data_year"] = 2017
data18["data_year"] = 2018
data19["data_year"] = 2019
data20["data_year"] = 2020
data21["data_year"] = 2021

dataList = [data21, data20, data19, data18, data17, data16, data15]
dataNames = ["data15", "data16", "data17", "data18", "data19", "data20", "data21"]


def filter_position(pandaslist):
    columnDict = {
        "LW": [],
        "ST": [],
        "RW": [],
        "CF": [],
        "LM": [],
        "CM": [],
        "RM": [],
        "CAM": [],
        "CDM": [],
        "LB": [],
        "CB": [],
        "RB": [],
        "LWB": [],
        "RWB": [],
        "GK": []
    }
    for p in pandaslist:
        category = p.split(",")
        for pos in columnDict.keys():
            if pos in category:
                temp = columnDict[pos]
                temp.append(1)

                columnDict[pos] = temp
            else:
                temp = columnDict[pos]
                temp.append(0)
                columnDict[pos] = temp
    return columnDict


cleanList = []

for d in dataList:
    dataNoDuplicate = d
    dataNoDuplicate = dataNoDuplicate.iloc[:, :80]
    dataNoDuplicate["data_year"] = d["data_year"]
    dataNoDuplicate = dataNoDuplicate.drop(columns=[
        'player_url',
        'short_name',
        'long_name',
        'dob',
        'real_face',
        'release_clause_eur',
        'player_tags',
        'loaned_from',
        'body_type',
        'nation_position',
        'nation_jersey_number',
        'gk_diving',
        'gk_handling',
        'gk_kicking',
        'gk_reflexes',
        'gk_speed',
        'gk_positioning',
        'goalkeeping_diving',
        'goalkeeping_handling',
        'goalkeeping_kicking',
        'goalkeeping_positioning',
        'goalkeeping_reflexes',
        'defending_marking',
        'player_traits',
        'joined',
        'mentality_composure',
        'pace',
        'shooting',
        'passing',
        'dribbling',
        'defending',
        'physic',
        'contract_valid_until',
        'team_jersey_number',
        # "player_positions"
    ])
    dataNoDuplicate = dataNoDuplicate.dropna(axis=0, how='any')
    dataNoDuplicate['nationality'] = dataNoDuplicate['nationality'].astype('category').cat.codes
    dataNoDuplicate['club_name'] = dataNoDuplicate['club_name'].astype('category').cat.codes
    dataNoDuplicate['league_name'] = dataNoDuplicate['league_name'].astype('category').cat.codes
    dataNoDuplicate['preferred_foot'] = dataNoDuplicate['preferred_foot'].astype('category').cat.codes
    dataNoDuplicate['team_position'] = dataNoDuplicate['team_position'].astype('category').cat.codes
    dataNoDuplicate['work_rate'] = dataNoDuplicate['team_position'].astype('category').cat.codes

    dataNoDuplicate['league_rank'] = dataNoDuplicate['league_rank'].astype('int32')
    dataNoDuplicate = dataNoDuplicate.sort_values(by="sofifa_id")

    cleanList.append(dataNoDuplicate)

df_all = pd.concat(cleanList, join="inner")

df_all = df_all[df_all.groupby('sofifa_id')["sofifa_id"].transform('count') >= 3].copy()

df_positions = filter_position(df_all["player_positions"].values)

for col in df_positions.keys():
    df_all[col] = df_positions[col]

print(cleanList)
df_all = df_all.drop(columns=["player_positions"])

df_all.to_csv("allPlayers.csv", index=False)
