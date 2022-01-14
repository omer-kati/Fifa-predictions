# Load the Pandas libraries with alias 'pd'
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
dataList = [data21,data20,data19,data18,data17,data16,data15]
dataNames = ["data15","data16","data17","data18","data19","data20","data21"]


notKeeper = data15["player_positions"] != "GK"
allPlayers = data15[notKeeper]["sofifa_id"].values

notDuplicate = data21["sofifa_id"].isin(allPlayers)
print(notDuplicate)
allPlayers = data21[notDuplicate]["sofifa_id"].values

def filter_position(list):
    newList= []
    for p in list:
        category = p.split(",")[0]
        if category in ["LW","ST","RW","CF"]:
            newList.append('attacker')
        elif category in ["LM","CM","RM","CAM","CDM"]:
            newList.append('midfielder')
        elif category in ["LB","CB","RB","LWB","RWB"]:
            newList.append('defender')
        else:
            newList.append('goal')

    return newList


cleanList = []

for d in dataList:
    dataNoDuplicate = d
    dataNoDuplicate = dataNoDuplicate.iloc[:, :80]
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
        'mentality_composure'
    ])
    dataNoDuplicate = dataNoDuplicate.dropna(axis=0,how='any')
    dataNoDuplicate["player_positions"] = filter_position(dataNoDuplicate["player_positions"])
    dataNoDuplicate['player_positions'] = dataNoDuplicate['player_positions'].astype('category').cat.codes
    dataNoDuplicate['nationality'] = dataNoDuplicate['nationality'].astype('category').cat.codes
    dataNoDuplicate['club_name'] = dataNoDuplicate['club_name'].astype('category').cat.codes
    dataNoDuplicate['league_name'] = dataNoDuplicate['league_name'].astype('category').cat.codes
    dataNoDuplicate['player_positions'] = dataNoDuplicate['player_positions'].astype('category').cat.codes
    dataNoDuplicate['preferred_foot'] = dataNoDuplicate['preferred_foot'].astype('category').cat.codes
    dataNoDuplicate['team_position'] = dataNoDuplicate['team_position'].astype('category').cat.codes
    dataNoDuplicate['work_rate'] = dataNoDuplicate['team_position'].astype('category').cat.codes

    dataNoDuplicate['team_jersey_number'] =dataNoDuplicate['team_jersey_number'].astype('int32')
    dataNoDuplicate['contract_valid_until'] =dataNoDuplicate['contract_valid_until'].astype('int32')
    dataNoDuplicate['league_rank'] =dataNoDuplicate['league_rank'].astype('int32')
    dataNoDuplicate['pace'] =dataNoDuplicate['pace'].astype('int32')
    dataNoDuplicate['shooting'] =dataNoDuplicate['shooting'].astype('int32')
    dataNoDuplicate['passing'] =dataNoDuplicate['passing'].astype('int32')
    dataNoDuplicate['dribbling'] =dataNoDuplicate['dribbling'].astype('int32')
    dataNoDuplicate['defending'] =dataNoDuplicate['defending'].astype('int32')
    dataNoDuplicate['physic'] =dataNoDuplicate['physic'].astype('int32')
    dataNoDuplicate = dataNoDuplicate.sort_values(by="sofifa_id")

    cleanList.append(dataNoDuplicate)


df_all= pd.concat(cleanList, join="inner")

df_all= df_all[df_all.groupby('sofifa_id')["sofifa_id"].transform('count') == 7].copy()

df_target= df_all[["sofifa_id",'overall']]
df_source= df_all.drop(columns=["overall"])


df_source.to_csv("source.csv", index= False)
df_target.to_csv("target.csv", index= False)

