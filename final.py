import pandas as pd
import numpy as np

path = "./Mammoth Springs Yellowstone.csv"

df = pd.read_csv(path)

df.head()

df.columns

# Find the number of staions (Theres only one)
stations = df["STATION"].unique()
print(stations)

# Check Values
df.info()

df.describe()

# Key missing values TMAX, TMIN, PRCP
cleaned = df.copy()

cleaned.dropna(subset=["TMAX", "TMIN", "PRCP"], inplace=True)
cleaned.drop(columns=["DAPR", "MDPR"], inplace=True)

cleaned.info()

cleaned.describe()

# Build line chart showing the TMAX and TMIN

# Build line chart showing PRCP & SNOW

# Bulid a mixed bar/line plot bar being PRCP/SNOW and line bing Temp

cleaned[["PRCP", "SNOW", "TMAX", "TMIN"]].head()
