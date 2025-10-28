import pandas as pd

'''
#https://www.nbastuffer.com/analytics101/game-score/
Game Score Formula=(Points)+0.4*(Field Goals Made)+0.7*(Offensive Rebounds)+0.3*(Defensive rebounds)
+(Steals)+0.7*(Assists)+0.7*(Blocked Shots)
- 0.7*(Field Goal Attempts)-0.4*(Free Throws Missed) - 0.4*(Personal Fouls)-(Turnovers)

do it per minute?
'''
def game_performance(player, table):
    points = 0
    rebounds = 0
    fouls = 0
    missed_shots = 0
    
    gameids = []
    
    reduced_table = table[table['player'] == player]
    for index, row in reduced_table.iterrows():
        #print(row)
        
        match row['type']:
            case 'Made Shot':
                points += 2
            case 'Rebound':
                rebounds += 1
            case 'Foul':
                fouls += 1
            case 'Missed Shot':
                missed_shots += 1
        
        if row['gameid'] not in gameids:
            gameids.append(row['gameid'])

    print(f"total points: {points}")
    print(f"Total games: {len(gameids)}")
    print(f"Total points per game: {points/len(gameids)}")

    total_score = points + 0.4 * (points/2) + 0.5 * rebounds - 0.7 * missed_shots - 0.4 * fouls
    print(f"avg game score per game: {total_score/len(gameids)}")


def test_performance():
    first_table = pd.read_csv("data/pbp1997.csv")
    #print(first_table.shape)
    
    '''
    #names = get_all_players(first_table)
    
    print(len(names))

    game_performance = {}

    for name in names:
        name_table = first_table[first_table['player']==name]
        game_performance[name] = game_performance(name, name_table)

    print(game_performance)
    '''

    pippen = first_table[first_table['player'] == "S. Pippen"]
    print(pippen.head())
    print(pippen.shape)

    game_performance("S. Pippen", pippen)



def get_all_players(table):
    player_names = []
    for index, row in table.iterrows():
        #player_index = 6
        #print(row)
        if (row['player'] not in player_names):
            player_names.append(row["player"])

    return player_names


if __name__ == "__main__":
    test_performance()