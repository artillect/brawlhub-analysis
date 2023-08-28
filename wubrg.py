import csv
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import plotly.colors as pc
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
wubrg = {}

for color in ['W', 'U', 'B', 'R', 'G']:
    if color not in wubrg:
        wubrg[color] = {}

    for color2 in ['W', 'U', 'B', 'R', 'G']:
        wubrg[color][color2] = {'match_wins': 0, 'total_matches': 0, 'game_wins': 0, 'total_games': 0}

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
                    player_color_combo = archetypes['Color Combo'][archetypes['Commander'] == commanders].values[0]
                if commanders == opponent_commander:
                    opponent_color_combo = archetypes['Color Combo'][archetypes['Commander'] == commanders].values[0]

            # Break color combos into an array
            # Ex. 'WUBRG' -> ['W', 'U', 'B', 'R', 'G']
            player_colors = list(player_color_combo)
            opponent_colors = list(opponent_color_combo)

            print(player_colors, opponent_colors)

            # Check if colors share a color
            share_color = False
            for color in player_colors:
                if color in opponent_colors:
                    share_color = True
            
            if share_color:
                continue

            # Check if opponent is blank or nan
            if pd.isnull(opponent) or opponent == '':
                continue

            # Get both players' scores
            playerScore = row.iloc[week.columns.get_loc(col) + 1]
            opponentScore = row.iloc[week.columns.get_loc(col) + 2]
            
            if not pd.isnull(player) and not pd.isnull(commander) and not pd.isnull(opponent) and not pd.isnull(playerScore) and not pd.isnull(opponentScore):
                # Check if this pair of players has already played
                if (opponent, player) not in matchups:
                    for player_color in player_colors:
                        if player_color not in wubrg:
                            wubrg[player_color] = {} 
                        print(player_color)                       
                        for opponent_color in opponent_colors:
                            print(opponent_color)

                            if opponent_color not in wubrg:
                                wubrg[opponent_color] = {}
                            # if player_color == opponent_color:
                            #     continue

                            if opponent_color not in wubrg[player_color]:
                                print('opponent_color not in wubrg[player_color]')
                                wubrg[player_color][opponent_color] = {'match_wins': 0, 'total_matches': 0, 'game_wins': 0, 'total_games': 0}
                            
                            if player_color not in wubrg[opponent_color]:
                                print('player_color not in wubrg[opponent_color]')
                                wubrg[opponent_color][player_color] = {'match_wins': 0, 'total_matches': 0, 'game_wins': 0, 'total_games': 0}

                            # Update the winrate for this commander against this opponent
                            wubrg[player_color][opponent_color]['total_matches'] += 1
                            # Check if playerscore is an int
                            if not isinstance(playerScore, int):
                                print('playerScore is not an int')
                            wubrg[player_color][opponent_color]['game_wins'] += playerScore
                            wubrg[player_color][opponent_color]['total_games'] += playerScore + opponentScore
                            if playerScore - opponentScore > 0:
                                wubrg[player_color][opponent_color]['match_wins'] += 1

                            # Update the winrate for this commander against this opponent
                            wubrg[opponent_color][player_color]['total_matches'] += 1
                            wubrg[opponent_color][player_color]['game_wins'] += opponentScore
                            wubrg[opponent_color][player_color]['total_games'] += playerScore + opponentScore
                            if playerScore - opponentScore < 0:
                                wubrg[opponent_color][player_color]['match_wins'] += 1

                    # Add this pair of players to the list of matchups
                    matchups[(player, opponent)] = True
                # else:
                #     print(f'  {player} vs {opponent} already played')

# # Sort winrates against each opponent
# for color in wubrg:
#     wubrg[color] = {k: v for k, v in sorted(wubrg[color].items(), key=lambda item: item[1]['total_matches'], reverse=True)}

# Calculate the final winrates for each commander matchup
for color in wubrg:
    print(f'{color}:')
    # Calculate total winrate for this commander
    total_wins = 0
    total_games = 0
    for opponent_color in wubrg[color]:
        total_wins += wubrg[color][opponent_color]['game_wins']
        total_games += wubrg[color][opponent_color]['total_games']
    # print(f'  Total: {total_wins / total_games:.2f}')
    for opponent_colors in wubrg[color]:
        try:
            game_winrate = wubrg[color][opponent_colors]['game_wins'] / wubrg[color][opponent_colors]['total_games']
        except:
            game_winrate = 0
        total_matches = wubrg[color][opponent_colors]['total_matches']
        if total_matches == 0:
            continue
        if pd.isnull(total_matches):
            print('ERROR total matches is null')
        match_winrate = wubrg[color][opponent_colors]['match_wins'] / total_matches
        wubrg[color][opponent_colors]['match_winrate'] = match_winrate
        wubrg[color][opponent_colors]['game_winrate'] = game_winrate
        if pd.isnull(match_winrate):
            print('ERROR match winrate is null')
        print(f'  {opponent_colors}: {total_matches} {game_winrate:.2f} {match_winrate:.2f}')

# # Find overall winrates for each color
# for color in wubrg:
#     total_wins = 0
#     total_games = 0
#     for opponent_color in wubrg[color]:
#         total_wins += wubrg[color][opponent_color]['game_wins']
#         total_games += wubrg[color][opponent_color]['total_games']
#     wubrg[color]['total_winrate'] = total_wins / total_games
#     print(f'{color}: {total_wins / total_games:.2f}')

# Display the winrates in a table
# Create a dataframe to hold the winrates
# First row and column are the colors
# Each cell is the winrate for the row color against the column color
winrates = pd.DataFrame(columns=wubrg.keys(), index=wubrg.keys())
for color in wubrg:
    for opponent_color in wubrg[color]:
        try:
            winrates[opponent_color][color] = wubrg[color][opponent_color]['game_winrate']
        except:
            continue
        if color == opponent_color:
            winrates[opponent_color][color] = 0.5

winrates.fillna('---')

# fig = go.Figure([go.Table(
#     header=dict(values=[''] + list(winrates.index),
#                 fill_color='paleturquoise',
#                 align='left',
#                 font=dict(color='black', size=11)),
#     # cells=dict(values=[winrates.index] + [winrates[c] for c in winrates.columns],
#                 # align='left', format=["",".1%"]))
#     cells=dict(values=[winrates.index] + [winrates[c] for c in winrates.columns],
#                # Color cells based on winrate
#                 fill_color=['paleturquoise'] + [['red' if x > 0.5 else 'blue' if x < 0.5 else 'grey' for x in row] for row in winrates.values],
#                 align='left', format=["",".1%"],
#                 font=dict(color=['black','white'], size=11)))
# ])

# fig.show()

# cm = sns.diverging_palette(10, 220, sep=80, n=7, as_cmap=True)

# winrates.apply(pd.to_numeric).style \
#     .background_gradient(cmap=cm, vmin=0, vmax=1) \
#     .format(precision=2) \
#     .to_html('wubrg winrates.html')

# Convert wubrg dictionary into a dataframe
wubrg_df = pd.DataFrame.from_dict(wubrg, orient='index')

# Make separate dataframe for total matches
# FIXME: error: too many indexers
# total_matches = wubrg_df.loc[pd.IndexSlice[:,:,'total_matches']].copy()

total_games = pd.DataFrame(index=wubrg_df.index, columns=wubrg_df.columns)
for color in wubrg:
    for opponent_color in wubrg[color]:
        total_games[opponent_color][color] = wubrg[color][opponent_color]['total_games']

print(total_matches)

print(wubrg_df.unstack())

# Use plotly to display matrix heatmap of winrates
fig = go.Figure(data=go.Heatmap(
                     z=winrates.apply(pd.to_numeric).values,
                    x=winrates.columns,
                    y=winrates.index,
                    colorscale='RdBu',
                    zmin=0,
                    zmax=1,
                    ))

fig.update_traces(customdata=total_games.values,
                  hovertext=total_games.values,
                    hovertemplate="%{y} vs. %{x}<br>Game win rate: %{z:.0%}<br>(%{customdata} games)<extra></extra>",
                    texttemplate="%{z:.0%}")

fig.update_yaxes(autorange="reversed")

# Show x axis labels on top
fig.update_layout(xaxis_side="top")

fig.show()