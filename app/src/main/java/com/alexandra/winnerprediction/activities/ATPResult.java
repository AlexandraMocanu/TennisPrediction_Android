package com.alexandra.winnerprediction.activities;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.alexandra.winnerprediction.R;
import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.google.android.material.bottomnavigation.LabelVisibilityMode;

public class ATPResult extends BaseActivity {

    TextView player1_name;
    TextView player2_name;
    TextView winner;
    TextView score;
    TextView time;
    TextView player1_ace;
    TextView player1_df;
    TextView player1_svpt;
    TextView player1_1stIn;
    TextView player1_1stWon;
    TextView player1_2ndWon;
    TextView player1_SvGms;
    TextView player1_bpSaved;
    TextView player1_bpFaced;
    TextView player2_ace;
    TextView player2_df;
    TextView player2_svpt;
    TextView player2_1stIn;
    TextView player2_1stWon;
    TextView player2_2ndWon;
    TextView player2_SvGms;
    TextView player2_bpSaved;
    TextView player2_bpFaced;
    ImageView player1;
    ImageView player2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.atp_result);

        setListeners();
        mActivity.setText(getActivityName());
        bottomNavigationView.setActivated(false);
        bottomNavigationView.setVisibility(View.INVISIBLE);

        mMyIcon = (ImageView) findViewById(R.id.iconTop);
        mMyIcon.setImageDrawable(getResources().getDrawable(getResourceID("icon_atp_round", "drawable", getBaseContext())));

        player1_name = (TextView) findViewById(R.id.player1_name);
        player2_name = (TextView) findViewById(R.id.player2_name);
        winner = (TextView) findViewById(R.id.winner);
        score = (TextView) findViewById(R.id.score);
        time = (TextView) findViewById(R.id.time);
        player1_ace = (TextView) findViewById(R.id.p1_ace);
        player1_df = (TextView) findViewById(R.id.p1_df);
        player1_svpt = (TextView) findViewById(R.id.p1_svpt);
        player1_1stIn = (TextView) findViewById(R.id.p1_1stIn);
        player1_1stWon = (TextView) findViewById(R.id.p1_1stWon);
        player1_2ndWon = (TextView) findViewById(R.id.p1_2ndWon);
        player1_SvGms = (TextView) findViewById(R.id.p1_SvGms);
        player1_bpSaved = (TextView) findViewById(R.id.p1_bpSaved);
        player1_bpFaced = (TextView) findViewById(R.id.p1_bpFaced);
        player2_ace = (TextView) findViewById(R.id.p2_ace);
        player2_df = (TextView) findViewById(R.id.p2_df);
        player2_svpt = (TextView) findViewById(R.id.p2_svpt);
        player2_1stIn = (TextView) findViewById(R.id.p2_1stIn);
        player2_1stWon = (TextView) findViewById(R.id.p2_1stWon);
        player2_2ndWon = (TextView) findViewById(R.id.p2_2ndWon);
        player2_SvGms = (TextView) findViewById(R.id.p2_SvGms);
        player2_bpSaved = (TextView) findViewById(R.id.p2_bpSaved);
        player2_bpFaced = (TextView) findViewById(R.id.p2_bpFaced);

        player1 = (ImageView) findViewById(R.id.player1);
        player1.setImageDrawable(getResources().getDrawable(getResourceID("atp_player_1", "drawable", getBaseContext())));
        player2 = (ImageView) findViewById(R.id.player2);
        player2.setImageDrawable(getResources().getDrawable(getResourceID("atp_player_2", "drawable", getBaseContext())));

        getResults();

    }

    private void getResults() {
        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this.getBaseContext()));
        }

        Python python_instance = Python.getInstance();
        PyObject test_module = python_instance.getModule("predict_p/predict");
        PyObject get_labels = test_module.callAttr("get_labels");

//        player1_name, player2_name, winner, loser, score, time, player1_ace, player1_df, player1_svpt, \
//        player1_1stIn, player1_1stWon, player1_2ndWon, player1_SvGms, player1_bpSaved, \
//        player1_bpFaced, player2_ace, player2_df, player2_svpt, player2_1stIn, player2_1stWon, \
//        player2_2ndWon, player2_SvGms, player2_bpSaved, player2_bpFaced

        if (get_labels.asList().get(0).toString().compareTo(get_labels.asList().get(2).toString()) == 0){
            player1_name.setText(get_labels.asList().get(0).toString() + " (winner)");
            player2_name.setText(get_labels.asList().get(1).toString() + " (loser)");
        }else{
            player1_name.setText(get_labels.asList().get(0).toString() + " (loser)");
            player2_name.setText(get_labels.asList().get(1).toString() + " (winner)");
        }

        winner.setText(get_labels.asList().get(2).toString());
        score.setText(get_labels.asList().get(3).toString());
        time.setText(get_labels.asList().get(4).toString());
        player1_ace.setText(get_labels.asList().get(5).toString());
        player1_df.setText(get_labels.asList().get(6).toString());
        player1_svpt.setText(get_labels.asList().get(7).toString());
        player1_1stIn.setText(get_labels.asList().get(8).toString());
        player1_1stWon.setText(get_labels.asList().get(9).toString());
        player1_2ndWon.setText(get_labels.asList().get(10).toString());
        player1_SvGms.setText(get_labels.asList().get(11).toString());
        player1_bpSaved.setText(get_labels.asList().get(12).toString());
        player1_bpFaced.setText(get_labels.asList().get(13).toString());
        player2_ace.setText(get_labels.asList().get(14).toString());
        player2_df.setText(get_labels.asList().get(15).toString());
        player2_svpt.setText(get_labels.asList().get(16).toString());
        player2_1stIn.setText(get_labels.asList().get(17).toString());
        player2_1stWon.setText(get_labels.asList().get(18).toString());
        player2_2ndWon.setText(get_labels.asList().get(19).toString());
        player2_SvGms.setText(get_labels.asList().get(20).toString());
        player2_bpSaved.setText(get_labels.asList().get(21).toString());
        player2_bpFaced.setText(get_labels.asList().get(22).toString());
    }

    @Override
    public String getActivityName() {
        return "ATP Match Prediction Results";
    }
}
