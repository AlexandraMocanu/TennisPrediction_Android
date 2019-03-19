package com.alexandra.winnerprediction.activities;

import android.app.Activity;
import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
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

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import androidx.constraintlayout.widget.ConstraintLayout;

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

        List<String> tourney_list = get_tournaments();
        tournament = (Spinner) findViewById(R.id.tourney);
        ArrayAdapter<String> tournament_adapter = new ArrayAdapter<String>(this,
                R.layout.spinner_item, tourney_list);
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
                predict.setPressed(true);
                setView();
                call_python();
                Intent newIntent = new Intent(getBaseContext(), WTAResult.class);
                startActivity(newIntent);
            }
        });
    }

    private List<String> get_tournaments(){
        ArrayList<String> tourneys = new ArrayList<>();
        String json = null;

        try {
            InputStream is = getAssets().open("tourneys_wta.json");
            int size = is.available();
            byte[] buffer = new byte[size];
            is.read(buffer);
            is.close();
            json = new String(buffer, "UTF-8");
        } catch (IOException ex) {
            ex.printStackTrace();
            return null;
        }

        try {
            JSONArray tourneys_j = new JSONArray(json);
            for (int i = 0; i < tourneys_j.length(); i++){
                JSONObject t = tourneys_j.getJSONObject(i);
                tourneys.add(t.getString("tourney_name"));
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

        tourneys.sort(new Comparator<String>() {
            @Override
            public int compare(String o1, String o2) {
                return o1.compareTo(o2);
            }
        });
        return  tourneys;
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
        PyObject test_module = python_instance.getModule("predict_p/predict");
        PyObject set_features = test_module.callAttr("set_features", "WTA",
                                                            n1, n2,
                                                            tour, draw, surf, best,
                                                            p1_hand, p2_hand, p1_rank, p2_rank, p1_seed, p2_seed);
    }

    private void setView(){
        startProgressBar();
        ConstraintLayout layout = findViewById(R.id.layout_wta);
        Drawable forg = new ColorDrawable(getResources().getColor(R.color.backgroundLight));
        forg.setAlpha(175);
        layout.setForeground(forg);
    }

    @Override
    public String getActivityName() {
        return "Predict WTA match";
    }
}
