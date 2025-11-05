import pandas as pd
import re

'''
#https://www.nbastuffer.com/analytics101/game-score/

Game Score Formula=(Points)+0.4*(Field Goals Made)+0.7*(Offensive Rebounds)+0.3*(Defensive rebounds)
+(Steals)+0.7*(Assists)+0.7*(Blocked Shots)
- 0.7*(Field Goal Attempts)-0.4*(Free Throws Missed) - 0.4*(Personal Fouls)-(Turnovers)
do it per minute?
'''

def game_performance(player, table):
    
    def parse_description(phrase):
        nonlocal blocks, steals, game_def_rebounds, game_off_rebounds, turnovers
        
        if "STEAL" in phrase:
            steals += 1
        elif "REBOUND" in phrase:
            match = re.search(r'Off:(\d+)\s+Def:(\d+)', phrase)
            game_off_rebounds = int(match.group(1))
            game_def_rebounds =  int(match.group(2))
        elif "BLOCK" in phrase:
            blocks += 1
        elif 'Turnover' in phrase:
            turnovers += 1
        
    def parse_shot(phrase):
        nonlocal game_points,num_field_goals
        
        num_field_goals += 1

        if '3' in phrase:
            game_points += 3
        else:
            game_points += 2
    
    def parse_free_throw(phrase):
        nonlocal game_points, free_throw_misses
        
        if ('MISS' in phrase):
            free_throw_misses += 1
        else:
            game_points += 1

    steals = 0
    points = 0
    off_rebounds = 0
    def_rebounds = 0
    num_field_goals = 0
    free_throw_misses = 0

    game_off_rebounds = 0
    game_def_rebounds = 0
    game_points = 0
    fouls = 0
    missed_shots = 0
    blocks = 0
    turnovers = 0
    
    gameids = []
    
    reduced_table = table[table['player'] == player]
    for index, row in reduced_table.iterrows():
        #print(row)

        if row['gameid'] not in gameids:
            off_rebounds += game_off_rebounds
            def_rebounds += game_def_rebounds
            points += game_points

            game_points = 0
            game_off_rebounds = 0
            game_def_rebounds = 0
            gameids.append(row['gameid'])
        
        match row['type']:
            case 'Made Shot':
                parse_shot(row['desc'])
            case 'Rebound':
                parse_description(row['desc'])
            case 'Foul':
                fouls += 1
            case 'Missed Shot':
                num_field_goals += 1
                missed_shots += 1
            case 'Free Throw':
                parse_free_throw(row['desc'])
            case 'NaN':
                parse_description(row['desc'])

    
    #Total score I think
    #Don't have assists, may need to adjust for that
    total_score = points + 0.4 * num_field_goals + 0.7 * off_rebounds + 0.3 * def_rebounds  + steals + 0.7 * blocks - 0.7 * num_field_goals - 0.4 * free_throw_misses - 0.4 * fouls - turnovers
    
    '''
    Game Score Formula=(Points)+0.4*(Field Goals Made)+0.7*(Offensive Rebounds)+0.3*(Defensive rebounds)
    +(Steals)+0.7*(Assists)+0.7*(Blocked Shots)
    - 0.7*(Field Goal Attempts)-0.4*(Free Throws Missed) - 0.4*(Personal Fouls)-(Turnovers)
    
    '''
    
    if (len(gameids) != 0):
         print(f"{player} avg game score per game: {total_score/len(gameids)}")


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

    #pippen = first_table[first_table['player'] == "S. Pippen"]
    #print(pippen.head())
    #print(pippen.shape)

    names = get_all_players(first_table)
    for name in names:
        game_performance(name, first_table)
        print(name)

    #game_performance("S. Pippen", pippen)



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