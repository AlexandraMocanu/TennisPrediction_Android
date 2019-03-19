package com.alexandra.winnerprediction.activities;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import fr.castorflex.android.circularprogressbar.CircularProgressBar;
import fr.castorflex.android.circularprogressbar.CircularProgressDrawable;

import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;

import com.alexandra.winnerprediction.R;
import com.alexandra.winnerprediction.customviews.MontserratTextView;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.bottomnavigation.LabelVisibilityMode;


abstract public class BaseActivity extends AppCompatActivity implements
        BottomNavigationView.OnNavigationItemSelectedListener {

    ProgressBar progressBar;

    protected BottomNavigationView bottomNavigationView;
    protected ImageView mMyIcon;
    protected ImageButton mBackButton;
    protected MontserratTextView mActivity;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_base);

        setListeners();

    }

    protected void setListeners() {

        bottomNavigationView = (BottomNavigationView)
                findViewById(R.id.bottom_bar);
        bottomNavigationView.setLabelVisibilityMode(LabelVisibilityMode.LABEL_VISIBILITY_SELECTED);
        bottomNavigationView.setOnNavigationItemSelectedListener(this);

        mMyIcon = (ImageView) findViewById(R.id.iconTop);

        mBackButton = (ImageButton) findViewById(R.id.back_button);
        mBackButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

        mActivity = (MontserratTextView) findViewById(R.id.titleAct);

        progressBar = (ProgressBar) findViewById(R.id.progressBar);
        progressBar.setEnabled(true);
        progressBar.setAlpha(1);
        progressBar.setActivated(true);
        progressBar.setVisibility(View.GONE);

    }

    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        boolean result = BaseActivity.this.onOptionsItemSelected(item);
//                        bottomNavigationView.setSelectedItemId(item.getItemId());
        return result;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.wta) {
            if (!(this instanceof WTAPrediction)) {
                Intent newIntent = new Intent(this, WTAPrediction.class);
//                newIntent.setFlags(FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(newIntent);
            }
        }
        if (id == R.id.atp) {
            if (!(this instanceof ATPPrediction)) {
                Intent newIntent = new Intent(this, ATPPrediction.class);
//                newIntent.setFlags(FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(newIntent);
            }
        }

        return super.onOptionsItemSelected(item);
    }

    abstract public String getActivityName();

    public final static int getResourceID(final String resName, final String resType, final Context ctx) {
        final int ResourceID = ctx.getResources().getIdentifier(
                resName, resType, ctx.getApplicationInfo().packageName);
        if (ResourceID == 0) {
            throw new IllegalArgumentException("No resource string found with name " + resName);
        } else {
            return ResourceID;
        }
    }

    protected void startProgressBar(){
        progressBar.setEnabled(true);
        progressBar.setAlpha(1);
        progressBar.setActivated(true);
        progressBar.setVisibility(View.VISIBLE);
    }

    protected void stopProgressBar(){
        progressBar.setActivated(false);
        progressBar.setAlpha(0);
        progressBar.setEnabled(false);
        progressBar.setVisibility(View.GONE);
    }
}
