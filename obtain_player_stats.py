#! /usr/bin/env python3
"""
    Provides functions for:
        * recording tournaments each player has attended
        * printing input-player's wins and losses at each tournament
"""

import collections
import os
import argparse

def get_trueskill_list():
    player_ratings = {}
    with open('./data/64SinglesTrueSkill.csv','r') as finput:
        for line in finput:
            parts = line.strip().split(',')
            if 'player,mu,sigma,wins,losses,sets' in line:
                continue
            playername = parts[0]
            rating = float(parts[1])
            sigma_rating = float(parts[2])

            player_ratings[playername] = [rating, sigma_rating]
    return player_ratings


def get_detailed_tournament_info():
    # Generate tournament dictionary
    tournamentlist = {}
    tourneyinfo_dict = {}
    tourneyinfo_list = []

    with open('./data/tournaments.csv', 'r') as tourneyinput:
        for line in tourneyinput:
            if 'Tournament,slug,startDate,endDate,entrants' in line:
                continue
            parts = line.strip().split(',')
            tournamentlist[parts[1]] = parts[0]  # map slug to abbreviated name
            # convert date to list
            dateobj = [ int(x) for x in parts[2].split('-') ]
            tourneyinfo_dict[parts[0]] = [parts[1], dateobj, int(parts[4])]  # slug, date, entrants
            tourneyinfo_list.append( [parts[0], dateobj, int(parts[4]) ] )

    tourneyinfo_list.sort(key=lambda x:x[1], reverse=True)  # Sorted so most recent tournament is first.
    return tourneyinfo_dict, tourneyinfo_list


def get_player_tournaments():
    playertournaments = collections.defaultdict(set)

    with open('./data/all-stats.csv', 'r') as finput:
        for line in finput:
            parts = line.strip().split(',')
            playertournaments[parts[0]].add(parts[5])
            playertournaments[parts[1]].add(parts[5])

    return playertournaments


# Input a player, print all their wins and losses, by tournament.
def get_player_record(input_player='kerokeroppi'):

    # First get tournament list:
    playerinfo = {}
    playertournaments = get_player_tournaments()

    if input_player not in playertournaments:
        return None

    for tourney in playertournaments[input_player]:
        playerinfo[tourney] = {'wins':[], 'losses':[]}

    # iterate over full dataset
    with open('./data/all-stats.csv', 'r') as finput:
        for line in finput:
            parts = line.strip().split(',')
            player1 = parts[0]
            player2 = parts[1]
            winning_player = int(parts[2])
            p1wins = int(parts[3])
            p2wins = int(parts[4])
            tourney_name = parts[5]

            if input_player != player1 and input_player != player2:
                continue
            else:
                input_player_number = 0
                opponent_name = player2
                if input_player == player2:
                    input_player_number = 1
                    opponent_name = player1

                key_to_use = 'losses'
                if input_player_number == winning_player:
                    key_to_use = 'wins'

                playerinfo[tourney_name][key_to_use].append( [opponent_name,  max(p1wins, p2wins), min(p1wins, p2wins) ] )

    # Sort tournament list with most recent results first
    tourneyinfo_dict, tourneyinfo_list = get_detailed_tournament_info()

    player_tourney_list = [ ( x, tourneyinfo_dict[x]) for x in playerinfo.keys() ]
    player_tourney_list.sort(key=lambda x:x[1][1], reverse=True)  # Sorted so most recent tournament is first.

    # Print results
    player_ratings = get_trueskill_list()
    print("\n"+input_player)
    print("{s:{charused}^{num}}".format(s='',charused="=",num=len(input_player)) )
    string_power_level1 = "Power level: {:>6.1f} ".format(player_ratings[input_player][0])
    string_power_level2 = "(\t larger = better, boom is 50+, new-comers are ~10)"
    print(string_power_level1, string_power_level2)
    string_accuracy1 = "Accuracy   : {:>5.1f} ".format(player_ratings[input_player][1])
    string_accuracy2 = "(\t smaller = more accurate, < 1 is great, 2 is ok, 3 is bad )"
    print(string_accuracy1, string_accuracy2)

    player_history = {}
    player_history["header"] = [ input_player, string_power_level1, string_power_level2, string_accuracy1, string_accuracy2 ]
    player_history["tournaments"] = []

    def printing_result(match_row, player_ratings):
        opponent_name = match_row[0]
        pname = match_row[0]
        match_results = match_row[1:3]
        opp_skill = player_ratings[opponent_name][0]
        opp_var = player_ratings[opponent_name][1]
        print("{s:{charused}<20} {}-{} ..... ({:>5.1f}, {:3.1f})".format(*match_results, opp_skill, opp_var, s=pname, charused="_"))
        
        return [pname, *match_results, "{:>5.1f}".format(opp_skill), "{:3.1f}".format(opp_var)]

    for tourneyname, tourney in player_tourney_list:
        full_tournament = {}
        match_record = playerinfo[ tourneyname ]
        datestr = str(tourney[1][0]) + '-' + str(tourney[1][1]) + '-' + str(tourney[1][2])
        header_string = "\n{:<20}, {},   Entrants: {}".format(tourneyname, datestr, tourney[2])
        print(header_string)

        full_tournament["header"] = [tourneyname, datestr, tourney[2] ]
        full_tournament["wins"] = []
        print("  W:")
        for match_row in match_record['wins']:
            full_tournament["wins"].append(printing_result(match_row, player_ratings))

        full_tournament["losses"] = []
        print("  L:")
        for match_row in match_record['losses']:
            full_tournament["losses"].append(printing_result(match_row, player_ratings))

        print("FULL TOURNAMENT HEADER:")
        print(full_tournament["header"])
        player_history["tournaments"].append(full_tournament)


    return player_history


def print_trueskill():
    player_ratings = []
    with open('./data/64SinglesTrueSkill.csv','r') as finput:
        for line in finput:
            parts = line.strip().split(',')
            if 'player,mu,sigma,wins,losses,sets' in line:
                continue
            playername = parts[0]
            rating = float(parts[1])
            sigma_rating = float(parts[2])

            player_ratings.append( tuple(payername, rating, sigma_rating) )

    sorted( 'descending', player_ratings, key=lambda x: x[1])


if __name__ == "__main__":
    """
        Main script
    """
    parser = argparse.ArgumentParser(description='Print record of a player.')
    parser.add_argument('input_player', help='Handle of a player in the database', type=str)
    parser.add_argument('--recompile', dest='recompile', action='store_const',
                        const=True, default=False,
                        help='Re-compile match archive')

    args = parser.parse_args()

    if args.recompile:
        print("Re-compiling match archive.")
        aggregate_tournament_csv()

    input_plyr = args.input_player
    get_player_record(input_plyr)
