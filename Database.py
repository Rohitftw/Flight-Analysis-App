import pandas as pd
from sqlalchemy import create_engine

# CSV read
df = pd.read_csv(r"flights_cleaned - flights_cleaned.csv")

# MySQL connection
engine = create_engine("mysql+pymysql://<username>:<password>@localhost/<Database>")

# CSV to MySQL
df.to_sql("<name>", con=engine, if_exists='replace', index=False)