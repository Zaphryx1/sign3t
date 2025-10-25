# Supabase Setup Guide for Sign3T

This guide will help you set up Supabase for persistent database storage and vector search capabilities.

## Quick Setup

### Option 1: Use Supabase (Recommended)

1. **Create Supabase Account**
   - Go to [https://supabase.com](https://supabase.com)
   - Sign up for a free account
   - Create a new project

2. **Get Your Credentials**
   - Go to Settings > API in your Supabase dashboard
   - Copy your Project URL and API keys

3. **Create Environment File**
   ```bash
   # Create .env file in the project root
   touch .env
   echo "SUPABASE_URL=YOUR_SUPABASE_URL" >> .env
   echo "SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY" >> .env
   echo "SUPABASE_SERVICE_ROLE_KEY=YOUR_SUPABASE_SERVICE_ROLE_KEY" >> .env
   ```
   - Replace `YOUR_SUPABASE_URL`, `YOUR_SUPABASE_ANON_KEY`, `YOUR_SUPABASE_SERVICE_ROLE_KEY` with your actual credentials.

4. **Enable pgvector Extension**
   - In your Supabase dashboard, navigate to **Database > Extensions**
   - Search for `pgvector` and enable it.

5. **Run Database Schema**
   - In your Supabase dashboard, navigate to **SQL Editor**
   - Click **"New Query"**
   - Copy the entire content of `supabase_schema.sql` from your project
   - Paste it into the SQL editor and click **"Run"**

6. **Install Dependencies**
   ```bash
   cd /path/to/your/sign3t
   source venv/bin/activate
   pip install -r requirements.txt
   ```

7. **Run Setup Script**
   ```bash
   python setup_supabase.py
   ```
   This script will verify your Supabase connection and table setup.

8. **Run the Application**
   ```bash
   ./run.sh
   ```
   This will start the Streamlit dashboard.

### Option 2: Local Mode (No Supabase)

If you prefer not to use Supabase, the system will run in a "local mode" where data is stored in memory and not persisted. Vector search and historical data features will be limited.

1. **Skip Supabase Setup**
   - Do not create a `.env` file or configure Supabase credentials.

2. **Install Dependencies**
   ```bash
   cd /path/to/your/sign3t
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   ./run.sh
   ```
   The system will detect missing Supabase credentials and operate in local mode.

## Troubleshooting

- **"ModuleNotFoundError: No module named 'supabase'"**: Ensure you have installed dependencies: `pip install -r requirements.txt`
- **"Failed to connect to Supabase"**: Double-check your `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `SUPABASE_SERVICE_ROLE_KEY` in your `.env` file.
- **"Error creating tables" / "column does not exist"**: Ensure you have run the `supabase_schema.sql` script in your Supabase SQL Editor and enabled the `pgvector` extension.
- **"Port 8501 is already in use"**: Another Streamlit app is running. Kill the process or run on a different port: `streamlit run src/dashboard.py --server.port 8502`
- **Ollama not running**: Ensure Ollama is installed (`brew install ollama`) and running (`ollama serve`).

## Project Structure

```
sign3t/
├── src/
│   ├── dashboard.py
│   ├── threat_assessment.py
│   ├── threat_score.py
│   ├── local_ai.py
│   ├── supabase_config.py
│   ├── privacy_compliance.py
│   └── simulation.py
├── data/
├── venv/
├── requirements.txt
├── supabase_schema.sql
├── test_database.py
├── setup_supabase.py
├── run.sh
└── README.md
```
