import os
import keras
import numpy as np
import pandas as pd
from keras.models import load_model

os.environ["KERAS_BACKEND"] = "tensorflow"

import predict_p.models

global player1_name, player2_name, tourney_name, draw_size, surface, best_of, player1_hand, \
    player2_hand, player1_rank, player2_rank, player1_seed, player2_seed

global winner, loser, score, time, player1_ace, player1_df, player1_svpt, player1_1stIn, player1_1stWon, \
    player1_2ndWon, player1_SvGms, player1_bpSaved, player1_bpFaced, player2_ace, player2_df, \
    player2_svpt, player2_1stIn, player2_1stWon, player2_2ndWon, player2_SvGms, player2_bpSaved, \
    player2_bpFaced

def set_features(n1, n2,
                 tour, draw, surf, best,
                 p1_hand, p2_hand, p1_rank, p2_rank, p1_seed, p2_seed):
    global player1_name, player2_name, tourney_name, draw_size, surface, best_of, \
        player1_hand, player2_hand, player1_rank, player2_rank, player1_seed, player2_seed
    player1_name = n1
    player2_name = n2
    tourney_name = tour
    draw_size = draw
    surface = surf
    best_of = best
    player1_hand = p1_hand
    player2_hand = p2_hand
    player1_rank = p1_rank
    player2_rank = p2_rank
    player1_seed = p1_seed
    player2_seed = p2_seed

    call_model_predict()

def get_labels():
    global player1_name, player2_name, winner, loser, score, time, player1_ace, player1_df, player1_svpt, \
        player1_1stIn, player1_1stWon, player1_2ndWon, player1_SvGms, player1_bpSaved, \
        player1_bpFaced, player2_ace, player2_df, player2_svpt, player2_1stIn, player2_1stWon, \
        player2_2ndWon, player2_SvGms, player2_bpSaved, player2_bpFaced
    # winner = player1_name
    # score = "6-4 6-5"
    # time = "118.0"
    # player1_ace = "3"
    # player1_df = "1"
    # player1_svpt = "5"
    # player1_1stIn = "0.56"
    # player1_1stWon = "0.66"
    # player1_2ndWon = "0.23"
    # player1_SvGms = "4"
    # player1_bpSaved = "4"
    # player1_bpFaced = "7"
    # player2_ace = "1"
    # player2_df = "4"
    # player2_svpt = "2"
    # player2_1stIn = "0.44"
    # player2_1stWon = "0.34"
    # player2_2ndWon = "0.14"
    # player2_SvGms = "3"
    # player2_bpSaved = "2"
    # player2_bpFaced = "5"

    # print(__name__)
    # print(os.path.dirname(os.path.abspath(__file__)))

    # if os.path.exists(os.path.join(os.path.dirname(predict_p.models.__file__), "best_model_atp.h5")):
    #     print("====== ")

    model = load_model(os.path.join(os.path.dirname(predict_p.models.__file__), "best_model_atp.h5"))

    ##
        # year	tourney_id	player2_id	player1_id
        # player2_seed	player2_ht	player2_age	player2_rank
        # player1_seed	player1_ht	player1_age	player1_rank
        # draw_size_0	draw_size_10	draw_size_12	draw_size_128
        # draw_size_16	draw_size_24	draw_size_28	draw_size_32
        # draw_size_4	draw_size_48	draw_size_56	draw_size_6
        # draw_size_64	draw_size_7	draw_size_8	draw_size_9	draw_size_96
        # surface_0	surface_Carpet	surface_Clay	surface_Grass	surface_Hard
        # surface_None	player1_hand_0	player1_hand_L	player1_hand_R	player1_hand_U
        # player2_hand_0	player2_hand_L	player2_hand_R	player2_hand_U	best_of_3	best_of_5
            # 0.5799999999999983	0.09884954275759417 	0.026628559800956353	0.019830054493396143
            # 0.19999999999999998	0.8798076923076924	    0.3444304564734655	    0.06531531531531531
            # 0.05714285714285714	0.8557692307692308	    0.38180006930058824	    0.04873726185201595
            # 0.0  0.0	0.0	0.0	0.0	0.0	0.0	1.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	1.0	0.0	0.0	0.0
            # 0.0	0.0	0.0	1.0	0.0	0.0	0.0	1.0	0.0	1.0	0.0

    features_p = np.array([0.5799999999999983, 0.09884954275759417, 0.026628559800956353,
                         0.019830054493396143, 0.19999999999999998, 0.8798076923076924,
                         0.3444304564734655, 0.06531531531531531, 0.05714285714285714,
                         0.8557692307692308, 0.38180006930058824, 0.04873726185201595,
                         0.0, 0.0, 	0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 	0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
                         0.0, 1.0, 0.0])
    features_p = np.expand_dims(features_p, axis=0)
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


def call_model_predict():
    return