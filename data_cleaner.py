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
    dataNoDuplicate = dataNoDuplicate.drop(columns=[
        'player_url',
        'sofifa_id',
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
        'team_jersey_number'
    ])
    dataNoDuplicate = dataNoDuplicate.dropna(axis=0, how='any')
    # print(filter_position(dataNoDuplicate["player_positions"]))
    # dataNoDuplicate["player_positions"] = filter_position(dataNoDuplicate["player_positions"])
    # dataNoDuplicate['player_positions'] = dataNoDuplicate['player_positions'].astype('category').cat.codes
    dataNoDuplicate['nationality'] = dataNoDuplicate['nationality'].astype('category').cat.codes
    dataNoDuplicate['club_name'] = dataNoDuplicate['club_name'].astype('category').cat.codes
    dataNoDuplicate['league_name'] = dataNoDuplicate['league_name'].astype('category').cat.codes
    # dataNoDuplicate['player_positions'] = dataNoDuplicate['player_positions'].astype('category').cat.codes
    dataNoDuplicate['preferred_foot'] = dataNoDuplicate['preferred_foot'].astype('category').cat.codes
    dataNoDuplicate['team_position'] = dataNoDuplicate['team_position'].astype('category').cat.codes
    dataNoDuplicate['work_rate'] = dataNoDuplicate['team_position'].astype('category').cat.codes

    dataNoDuplicate['league_rank'] = dataNoDuplicate['league_rank'].astype('int32')
    dataNoDuplicate = dataNoDuplicate.sort_values(by="short_name")

    cleanList.append(dataNoDuplicate)

df_all = pd.concat(cleanList, join="inner")

df_all = df_all[df_all.groupby('short_name')["short_name"].transform('count') == 3].copy()

print(df_all.head())
df_positions = filter_position(df_all["player_positions"].values)

for col in df_positions.keys():
    df_all[col] = df_positions[col]

print(df_all.head())


df_all.to_csv("allPlayersCleaned.csv", index=False)
# df_target.to_csv("target.csv", index= False)
