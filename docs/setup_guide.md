# Setup Guide for ATP Predictor

## Prerequisites
- **Python 3.10+** installed. You can download it from [python.org](https://www.python.org/downloads/).
  - *Windows users:* Ensure you check the "Add Python to PATH" option during installation.

## Initial Setup

1. Open your terminal (Mac) or command prompt (Windows).
2. Navigate to the `tennis_atp` project directory:
   ```bash
   cd path/to/tennis_atp
   ```
3. Create a virtual environment and install the required dependencies:

   **For Windows:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e .
   ```

   **For Mac/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

## Running the Application

Whenever you want to use the application, open your terminal in the project directory and run the server.

**For Windows:**
```cmd
.venv\Scripts\activate
python gui_server.py
```

**For Mac/Linux:**
```bash
source .venv/bin/activate
python3 gui_server.py
```

Once the server is running, open your web browser and navigate to:
**[http://localhost:8000/gui](http://localhost:8000/gui)**

## Routine Maintenance

To maintain prediction accuracy, the data should be updated periodically:

1. Download the latest `atp_matches_202X.csv` and `atp_rankings_current.csv` files.
2. Replace the existing files in the root `tennis_atp` folder.
3. Open your terminal in the project directory and run the update script to refresh features and retrain the model:

   **For Mac/Linux:**
   ```bash
   ./update.sh
   ```

   **For Windows:**
   ```cmd
   update.bat
   ```
