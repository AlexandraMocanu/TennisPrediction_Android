import os
import datetime
import difflib
import keras
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

import predict_p.models

global year, player1_name, player2_name, player1_id, player2_id, tourney_name, tourney_id, \
    player2_ht, player2_age, player1_ht, player1_age, \
    draw_size, surface, best_of, player1_hand, player2_hand, \
    player1_rank, player2_rank, player1_seed, player2_seed

global winner, loser, score, time, player1_ace, player1_df, player1_svpt, player1_1stIn, player1_1stWon, \
    player1_2ndWon, player1_SvGms, player1_bpSaved, player1_bpFaced, player2_ace, player2_df, \
    player2_svpt, player2_1stIn, player2_1stWon, player2_2ndWon, player2_SvGms, player2_bpSaved, \
    player2_bpFaced

def set_features(type,
                 n1, n2,
                 tour, draw, surf, best,
                 p1_hand, p2_hand, p1_rank, p2_rank, p1_seed, p2_seed):
    global draw_size, surface, best_of, \
        player1_hand, player2_hand, player1_rank, player2_rank, player1_seed, player2_seed, \
        player1_age, player1_ht, player2_age, player2_ht

    players_file = ""
    tourneys_file = ""
    basicinfo_file = ""
    if "WTA" in type:
        players_file = "wta_players_map.csv"
        tourneys_file = "unique_tourneys_wta.csv"
        basicinfo_file = "wta_players_basicinfo.csv"
    else:
        players_file = "atp_players_map.csv"
        tourneys_file = "unique_tourneys_atp.csv"
        basicinfo_file = "atp_players_basicinfo.csv"

    set_players(players_file, n1, n2)
    player2_age = get_age(player2_name, basicinfo_file)
    player1_age = get_age(player1_name, basicinfo_file)
    player2_ht = get_height(player2_name, basicinfo_file)
    player1_ht = get_height(player1_name, basicinfo_file)
    set_tourney(tourneys_file, tour)
    set_year()

    draw_size = draw
    surface = surf
    best_of = best

    player1_hand = set_hand(p1_hand)
    player2_hand = set_hand(p2_hand)
    player1_rank = set_rank(p1_rank)
    player2_rank = set_rank(p2_rank)
    player1_seed = set_seed(p1_seed)
    player2_seed = set_seed(p2_seed)
    print(player1_hand, player2_hand, player1_rank, player2_rank, player1_seed, player2_seed)


def set_tourney(file, tour):
    tourneys = pd.read_csv(os.path.join(os.path.dirname(predict_p.models.__file__), file))
    tourney_row = tourneys.loc[tourneys['tourney_name'] == tour]
    global tourney_name, tourney_id
    tourney_name = tour
    tourney_id = tourney_row['id']
    # print(tourney_name, tourney_id)


def set_year():
    global year
    now = datetime.datetime.now()
    year = now.year
    # print(year)


def set_players(file, n1, n2):
    global player1_name, player2_name, player1_id, player2_id
    player1_name = n1
    player2_name = n2
    players = pd.read_csv(os.path.join(os.path.dirname(predict_p.models.__file__), file))
    players_names = players[['full_name']]
    # search for first most close match
    p1 = difflib.get_close_matches(player1_name, players_names['full_name'].values.tolist(), n=1)
    p2 = difflib.get_close_matches(player2_name, players_names['full_name'].values.tolist(), n=1)
    # get rows
    p1_row = players.loc[players['full_name'] == p1[0]]
    p2_row = players.loc[players['full_name'] == p2[0]]
    # get ids
    player1_id = p1_row['id']
    player2_id = p2_row['id']
    # print(player1_name, player1_id)
    # print(player2_name, player2_id)


def get_age(name, file):
    players = pd.read_csv(os.path.join(os.path.dirname(predict_p.models.__file__), file))
    players_names = players[['name']]
    p1 = difflib.get_close_matches(name, players_names['name'].values.tolist(), n=1)
    p1_row = players.loc[players['name'] == p1[0]]
    return p1_row['age']


def get_height(name, file):
    players = pd.read_csv(os.path.join(os.path.dirname(predict_p.models.__file__), file))
    players_names = players[['name']]
    p1 = difflib.get_close_matches(name, players_names['name'].values.tolist(), n=1)
    p1_row = players.loc[players['name'] == p1[0]]
    return p1_row['height']


def set_hand(hand):
    if "Left" in hand:
        return "L"
    elif "Right" in hand:
        return "R"
    elif "Both" in hand:
        return "U"
    else: return "0"


def set_rank(rank):
    if not rank or rank == "":
        return -1
    else: return int(rank)


def set_seed(seed):
    if not seed or seed == "":
        return -1
    else: return int(seed)


def get_features_numpy_array():
    ##
        # 'year', 'tourney_id', 'player2_id', 'player1_id',
        # # surface
        # 'surface_0', 'surface_Carpet', 'surface_Clay', 'surface_Grass', 'surface_Hard',
        # # draw_size
        # 'draw_size_12', 'draw_size_128', 'draw_size_15', 'draw_size_16', 'draw_size_28', 'draw_size_30',
        # 'draw_size_31', 'draw_size_32', 'draw_size_4', 'draw_size_48', 'draw_size_54', 'draw_size_55',
        # 'draw_size_56', 'draw_size_60', 'draw_size_64', 'draw_size_8', 'draw_size_96',
        # # best_of
        # 'best_of_3', 'best_of_5'
        # 'player2_seed',
        # # player2_hand
        # 'player2_hand_0', 'player2_hand_L', 'player2_hand_R', 'player2_hand_U',
        # 'player2_ht', 'player2_age', 'player2_rank',
        # 'player1_seed',
        # # player1_hand
        # 'player1_hand_0', 'player1_hand_L', 'player1_hand_R', 'player1_hand_U',
        #  'player1_ht', 'player1_age', 'player1_rank',

    global year, player1_name, player2_name, player1_id, player2_id, tourney_name, tourney_id, \
        player2_ht, player2_age, player1_ht, player1_age, \
        draw_size, surface, best_of, player1_hand, player2_hand, \
        player1_rank, player2_rank, player1_seed, player2_seed

    features_list = []
    features_list.append(year)
    features_list.append(tourney_id)
    features_list.append(player2_id)
    features_list.append(player1_id)
    surface_p = get_surface(surface)
    drawsize_p = get_drawsize(draw_size)
    bestof_p = get_bestof(best_of)
    features_list.extend(surface_p)
    features_list.extend(drawsize_p)
    features_list.extend(bestof_p)
    features_list.append(player2_seed)
    p2_hand = get_hand(player2_hand)
    features_list.extend(p2_hand)
    p2_height = player2_ht
    p2_age = player2_age
    features_list.append(p2_height)
    features_list.append(p2_age)
    features_list.append(player2_rank)
    features_list.append(player1_seed)
    p1_hand = get_hand(player1_hand)
    features_list.extend(p1_hand)
    p1_height = player1_ht
    p1_age = player1_age
    features_list.append(p1_height)
    features_list.append(p1_age)
    features_list.append(player1_rank)

    features_np = np.asarray(features_list)
    rs = MinMaxScaler()
    features_np = np.reshape(features_np, (1, -1))
    features_cont = rs.fit_transform(features_np)

    return features_cont


def get_hand(hand):
    # 'player2_hand_0', 'player2_hand_L', 'player2_hand_R', 'player2_hand_U',
    # 'player1_hand_0', 'player1_hand_L', 'player1_hand_R', 'player1_hand_U',
    if "L" in hand:
        return [0, 1, 0, 0]
    elif "R" in hand:
        return [0, 0, 1, 0]
    elif "U" in hand:
        return [0, 0, 0, 1]
    else: return [1, 0, 0, 0]


def get_bestof(bestof):
    #  'best_of_3', 'best_of_5'
    if "3" in surface:
        return [1, 0]
    elif "5" in surface:
        return [0, 1]
    else: return [0, 0]


def get_surface(surface):
    # 'surface_0', 'surface_Carpet', 'surface_Clay', 'surface_Grass', 'surface_Hard',
    if "Carpet" in surface:
        return [0, 1, 0, 0, 0]
    elif "Clay" in surface:
        return [0, 0, 1, 0, 0]
    elif "Grass" in surface:
        return [0, 0, 0, 1, 0]
    elif "Hard" in surface:
        return [0, 0, 0, 0, 1]
    else:
        return [1, 0, 0, 0, 0]


def get_drawsize(drawsize):
    # # draw_size
    # 'draw_size_12', 'draw_size_128', 'draw_size_15', 'draw_size_16', 'draw_size_28', 'draw_size_30',
    # 'draw_size_31', 'draw_size_32', 'draw_size_4', 'draw_size_48', 'draw_size_54', 'draw_size_55',
    # 'draw_size_56', 'draw_size_60', 'draw_size_64', 'draw_size_8', 'draw_size_96',
    sizes = [12, 128, 15, 16, 28, 30, 31, 32, 4, 48, 54, 55, 56, 60, 64, 8, 96]
    draw_size_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if drawsize in sizes:
        idx = sizes.index(drawsize)
        draw_size_p[idx] = 1
    print(draw_size_p)
    return draw_size_p



def get_labels_wta():
    global player1_name, player2_name, winner, loser, score, time, player1_ace, player1_df, player1_svpt, \
        player1_1stIn, player1_1stWon, player1_2ndWon, player1_SvGms, player1_bpSaved, \
        player1_bpFaced, player2_ace, player2_df, player2_svpt, player2_1stIn, player2_1stWon, \
        player2_2ndWon, player2_SvGms, player2_bpSaved, player2_bpFaced

    model_file = "best_model_wta.h5"

    model = load_model(os.path.join(os.path.dirname(predict_p.models.__file__), model_file))

    features_p = get_features_numpy_array()
    print(features_p)
    # features_p = np.array([0.5799999999999983, 0.09884954275759417, 0.026628559800956353,
    #                      0.019830054493396143, 0.19999999999999998, 0.8798076923076924,
    #                      0.3444304564734655, 0.06531531531531531, 0.05714285714285714,
    #                      0.8557692307692308, 0.38180006930058824, 0.04873726185201595,
    #                      0.0, 0.0, 	0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #                      0.0, 0.0, 	0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
    #                      0.0, 1.0, 0.0])

    # features_p = np.expand_dims(features_p, axis=0)
    results_np = model.predict(features_p)
    results = pd.DataFrame(data=results_np,
                          columns=['winner',
                                   'set1_w', 'set1_l', 'set2_w', 'set2_l', 'set3_w', 'set3_l', 'set4_w', 'set4_l', 'set5_w', 'set5_l',
                                   't1', 't2', 't3', 't4', 't5', 'minutes', 'player2_ace', 'player2_df', 'player2_svpt', 'player2_1stIn', 'player2_1stWon',
                                   'player2_2ndWon', 'player2_SvGms', 'player2_bpSaved', 'player2_bpFaced', 'player1_ace', 'player1_df',
                                   'player1_svpt', 'player1_1stIn', 'player1_1stWon', 'player1_2ndWon', 'player1_SvGms', 'player1_bpSaved',
                                   'player1_bpFaced'])

    if results.at[0,'winner'] == 0:
        winner = player2_name
        loser = player1_name
    else:
        winner = player1_name
        loser = player2_name
    score = str(results.at[0,'set1_w']) + ' - ' + str(results.at[0,'set1_l']) + ' '\
            + str(results.at[0,'set2_w']) + ' - ' + str(results.at[0,'set2_l'])
    time = results.at[0,'minutes']
    player2_ace = results.at[0,'player2_ace']
    player2_df = results.at[0,'player2_df']
    player2_svpt = results.at[0,'player2_svpt']
    player2_1stIn = results.at[0,'player2_1stIn']
    player2_1stWon = results.at[0,'player2_1stWon']
    player2_2ndWon = results.at[0,'player2_2ndWon']
    player2_SvGms = results.at[0,'player2_SvGms']
    player2_bpSaved = results.at[0,'player2_bpSaved']
    player2_bpFaced = results.at[0,'player2_bpFaced']
    player1_ace = results.at[0,'player1_ace']
    player1_df = results.at[0,'player1_df']
    player1_svpt = results.at[0,'player1_svpt']
    player1_1stIn = results.at[0,'player1_1stIn']
    player1_1stWon = results.at[0,'player1_1stWon']
    player1_2ndWon = results.at[0,'player1_2ndWon']
    player1_SvGms = results.at[0,'player1_SvGms']
    player1_bpSaved = results.at[0,'player1_bpSaved']
    player1_bpFaced = results.at[0,'player1_bpFaced']

    ##
    return player1_name, player2_name, winner, loser, score, time, player1_ace, player1_df, player1_svpt, \
           player1_1stIn, player1_1stWon, player1_2ndWon, player1_SvGms, player1_bpSaved, \
           player1_bpFaced, player2_ace, player2_df, player2_svpt, player2_1stIn, player2_1stWon, \
           player2_2ndWon, player2_SvGms, player2_bpSaved, player2_bpFaced

