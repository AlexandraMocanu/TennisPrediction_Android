package com.alexandra.winnerprediction.activities;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.alexandra.winnerprediction.R;
import com.alexandra.winnerprediction.activities.BaseActivity;
import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.google.android.material.bottomnavigation.LabelVisibilityMode;

public class MainActivity extends BaseActivity {

    EditText name;
    EditText surname;
    TextView output;
    Button predict;

    Button wta_match;
    Button atp_match;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        setListeners();
        mActivity.setText(getActivityName());
        bottomNavigationView.setActivated(false);
        bottomNavigationView.setVisibility(View.INVISIBLE);
        mMyIcon.setActivated(false);
        mMyIcon.setVisibility(View.INVISIBLE);
        mBackButton.setActivated(false);
        mBackButton.setVisibility(View.INVISIBLE);

        wta_match = (Button) findViewById(R.id.wta_match);
        wta_match.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent newIntent = new Intent(getBaseContext(), WTAPrediction.class);
                startActivity(newIntent);
            }
        });

        atp_match = (Button) findViewById(R.id.atp_match);
        atp_match.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent newIntent = new Intent(getBaseContext(), ATPPrediction.class);
                startActivity(newIntent);
            }
        });

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        return super.onOptionsItemSelected(item);
    }

    @Override
    public String getActivityName() {
        return "Tennis Prediction";
    }
}
