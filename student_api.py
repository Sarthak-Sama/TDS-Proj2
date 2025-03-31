import sys
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Read command-line arguments
csv_path = sys.argv[1]
port = int(sys.argv[2])

# Load CSV data
try:
    students_df = pd.read_csv(csv_path)
except Exception as e:
    print(f"Error loading CSV: {e}")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(title="Student Data API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Data API", "endpoints": ["/api"]}

@app.get("/api")
def get_students(class_: List[str] = Query(None, alias="class")):
    """
    Fetch student data from the CSV.
    """
    filtered_df = students_df[students_df["class"].isin(class_)] if class_ else students_df
    return {"students": filtered_df.to_dict(orient="records")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
