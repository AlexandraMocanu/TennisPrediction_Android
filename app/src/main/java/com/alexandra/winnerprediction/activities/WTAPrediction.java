package com.alexandra.winnerprediction.activities;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;

import com.alexandra.winnerprediction.R;
import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.google.android.material.bottomnavigation.LabelVisibilityMode;

public class WTAPrediction extends BaseActivity {

    Spinner tournament;
    Spinner player1_hand;
    Spinner player2_hand;
    Spinner surface;
    Spinner best_of;
    Spinner draw_size;
    EditText player1_name;
    EditText player2_name;
    EditText player1_rank;
    EditText player2_rank;
    EditText player1_seed;
    EditText player2_seed;
    Button predict;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.wta_prediction);

        setListeners();
        mActivity.setText(getActivityName());
        bottomNavigationView.setLabelVisibilityMode(LabelVisibilityMode.LABEL_VISIBILITY_SELECTED);
        bottomNavigationView.getMenu().setGroupCheckable(0, true, true);
        bottomNavigationView.getMenu().findItem(R.id.wta).setChecked(true);
//        bottomNavigationView.getMenu().findItem(R.id.wta).setIcon(getResources().getDrawable(getResourceID("ic_svg_ball_blue", "drawable", getBaseContext())));
//        bottomNavigationView.getMenu().findItem(R.id.atp).setIcon(getResources().getDrawable(getResourceID("ic_svg_ball_grey", "drawable", getBaseContext())));
        mMyIcon = (ImageView) findViewById(R.id.iconTop);
        mMyIcon.setImageDrawable(getResources().getDrawable(getResourceID("icon_wta_round", "drawable", getBaseContext())));

        tournament = (Spinner) findViewById(R.id.tourney);
        ArrayAdapter<CharSequence> tournament_adapter = ArrayAdapter.createFromResource(this,
                R.array.tourney_wta_array, R.layout.spinner_item);
        tournament_adapter.setDropDownViewResource(R.layout.spinner_item);
        tournament.setAdapter(tournament_adapter);

        player1_hand = (Spinner) findViewById(R.id.player1_hand_s);
        ArrayAdapter<CharSequence> player1_hand_adapter = ArrayAdapter.createFromResource(this,
                R.array.hand, R.layout.spinner_item);
        player1_hand_adapter.setDropDownViewResource(R.layout.spinner_item);
        player1_hand.setAdapter(player1_hand_adapter);

        player2_hand = (Spinner) findViewById(R.id.player2_hand_s);
        ArrayAdapter<CharSequence> player2_hand_adapter = ArrayAdapter.createFromResource(this,
                R.array.hand, R.layout.spinner_item);
        player2_hand_adapter.setDropDownViewResource(R.layout.spinner_item);
        player2_hand.setAdapter(player2_hand_adapter);

        surface = (Spinner) findViewById(R.id.surface_s);
        ArrayAdapter<CharSequence> surface_adapter = ArrayAdapter.createFromResource(this,
                R.array.surface, R.layout.spinner_item);
        surface_adapter.setDropDownViewResource(R.layout.spinner_item);
        surface.setAdapter(surface_adapter);

        best_of = (Spinner) findViewById(R.id.best_of_s);
        ArrayAdapter<CharSequence> best_of_adapter = ArrayAdapter.createFromResource(this,
                R.array.best_of, R.layout.spinner_item);
        best_of_adapter.setDropDownViewResource(R.layout.spinner_item);
        best_of.setAdapter(best_of_adapter);

        draw_size = (Spinner) findViewById(R.id.draw_size_s);
        ArrayAdapter<CharSequence> draw_size_adapter = ArrayAdapter.createFromResource(this,
                R.array.draw_size, R.layout.spinner_item);
        draw_size_adapter.setDropDownViewResource(R.layout.spinner_item);
        draw_size.setAdapter(draw_size_adapter);

        player1_name = (EditText) findViewById(R.id.player1_in);
        player2_name = (EditText) findViewById(R.id.player2_in);
        player1_rank = (EditText) findViewById(R.id.player1_rank_r);
        player2_rank = (EditText) findViewById(R.id.player2_rank_r);
        player1_seed = (EditText) findViewById(R.id.player1_seed_s);
        player2_seed = (EditText) findViewById(R.id.player2_seed_s);

        predict = (Button) findViewById(R.id.predict);

        predict.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                call_python();
                Intent newIntent = new Intent(getBaseContext(), WTAResult.class);
                startActivity(newIntent);
            }
        });
    }

    private void call_python(){
        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this.getBaseContext()));
        }

        String n1 = player1_name.getText().toString();
        String n2 = player2_name.getText().toString();
        String tour = tournament.getSelectedItem().toString();
        String draw = draw_size.getSelectedItem().toString();
        String surf = surface.getSelectedItem().toString();
        String best = best_of.getSelectedItem().toString();
        String p1_hand = player1_hand.getSelectedItem().toString();
        String p2_hand = player2_hand.getSelectedItem().toString();
        String p1_rank = player1_rank.getText().toString();
        String p2_rank = player2_rank.getText().toString();
        String p1_seed = player1_seed.getText().toString();
        String p2_seed = player2_seed.getText().toString();

        Python python_instance = Python.getInstance();
        PyObject test_module = python_instance.getModule("test");
        PyObject set_features = test_module.callAttr("set_features",
                                                            n1, n2,
                                                            tour, draw, surf, best,
                                                            p1_hand, p2_hand, p1_rank, p2_rank, p1_seed, p2_seed);
    }

    @Override
    public String getActivityName() {
        return "Predict WTA match";
    }
}
