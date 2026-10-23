# ATP Tennis Predictor: Integration & Maintenance Guide

## 1. What It Does
This system calculates the exact mathematical win probabilities for ATP tennis matches. It compares these probabilities to bookmaker odds to find profitable bets and recommends wager sizes using the Kelly Criterion.

## 2. The Model
We use a **Logistic Regression** model because it provides perfectly calibrated percentages (crucial for betting) and runs extremely fast. It analyzes 19 pre-match data points including surface-specific Elo ratings, age, rank, and fatigue.

## 3. How to Update the Data
When new matches are played, you can update the system in two steps:
1. Download the latest `atp_matches_202X.csv` and `atp_rankings_current.csv` from Jeff Sackmann's GitHub and place them in the `tennis_atp/` folder.
2. Open your terminal and run:
   ```bash
   ./update.sh
   ```
This script updates all player Elos, retrains the model on the full historical dataset for maximum accuracy, and prepares the system for new predictions.

## 4. Integration Guide
To use these predictions inside a web or mobile app, run the Python engine as a local API.

1. **Start the API:** Run `.venv/bin/python gui_server.py` on your server.
2. **Get Predictions:** Send a `POST` request from your app to `http://127.0.0.1:8080/api/predict`.

**Request JSON:**
```json
{
    "p1": "Novak Djokovic",
    "p2": "Carlos Alcaraz",
    "surface": "Hard",
    "odds1": 1.95,
    "odds2": 1.85
}
```

**Response JSON:**
```json
{
    "player1": "Novak Djokovic",
    "player2": "Carlos Alcaraz",
    "surface": "Hard",
    "prob1": 0.246,
    "prob2": 0.754,
    "fair_odds1": 4.06,
    "fair_odds2": 1.33,
    "warnings": [],
    "betting_analysis": {
        "edge_player": "Carlos Alcaraz",
        "ev": 0.394,
        "kelly_fraction": 0.1159
    }
}
```
You can then render these probabilities and recommended bets directly in your own app's UI!
