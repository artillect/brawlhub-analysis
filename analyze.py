import csv
import pandas as pd
import seaborn as sns
from pandas.io.formats.style import Styler

archetypes = pd.read_csv('commanders.csv', header=0)

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

        # # Initialize the winrate for this commander if it doesn't already exist
        # if commander not in winrates:
        #     winrates[commander] = {}
        
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

            # Get both players' commanders' colors from archetypes
            for commanders in archetypes['Commander']:
                if commanders == commander:
                    player_colors = archetypes['Color Combo'][archetypes['Commander'] == commanders].values[0]
                if commanders == opponent_commander:
                    opponent_colors = archetypes['Color Combo'][archetypes['Commander'] == commanders].values[0]

            print(player_colors, opponent_colors)
            if player_colors not in winrates:
                winrates[player_colors] = {}
            if opponent_colors not in winrates:
                winrates[opponent_colors] = {}

            # Check if opponent is blank or nan
            if pd.isnull(opponent) or opponent == '':
                continue

            # Get both players' scores
            playerScore = row.iloc[week.columns.get_loc(col) + 1]
            opponentScore = row.iloc[week.columns.get_loc(col) + 2]
            
            # Check if this is a valid matchup (i.e. not a duplicate)
            # if player != '' and commander != '' and opponent != '' and playerScore != '' and opponentScore != '':
            if not pd.isnull(player) and not pd.isnull(commander) and not pd.isnull(opponent) and not pd.isnull(playerScore) and not pd.isnull(opponentScore):
                # Check if this pair of players has already played
                if (opponent, player) not in matchups:
                    # Initialize the winrate for this opponent if it doesn't already exist
                    if opponent_colors not in winrates[player_colors]:
                        winrates[player_colors][opponent_colors] = {'match_wins': 0, 'total_matches': 0, 'game_wins': 0, 'total_games': 0}
                    
                    if player_colors not in winrates[opponent_colors]:
                        winrates[opponent_colors][player_colors] = {'match_wins': 0, 'total_matches': 0, 'game_wins': 0, 'total_games': 0}
                    # Update the winrate for this commander against this opponent
                    winrates[player_colors][opponent_colors]['total_matches'] += 1
                    # Check if playerscore is an int
                    if not isinstance(playerScore, int):
                        print('playerScore is not an int')
                    winrates[player_colors][opponent_colors]['game_wins'] += playerScore
                    winrates[player_colors][opponent_colors]['total_games'] += playerScore + opponentScore
                    if playerScore - opponentScore > 0:
                        winrates[player_colors][opponent_colors]['match_wins'] += 1

                    # Update the winrate for this commander against this opponent
                    winrates[opponent_colors][player_colors]['total_matches'] += 1
                    winrates[opponent_colors][player_colors]['game_wins'] += opponentScore
                    winrates[opponent_colors][player_colors]['total_games'] += playerScore + opponentScore
                    if playerScore - opponentScore < 0:
                        winrates[opponent_colors][player_colors]['match_wins'] += 1

                    # Add this pair of players to the list of matchups
                    matchups[(player, opponent)] = True
                # else:
                #     print(f'  {player} vs {opponent} already played')

# Sort winrates against each opponent
for colors in winrates:
    winrates[colors] = {k: v for k, v in sorted(winrates[colors].items(), key=lambda item: item[1]['total_matches'], reverse=True)}

# Calculate the final winrates for each commander matchup
for colors in winrates:
    print(f'{colors}:')
    # Calculate total winrate for this commander
    total_wins = 0
    total_games = 0
    for opponent_colors in winrates[colors]:
        total_wins += winrates[colors][opponent_colors]['game_wins']
        total_games += winrates[colors][opponent_colors]['total_games']
    # print(f'  Total: {total_wins / total_games:.2f}')
    for opponent_colors in winrates[colors]:
        try:
            game_winrate = winrates[colors][opponent_colors]['game_wins'] / winrates[colors][opponent_colors]['total_games']
        except:
            game_winrate = 0
        total_matches = winrates[colors][opponent_colors]['total_matches']
        if pd.isnull(total_matches):
            print('ERROR total matches is null')
        match_winrate = winrates[colors][opponent_colors]['match_wins'] / total_matches
        winrates[colors][opponent_colors]['match_winrate'] = match_winrate
        winrates[colors][opponent_colors]['game_winrate'] = game_winrate
        if pd.isnull(match_winrate):
            print('ERROR match winrate is null')
        print(f'  {opponent_colors}: {total_matches} {game_winrate:.2f} {match_winrate:.2f}')

# Find overall winrates for each color
overall_winrates = {}
for color in winrates:
    if color not in overall_winrates:
        overall_winrates[color] = {'match_wins': 0, 'total_matches': 0, 'game_wins': 0, 'total_games': 0}
    for opponent_colors in winrates[color]:
        overall_winrates[color]['match_wins'] += winrates[color][opponent_colors]['match_wins']
        overall_winrates[color]['total_matches'] += winrates[color][opponent_colors]['total_matches']
        overall_winrates[color]['game_wins'] += winrates[color][opponent_colors]['game_wins']
        overall_winrates[color]['total_games'] += winrates[color][opponent_colors]['total_games']

# Calculate overall winrates for each color
for color in overall_winrates:
    overall_winrates[color]['match_winrate'] = overall_winrates[color]['match_wins'] / overall_winrates[color]['total_matches']
    overall_winrates[color]['game_winrate'] = overall_winrates[color]['game_wins'] / overall_winrates[color]['total_games']

# Sort overall winrates by game winrate
overall_winrates = {k: v for k, v in sorted(overall_winrates.items(), key=lambda item: item[1]['game_winrate'], reverse=False)}

# Remove colors with less than 10 matches
overall_winrates = {k: v for k, v in overall_winrates.items() if v['total_matches'] >= 70}

# get average number of matches per color
total_matches = 0
for color in overall_winrates:
    total_matches += overall_winrates[color]['total_matches']
print(f'Average number of matches per color: {total_matches / len(overall_winrates):.2f}')

# # Find commander with highest winrate against a given set of commanders
# best_commanders = {'Raffine, Scheming Seer','Rusko, Clockmaker','Atraxa, Grand Unifier','Teferi, Hero of Dominaria','Sythis, Harvests Hand','Adeline, Resplendent Cathar','Ragavan, Nimble Pilferer'}

# best_commander = ''
# best_winrate = 0

# for commander in winrates:
#     # Check if this commander has played against at least some number of the best commanders greater than some threshold
#     num_best_commanders = 0

#     for opponent in winrates[commander]:
#         if opponent in best_commanders and winrates[commander][opponent]['total_matches'] > 0 and winrates[commander][opponent]['total_games'] > 0:
#             num_best_commanders += 1

#     if num_best_commanders < 5:
#         # print(f'{commander} has only played against {num_best_commanders} of the best commanders')
#         continue
#     # Get total number of match wins and matches against the best commanders
#     total_match_wins = 0
#     total_matches = 0
#     for opponent in winrates[commander]:
#         if opponent in best_commanders:
#             total_match_wins += winrates[commander][opponent]['match_wins']
#             total_matches += winrates[commander][opponent]['total_matches']

#     # Get total number of game wins and games against the best commanders
#     total_game_wins = 0
#     total_games = 0
#     for opponent in winrates[commander]:
#         if opponent in best_commanders:
#             total_game_wins += winrates[commander][opponent]['game_wins']
#             total_games += winrates[commander][opponent]['total_games']

#     # Calculate winrate against the best commanders
#     if total_matches > 0:
#         match_winrate = total_match_wins / total_matches
#     else:
#         match_winrate = 0

#     if total_games > 0:
#         game_winrate = total_game_wins / total_games
#     else:
#         game_winrate = 0

#     if game_winrate > best_winrate:
#         best_winrate = game_winrate
#         best_commander = commander
#         print(f'New best commander: {best_commander} ({best_winrate:.2f})')
#         # Print commander's winrates against the best commanders
#         for opponent in winrates[commander]:
#             if opponent in best_commanders:
#                 print(f'  {opponent}: {winrates[commander][opponent]["total_matches"]} {winrates[commander][opponent]["game_wins"] / winrates[commander][opponent]["total_games"]:.2f} {winrates[commander][opponent]["match_wins"] / winrates[commander][opponent]["total_matches"]:.2f}')

# print(f'Best commander: {best_commander} ({best_winrate:.2f})')

winrates_df = pd.DataFrame(columns=overall_winrates.keys(), index=pd.MultiIndex.from_product([overall_winrates.keys()]))

# Make dataframe of winrates
for colors in overall_winrates.keys():
    for opponent_colors in overall_winrates.keys():
        try:
            winrate = winrates[colors][opponent_colors]['game_wins'] / winrates[colors][opponent_colors]['total_games']
        except:
            continue
        if colors not in winrates_df:
            winrates_df[colors] = {}
        if opponent_colors not in winrates_df[colors]:
            winrates_df[colors][opponent_colors] = {}
        winrates_df[colors][opponent_colors] = winrate

cm = sns.diverging_palette(10, 220, as_cmap=True)

# Save dataframe to html
winrates_df = pd.DataFrame(winrates_df)
winrates_df.style \
    .background_gradient(cmap=cm) \
    .format(precision=2) \
    .to_html('color winrates.html')