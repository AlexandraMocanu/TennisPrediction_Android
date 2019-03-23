import os
import datetime
import difflib
import pickle
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
    # print(player1_hand, player2_hand, player1_rank, player2_rank, player1_seed, player2_seed)


def set_tourney(file, tour):
    tourneys = pd.read_csv(os.path.join(os.path.dirname(predict_p.models.__file__), file))
    tourney_row = tourneys.loc[tourneys['tourney_name'] == tour]
    global tourney_name, tourney_id
    tourney_name = tour
    tourney_id = tourney_row['id'].values[0]
    # print("==== Tournament: ", tourney_name, tourney_id)


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
    player1_id = p1_row['id'].values[0]
    player2_id = p2_row['id'].values[0]
    # print("==== Player 1: ", player1_name, player1_id)
    # print("==== Player 2: ", player2_name, player2_id)


def get_age(name, file):
    players = pd.read_csv(os.path.join(os.path.dirname(predict_p.models.__file__), file))
    players_names = players[['name']]
    p1 = difflib.get_close_matches(name, players_names['name'].values.tolist(), n=1)
    p1_row = players.loc[players['name'] == p1[0]]
    return p1_row['age'].values[0]


def get_height(name, file):
    players = pd.read_csv(os.path.join(os.path.dirname(predict_p.models.__file__), file))
    players_names = players[['name']]
    p1 = difflib.get_close_matches(name, players_names['name'].values.tolist(), n=1)
    p1_row = players.loc[players['name'] == p1[0]]
    return p1_row['height'].values[0]


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
        return 0
    else: return int(rank)


def set_seed(seed):
    if not seed or seed == "":
        return 0
    else: return int(seed)


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


def get_drawsize_wta(drawsize):
    # # draw_size
    # 'draw_size_12', 'draw_size_128', 'draw_size_15', 'draw_size_16', 'draw_size_28', 'draw_size_30',
    # 'draw_size_31', 'draw_size_32', 'draw_size_4', 'draw_size_48', 'draw_size_54', 'draw_size_55',
    # 'draw_size_56', 'draw_size_60', 'draw_size_64', 'draw_size_8', 'draw_size_96',
    sizes = [12, 128, 15, 16, 28, 30, 31, 32, 4, 48, 54, 55, 56, 60, 64, 8, 96]
    draw_size_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if drawsize in sizes:
        idx = sizes.index(drawsize)
        draw_size_p[idx] = 1
    # print(draw_size_p)
    return draw_size_p


def getMinMaxScaler():
    with open(os.path.join(os.path.dirname(predict_p.models.__file__), 'MinMaxScaler'), 'rb') as f:
        rs = pickle.load(f)
    return rs

def get_features_numpy_array_wta():
    ##
        # year	tourney_id	player2_id	player1_id
        #  player2_seed	    player2_ht	    player2_age	    player2_rank
        #  player1_seed	    player1_ht	    player1_age 	player1_rank
        #  draw_size
        #  draw_size_12	    draw_size_128	draw_size_15	draw_size_16
        #  draw_size_28	    draw_size_30	draw_size_31	draw_size_32
        #  draw_size_4	    draw_size_48	draw_size_54	draw_size_55
        #  draw_size_56	    draw_size_60	draw_size_64	draw_size_8     draw_size_96
        #  surface
        #  surface_0    surface_Carpet  surface_Clay	surface_Grass	surface_Hard
        #  player1_hand
        #  player1_hand_0	player1_hand_L	player1_hand_R	player1_hand_U
        #  player2_hand
        #  player2_hand_0	player2_hand_L	player2_hand_R	player2_hand_U
        #  best_of
        #  best_of_3	best_of_5

    global year, player1_name, player2_name, player1_id, player2_id, tourney_name, tourney_id, \
        player2_ht, player2_age, player1_ht, player1_age, \
        draw_size, surface, best_of, player1_hand, player2_hand, \
        player1_rank, player2_rank, player1_seed, player2_seed

    features_list = []
    features_list.append(year)
    features_list.append(tourney_id)
    features_list.append(player2_id)
    features_list.append(player1_id)

    features_list.append(player2_seed)
    features_list.append(player2_ht)
    features_list.append(player2_age)
    features_list.append(player2_rank)

    features_list.append(player1_seed)
    features_list.append(player1_ht)
    features_list.append(player1_age)
    features_list.append(player1_rank)

    drawsize_p = get_drawsize_wta(draw_size)
    features_list.extend(drawsize_p)

    surface_p = get_surface(surface)
    features_list.extend(surface_p)

    p1_hand = get_hand(player1_hand)
    features_list.extend(p1_hand)
    p2_hand = get_hand(player2_hand)
    features_list.extend(p2_hand)

    bestof_p = get_bestof(best_of)
    features_list.extend(bestof_p)

    features_np = np.asarray(features_list)
    features_np = np.nan_to_num(features_np)
    features_np = np.reshape(features_np, (1, -1))
    rs = getMinMaxScaler()
    features_np = rs.transform(features_np)

    return features_np


def get_labels_wta():
    global player1_name, player2_name, winner, loser, score, time, player1_ace, player1_df, player1_svpt, \
        player1_1stIn, player1_1stWon, player1_2ndWon, player1_SvGms, player1_bpSaved, \
        player1_bpFaced, player2_ace, player2_df, player2_svpt, player2_1stIn, player2_1stWon, \
        player2_2ndWon, player2_SvGms, player2_bpSaved, player2_bpFaced

    model_file = "best_model_wta.h5"

    model = load_model(os.path.join(os.path.dirname(predict_p.models.__file__), model_file))

    features_p = get_features_numpy_array_wta()

    # features_p = np.expand_dims(features_p, axis=0)
    # f_p = [0.3333333333333428, 0.020134228187919462, 0.06530294932218972, 9.77278279989946e-05, 0.15151515151515152,
    #        0.0, 0.1895701198016862, 0.003779289493575208, 0.029411764705882353, 0.8835978835978835,
    #        0.5265882617754333, 	0.0006747638326585695, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
    #        1.0, 0.0, 1.0, 0.0]
    # f_p = np.expand_dims(f_p, axis=0)

    results_np = model.predict(features_p)
    results_np = np.rint(results_np)
    results = pd.DataFrame(data=results_np,
                          columns=['winner',
                                   'set1_w', 'set1_l', 'set2_w', 'set2_l', 'set3_w', 'set3_l', 'set4_w', 'set4_l', 'set5_w', 'set5_l',
                                   't1', 't2', 't3', 't4', 't5', 'minutes', 'player2_ace', 'player2_df', 'player2_svpt', 'player2_1stIn', 'player2_1stWon',
                                   'player2_2ndWon', 'player2_SvGms', 'player2_bpSaved', 'player2_bpFaced', 'player1_ace', 'player1_df',
                                   'player1_svpt', 'player1_1stIn', 'player1_1stWon', 'player1_2ndWon', 'player1_SvGms', 'player1_bpSaved',
                                   'player1_bpFaced'])
    print(results)
    if results.at[0,'winner'] > 0.4:
        winner = player2_name
        loser = player1_name
    else:
        winner = player1_name
        loser = player2_name
    global best_of
    if best_of == 3:
        if int(results.at[0,'set3_w']) > 4:
            score = str(int(results.at[0,'set1_w'])) + '-' + str(int(results.at[0,'set1_l'])) + ' ' \
                    + str(int(results.at[0,'set2_w'])) + '-' + str(int(results.at[0,'set2_l'])) + ' ' \
                    + str(int(results.at[0,'set3_w'])) + '-' + str(int(results.at[0,'set3_l']))
        else:
            score = str(int(results.at[0,'set1_w'])) + '-' + str(int(results.at[0,'set1_l'])) + ' ' \
                    + str(int(results.at[0,'set2_w'])) + '-' + str(int(results.at[0,'set2_l']))
    else:
        if int(results.at[0,'set5_w']) > 4:
            score = str(int(results.at[0,'set1_w'])) + '-' + str(int(results.at[0,'set1_l'])) + ' ' \
                    + str(int(results.at[0,'set2_w'])) + '-' + str(int(results.at[0,'set2_l'])) + ' ' \
                    + str(int(results.at[0,'set3_w'])) + '-' + str(int(results.at[0,'set3_l'])) + ' ' \
                    + str(int(results.at[0,'set4_w'])) + '-' + str(int(results.at[0,'set4_l'])) + ' ' \
                    + str(int(results.at[0,'set5_w'])) + '-' + str(int(results.at[0,'set5_l']))
        else:
            score = str(int(results.at[0,'set1_w'])) + '-' + str(int(results.at[0,'set1_l'])) + ' ' \
                    + str(int(results.at[0,'set2_w'])) + '-' + str(int(results.at[0,'set2_l'])) + ' ' \
                    + str(int(results.at[0,'set3_w'])) + '-' + str(int(results.at[0,'set3_l']))

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


def get_drawsize_atp(drawsize):
    ##
    # 'draw_size_0', 'draw_size_10', 'draw_size_12', 'draw_size_128', 'draw_size_16', 'draw_size_24',
    # 'draw_size_28', 'draw_size_32', 'draw_size_4', 'draw_size_48', 'draw_size_56',
    # 'draw_size_6', 'draw_size_64', 'draw_size_7', 'draw_size_8', 'draw_size_9',
    # 'draw_size_96'
    sizes = [0, 10, 12, 128, 16, 24, 28, 32, 4, 48, 56, 6, 64, 7, 8, 9, 96]
    draw_size_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if drawsize in sizes:
        idx = sizes.index(drawsize)
        draw_size_p[idx] = 1
    # print(draw_size_p)
    return draw_size_p


def get_features_numpy_array_atp():
    ##
        # year	tourney_id	player2_id	player1_id
        # player2_seed	player2_ht	player2_age	 player2_rank
        # player1_seed	player1_ht	player1_age	 player1_rank
        # draw_size_0	draw_size_10	draw_size_12	draw_size_128
        # draw_size_16	draw_size_24	draw_size_28	draw_size_32
        # draw_size_4	draw_size_48	draw_size_56	draw_size_6
        # draw_size_64	draw_size_7	    draw_size_8	    draw_size_9	    draw_size_96
        # surface_0	    surface_Carpet	surface_Clay	surface_Grass	surface_Hard
        # player1_hand_0	player1_hand_L	player1_hand_R	player1_hand_U
        # player2_hand_0	player2_hand_L	player2_hand_R	player2_hand_U
        # best_of_3	best_of_5

    global year, player1_name, player2_name, player1_id, player2_id, tourney_name, tourney_id, \
        player2_ht, player2_age, player1_ht, player1_age, \
        draw_size, surface, best_of, player1_hand, player2_hand, \
        player1_rank, player2_rank, player1_seed, player2_seed

    features_list = []
    features_list.append(year)
    features_list.append(tourney_id)
    features_list.append(player2_id)
    features_list.append(player1_id)

    features_list.append(player2_seed)
    features_list.append(player2_ht)
    features_list.append(player2_age)
    features_list.append(player2_rank)

    features_list.append(player1_seed)
    features_list.append(player1_ht)
    features_list.append(player1_age)
    features_list.append(player1_rank)

    drawsize_p = get_drawsize_atp(draw_size)
    features_list.extend(drawsize_p)

    surface_p = get_surface(surface)
    features_list.extend(surface_p)

    p1_hand = get_hand(player1_hand)
    features_list.extend(p1_hand)
    p2_hand = get_hand(player2_hand)
    features_list.extend(p2_hand)

    bestof_p = get_bestof(best_of)
    features_list.extend(bestof_p)

    features_np = np.asarray(features_list)
    features_np = np.reshape(features_np, (1, -1))
    rs = getMinMaxScaler()
    features_np = rs.transform(features_np)

    return features_np


def get_labels_atp():
    global player1_name, player2_name, winner, loser, score, time, player1_ace, player1_df, player1_svpt, \
        player1_1stIn, player1_1stWon, player1_2ndWon, player1_SvGms, player1_bpSaved, \
        player1_bpFaced, player2_ace, player2_df, player2_svpt, player2_1stIn, player2_1stWon, \
        player2_2ndWon, player2_SvGms, player2_bpSaved, player2_bpFaced

    model_file = "best_model_atp.h5"

    model = load_model(os.path.join(os.path.dirname(predict_p.models.__file__), model_file))

    features_p = get_features_numpy_array_atp()
    results_np = model.predict(features_p)
    results_np = np.rint(results_np)
    results = pd.DataFrame(data=results_np,
                           columns=['winner',
                                    'set1_w', 'set1_l', 'set2_w', 'set2_l', 'set3_w', 'set3_l', 'set4_w', 'set4_l', 'set5_w', 'set5_l',
                                    't1', 't2', 't3', 't4', 't5', 'minutes', 'player2_ace', 'player2_df', 'player2_svpt', 'player2_1stIn', 'player2_1stWon',
                                    'player2_2ndWon', 'player2_SvGms', 'player2_bpSaved', 'player2_bpFaced', 'player1_ace', 'player1_df',
                                    'player1_svpt', 'player1_1stIn', 'player1_1stWon', 'player1_2ndWon', 'player1_SvGms', 'player1_bpSaved',
                                    'player1_bpFaced'])
    print(results)
    if results.at[0,'winner'] > 0.4:
        winner = player2_name
        loser = player1_name
    else:
        winner = player1_name
        loser = player2_name
    global best_of
    if best_of == 3:
        score = str(int(results.at[0,'set1_w'])) + '-' + str(int(results.at[0,'set1_l'])) + ' ' \
                + str(int(results.at[0,'set2_w'])) + '-' + str(int(results.at[0,'set2_l'])) + ' ' \
                + str(int(results.at[0,'set3_w'])) + '-' + str(int(results.at[0,'set3_l']))
    else:
        score = str(int(results.at[0,'set1_w'])) + '-' + str(int(results.at[0,'set1_l'])) + ' ' \
                + str(int(results.at[0,'set2_w'])) + '-' + str(int(results.at[0,'set2_l'])) + ' ' \
                + str(int(results.at[0,'set3_w'])) + '-' + str(int(results.at[0,'set3_l'])) + ' ' \
                + str(int(results.at[0,'set4_w'])) + '-' + str(int(results.at[0,'set4_l'])) + ' ' \
                + str(int(results.at[0,'set5_w'])) + '-' + str(int(results.at[0,'set5_l']))
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

