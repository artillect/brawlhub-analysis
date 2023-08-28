import csv
import pandas as pd
import seaborn as sns
from pandas.io.formats.style import Styler
import plotly.express as px
import plotly.graph_objects as go


# Load the data into a DataFrame
S1W1 = pd.read_csv('S1 - Pairings - S1W1.csv', header=0)
S1W2 = pd.read_csv('S1 - Pairings - S1W2.csv', header=0)
S1W3 = pd.read_csv('S1 - Pairings - S1W3.csv', header=0)
S1W4 = pd.read_csv('S1 - Pairings - S1W4.csv', header=0)

S2W1 = pd.read_csv('S2 - Pairings - S2W1.csv', header=0)
S2W2 = pd.read_csv('S2 - Pairings - S2W2.csv', header=0)
S2W3 = pd.read_csv('S2 - Pairings - S2W3.csv', header=0)
S2W4 = pd.read_csv('S2 - Pairings - S2W4.csv', header=0)

S3W1 = pd.read_csv('S3 - Pairings - S3W1.csv', header=0)
S3W2 = pd.read_csv('S3 - Pairings - S3W2.csv', header=0)
S3W3 = pd.read_csv('S3 - Pairings - S3W3.csv', header=0)
S3W4 = pd.read_csv('S3 - Pairings - S3W4.csv', header=0)

S4W1 = pd.read_csv('S4 - Pairings - S4W1.csv', header=0)
S4W2 = pd.read_csv('S4 - Pairings - S4W2.csv', header=0)
S4W3 = pd.read_csv('S4 - Pairings - S4W3.csv', header=0)
S4W4 = pd.read_csv('S4 - Pairings - S4W4.csv', header=0)

S5W1 = pd.read_csv('S5 - League Database - Week1.csv', header=0)
S5W2 = pd.read_csv('S5 - League Database - Week2.csv', header=0)
S5W3 = pd.read_csv('S5 - League Database - Week3.csv', header=0)
S5W4 = pd.read_csv('S5 - League Database - Week4.csv', header=0)

S6W1 = pd.read_csv('S6 - Pairings - S6W1.csv', header=0)
S6W2 = pd.read_csv('S6 - Pairings - S6W2.csv', header=0)
S6W3 = pd.read_csv('S6 - Pairings - S6W3.csv', header=0)
S6W4 = pd.read_csv('S6 - Pairings - S6W4.csv', header=0)

# Create a dictionary to store the winrates for each commander matchup
winrates = {}

# Create an array of pairs of players
matchups = {}

week_num = 1

# Iterate over each week of data
for week in [S1W1, S1W2, S1W3, S1W4, S2W1, S2W2, S2W3, S2W4, S3W1, S3W2, S3W3, S3W4, S4W1, S4W2, S4W3, S4W4, S5W1, S5W2, S5W3, S5W4, S6W1, S6W2, S6W3, S6W4]:
    print(week_num)
    week_num += 1
    
    # Clear the list of matchups
    matchups = {}

    # Iterate over each row in the data
    for index, row in week.iterrows():
        # Get the commander for this row
        commander = row['Commander']
        player = row['Discord tag']
        
        # Check if commander is blank or nan
        if pd.isnull(commander) or commander == '':
            continue

        # Initialize the winrate for this commander if it doesn't already exist
        if commander not in winrates:
            winrates[commander] = {}
        
        # Iterate over the opponent columns
        for col in ['Adversaire 1', 'Adversaire 2', 'Adversaire 3']:
            # Get the opponent and score for this column
            opponent = row[col]

            # Get the opponent's commander
            # Check each row in the data
            for index2, row2 in week.iterrows():
                # If this row is for the opponent
                if row2['Discord tag'] == opponent:
                    # Get the opponent's commander
                    opponent_commander = row2['Commander']
                    if opponent_commander not in winrates:
                        winrates[opponent_commander] = {}
                    break

            # Check if opponent is blank or nan
            if pd.isnull(opponent) or opponent == '':
                continue

            # Get both players' scores
            playerScore = row.iloc[week.columns.get_loc(col) + 1]
            opponentScore = row.iloc[week.columns.get_loc(col) + 2]
            
            # Check if this is a valid matchup (i.e. not a duplicate)
            # if player != '' and commander != '' and opponent != '' and playerScore != '' and opponentScore != '':
            if not pd.isnull(player) and not pd.isnull(commander) and not pd.isnull(opponent) and not pd.isnull(playerScore) and not pd.isnull(opponentScore):
                # Initialize the winrate for this opponent if it doesn't already exist
                if opponent_commander not in winrates[commander]:
                    winrates[commander][opponent_commander] = {'match_wins': 0, 'total_matches': 0, 'game_wins': 0, 'total_games': 0}
                
                if commander not in winrates[opponent_commander]:
                    winrates[opponent_commander][commander] = {'match_wins': 0, 'total_matches': 0, 'game_wins': 0, 'total_games': 0}
                
                # Check if this pair of players has already played
                if (opponent, player) not in matchups:
                    # Update the winrate for this commander against this opponent
                    winrates[commander][opponent_commander]['total_matches'] += 1
                    # Check if playerscore is an int
                    if not isinstance(playerScore, int):
                        print('playerScore is not an int')
                    winrates[commander][opponent_commander]['game_wins'] += playerScore
                    winrates[commander][opponent_commander]['total_games'] += playerScore + opponentScore
                    if playerScore - opponentScore > 0:
                        winrates[commander][opponent_commander]['match_wins'] += 1
                    # Update the winrate for this commander against this opponent
                    winrates[opponent_commander][commander]['total_matches'] += 1
                    winrates[opponent_commander][commander]['game_wins'] += opponentScore
                    winrates[opponent_commander][commander]['total_games'] += playerScore + opponentScore
                    if playerScore - opponentScore < 0:
                        winrates[opponent_commander][commander]['match_wins'] += 1

                    # Add this pair of players to the list of matchups
                    matchups[(player, opponent)] = True
                # else:
                #     print(f'  {player} vs {opponent} already played')

# Sort commander winrates by sum of all matches
winrates = {k: v for k, v in sorted(winrates.items(), key=lambda item: sum([v2['total_matches'] for k2, v2 in item[1].items()]), reverse=True)}

# Sort winrates against each opponent
for commander in winrates:
    winrates[commander] = {k: v for k, v in sorted(winrates[commander].items(), key=lambda item: item[1]['total_matches'], reverse=True)}

# Calculate the final winrates for each commander matchup
for commander in winrates:
    print(f'{commander}:')
    # Calculate total winrate for this commander
    total_wins = 0
    total_games = 0
    for opponent in winrates[commander]:
        total_wins += winrates[commander][opponent]['game_wins']
        total_games += winrates[commander][opponent]['total_games']
    # print(f'  Total: {total_wins / total_games:.2f}')
    for opponent in winrates[commander]:
        try:
            game_winrate = winrates[commander][opponent]['game_wins'] / winrates[commander][opponent]['total_games']
        except:
            game_winrate = 0
        total_matches = winrates[commander][opponent]['total_matches']
        if pd.isnull(total_matches):
            print('ERROR total matches is null')
        match_winrate = winrates[commander][opponent]['match_wins'] / total_matches
        if pd.isnull(match_winrate):
            print('ERROR match winrate is null')
        print(f'  {opponent}: {total_matches} {game_winrate:.2f} {match_winrate:.2f}')

# Find commander with highest winrate against a given set of commanders
best_commanders = {'Raffine, Scheming Seer','Rusko, Clockmaker','Atraxa, Grand Unifier','Teferi, Hero of Dominaria','Sythis, Harvests Hand','Adeline, Resplendent Cathar','Ragavan, Nimble Pilferer'}

best_commander = ''
best_winrate = 0

for commander in winrates:
    # Check if this commander has played against at least some number of the best commanders greater than some threshold
    num_best_commanders = 0

    for opponent in winrates[commander]:
        if opponent in best_commanders and winrates[commander][opponent]['total_matches'] > 0 and winrates[commander][opponent]['total_games'] > 0:
            num_best_commanders += 1

    if num_best_commanders < 5:
        # print(f'{commander} has only played against {num_best_commanders} of the best commanders')
        continue
    # Get total number of match wins and matches against the best commanders
    total_match_wins = 0
    total_matches = 0
    for opponent in winrates[commander]:
        if opponent in best_commanders:
            total_match_wins += winrates[commander][opponent]['match_wins']
            total_matches += winrates[commander][opponent]['total_matches']

    # Get total number of game wins and games against the best commanders
    total_game_wins = 0
    total_games = 0
    for opponent in winrates[commander]:
        if opponent in best_commanders:
            total_game_wins += winrates[commander][opponent]['game_wins']
            total_games += winrates[commander][opponent]['total_games']

    # Calculate winrate against the best commanders
    if total_matches > 0:
        match_winrate = total_match_wins / total_matches
    else:
        match_winrate = 0

    if total_games > 0:
        game_winrate = total_game_wins / total_games
    else:
        game_winrate = 0

    if game_winrate > best_winrate:
        best_winrate = game_winrate
        best_commander = commander
        print(f'New best commander: {best_commander} ({best_winrate:.2f})')
        # Print commander's winrates against the best commanders
        for opponent in winrates[commander]:
            if opponent in best_commanders:
                print(f'  {opponent}: {winrates[commander][opponent]["total_matches"]} {winrates[commander][opponent]["game_wins"] / winrates[commander][opponent]["total_games"]:.2f} {winrates[commander][opponent]["match_wins"] / winrates[commander][opponent]["total_matches"]:.2f}')

print(f'Best commander: {best_commander} ({best_winrate:.2f})')



# Save the game winrates to a CSV file
# First column is the player's commander, and the first row is the opponent's commander
# The data is the winrate for the player's commander against the opponent's commander
with open('game_winrates.csv', 'w', newline='') as csvfile:
    # Create dataframe for winrates
    winrate_df = pd.DataFrame(columns=winrates.keys(), index=winrates.keys())
    for commander in winrates:
        for opponent in winrates[commander]:
            try:
                total_games = winrates[commander][opponent]['total_games']
                winrate_df[commander][opponent] = winrates[commander][opponent]['game_wins'] / total_games
            except:
                continue
    winrate_df.to_csv(csvfile)

# First column is the player's commander, and the first row is the opponent's commander
# The data is the winrate for the player's commander against the opponent's commander
winrate_table = pd.DataFrame(columns=winrates.keys(), index=pd.MultiIndex.from_product([winrates.keys(),['match_winrate','total_matches','game_winrate','total_games']]))

for commander in winrates:
    for opponent in winrates[commander]:

        total_matches = winrates[commander][opponent]['total_matches']
        total_games = winrates[commander][opponent]['total_games']
        if total_games == 0 or pd.isnull(total_games):
            continue
        winrate_table[opponent][commander, 'game_winrate'] = winrates[commander][opponent]['game_wins'] / total_games
        winrate_table[opponent][commander, 'match_winrate'] = winrates[commander][opponent]['match_wins'] / total_matches
        winrate_table[opponent][commander, 'total_matches'] = total_matches
        winrate_table[opponent][commander, 'total_games'] = total_games


# Create table of overall winrates for each commander
overall_winrates = pd.DataFrame(columns=['game_winrate','total_games','match_winrate','total_matches','total_wins','weighted_game_winrate'], index=winrates.keys())
for commander in winrates:
    game_winrate = 0
    total_games = 0
    total_wins = 0
    total_matches = 0
    match_winrate = 0
    for opponent in winrates[commander]:
        game_winrate += winrates[commander][opponent]['game_wins']
        total_games += winrates[commander][opponent]['total_games']
        total_wins += winrates[commander][opponent]['match_wins']
        total_matches += winrates[commander][opponent]['total_matches']
    if total_games > 0:
        game_winrate /= total_games
    if total_matches > 0:
        match_winrate = total_wins / total_matches

    overall_winrates['game_winrate'][commander] = game_winrate
    overall_winrates['total_games'][commander] = total_games
    overall_winrates['match_winrate'][commander] = match_winrate
    overall_winrates['total_wins'][commander] = total_wins
    overall_winrates['total_matches'][commander] = total_matches

# Calculate winrate weighted by winrate of opponents
for commander in overall_winrates.index:
    weighted_game_winrate = 0
    total_games = 0
    for opponent in winrates[commander]:
        if opponent in overall_winrates.index:
            weighted_game_winrate += winrates[commander][opponent]['game_wins'] * overall_winrates['game_winrate'][opponent]
            total_games += winrates[commander][opponent]['total_games']
    if total_games > 0:
        weighted_game_winrate /= total_games
    overall_winrates['weighted_game_winrate'][commander] = weighted_game_winrate

overall_winrates = overall_winrates.fillna(0)

# Get list of commanders sorted by number of matches played
commanders_by_matches = overall_winrates.sort_values(by='total_matches', ascending=False).index