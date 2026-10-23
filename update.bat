@echo off
echo ======================================
echo  ATP Betting Pipeline Update Script
echo ======================================

echo [1/4] Generating features from data/raw/...
.venv\Scripts\python src\tennis_atp_pipeline\build_features.py

echo [2/4] Training the final logistic regression model...
.venv\Scripts\python src\tennis_atp_pipeline\train_final_model.py

echo [3/4] Exporting current player Elos to current_elos.csv...
.venv\Scripts\python src\tennis_atp_pipeline\export_current_elos.py

echo ======================================
echo  Update Complete!
echo  
echo  You can now run predictions using:
echo    .venv\Scripts\python predict.py --p1 "Novak Djokovic" --p2 "Carlos Alcaraz" --surface Hard --odds1 1.95 --odds2 1.85
echo ======================================
pause
