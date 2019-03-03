
global player1_name, player2_name, tourney_name, draw_size, surface, best_of, player1_hand, \
    player2_hand, player1_rank, player2_rank, player1_seed, player2_seed

global winner, score, time, player1_ace, player1_df, player1_svpt, player1_1stIn, player1_1stWon, \
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
    global player1_name, player2_name, winner, score, time, player1_ace, player1_df, player1_svpt, \
        player1_1stIn, player1_1stWon, player1_2ndWon, player1_SvGms, player1_bpSaved, \
        player1_bpFaced, player2_ace, player2_df, player2_svpt, player2_1stIn, player2_1stWon, \
        player2_2ndWon, player2_SvGms, player2_bpSaved, player2_bpFaced
    winner = player1_name
    score = "6-4 6-5"
    time = "118.0"
    player1_ace = "3"
    player1_df = "1"
    player1_svpt = "5"
    player1_1stIn = "0.56"
    player1_1stWon = "0.66"
    player1_2ndWon = "0.23"
    player1_SvGms = "4"
    player1_bpSaved = "4"
    player1_bpFaced = "7"
    player2_ace = "1"
    player2_df = "4"
    player2_svpt = "2"
    player2_1stIn = "0.44"
    player2_1stWon = "0.34"
    player2_2ndWon = "0.14"
    player2_SvGms = "3"
    player2_bpSaved = "2"
    player2_bpFaced = "5"

    return player1_name, player2_name, winner, score, time, player1_ace, player1_df, player1_svpt, \
           player1_1stIn, player1_1stWon, player1_2ndWon, player1_SvGms, player1_bpSaved, \
           player1_bpFaced, player2_ace, player2_df, player2_svpt, player2_1stIn, player2_1stWon, \
           player2_2ndWon, player2_SvGms, player2_bpSaved, player2_bpFaced


def call_model_predict():
    return