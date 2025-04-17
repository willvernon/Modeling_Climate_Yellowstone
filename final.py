# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

path = "./data/Mammoth Springs Yellowstone.csv"
df = pd.read_csv(path)
df.head()

# %%
# Find the number of staions (Theres only one)
stations = df["STATION"].unique()
print(stations)

# %% [markdown]
# # Introduction to the Region:
#
# In this i am using Yellowstone Park Mammoth, Wy US as my location of choice. I thought Yellowstone would be a good place to get a wide range of temperature and rain/snow which can show a good amount of data. For the data in Yellowstone it has a great area that gets all kinds of weather being in a sweet spot in the country.
#

# %%
# Key missing values TMAX, TMIN, PRCP
cleaned = df.copy()

cleaned.dropna(subset=["TMAX", "TMIN", "PRCP"], inplace=True)
cleaned.drop(columns=["DAPR", "MDPR"], inplace=True)

cleaned.info()

cleaned.describe()

# %%
cleaned["MONTH"] = pd.to_datetime(cleaned["DATE"]).dt.month
cleaned["YEAR"] = pd.to_datetime(cleaned["DATE"]).dt.year
cleaned["MEAN_TEMP"] = (cleaned["TMAX"] + cleaned["TMIN"]) / 2

# %%
cleaned23 = cleaned[cleaned["YEAR"] == 2023]
cleaned23.head()

# %% [markdown]
# # TMAX and TMIN Temperature
#
# Looking at Temperature the total mean for TMAX is 54 degrees and for TMIN 28 degrees. If we look at the temperature grouped by months for the years of 2023-2024 the hottest month average temperature is July at 83.5 and the coldest average min is January at 10.
#

# %%
grouped = (
    cleaned.groupby("MONTH")[["MEAN_TEMP", "TMAX", "TMIN", "PRCP", "SNOW"]]
    .agg(
        {
            "MEAN_TEMP": "mean",
            "TMAX": "mean",
            "TMIN": "mean",
            "PRCP": "sum",
            "SNOW": "sum",
        }
    )
    .reset_index()
)
grouped

# %% [markdown]
# # PRCP, TMIN, TMAX, TAVG, Combo Plot
#
# Getting to the charts the first one here is a combo plot with Monthly total precipitation and the temperature as a fill_between which shows the max, min, and average for each month. By looking at this you can see the total precipitation actually happens more during the summer months than it does in the spring months with November and December bringing up the rear with the least amount of precipitation and June and Aug being the most amount of precipitation.
#

# %%
# KEEP
# Create plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Data
x = grouped["MONTH"]
y1 = grouped["TMAX"]
y2 = grouped["TMIN"]

# Secondary y-axis for temperatures
ax2 = ax1.twinx()
ax2.fill_between(
    x, y1, y2, alpha=0.5, color="lightcoral", linewidth=0, label="Temp Range"
)
ax2.plot(x, (y1 + y2) / 2, linewidth=2, color="darkred", label="Avg Temp")
ax2.set_ylabel("Temperature (°f)", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Dynamic temperature y-limits
y_min = min(y2.min(), 0) - 5
y_max = y1.max() + 5
ax2.set_ylim(y_min, y_max)

# Bar plot for PRCP
ax1.bar(
    x, grouped["PRCP"] * 25.4, color="skyblue", label="Precipitation (mm)", alpha=0.6
)
ax1.set_xlabel("Month")
ax1.set_ylabel("Precipitation (mm)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.set_ylim(0, (grouped["PRCP"] * 25.4).max())

# Custom x-ticks
ax1.set_xticks(np.arange(1, 13))
ax1.set_xticklabels(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
)

# Title and legend
plt.title("Monthly Total Precipitation and Temperature Range")
fig.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3)

# Grid
ax2.grid(True, alpha=0.3)

# Show plot
plt.tight_layout()
plt.show()

# %% [markdown]
# # Snow Temperature Range
#
# This Chart shows Total Snow and Temperature Range showing February and March being the most and a strong drop off into April.
#

# %%
# KEEP
# Create plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Data
x = grouped["MONTH"]
y1 = grouped["TMAX"]
y2 = grouped["TMIN"]

# Secondary y-axis for temperatures
ax2 = ax1.twinx()
ax2.fill_between(
    x, y1, y2, alpha=0.5, color="lightcoral", linewidth=0, label="Temp Range"
)
ax2.plot(x, (y1 + y2) / 2, linewidth=2, color="darkred", label="Avg Temp")
ax2.set_ylabel("Temperature (°f)", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Dynamic temperature y-limits
y_min = min(y2.min(), 0) - 5
y_max = y1.max() + 5
ax2.set_ylim(y_min, y_max)

# Bar plot for PRCP
ax1.bar(x, grouped["SNOW"], color="skyblue", label="Snow (in)", alpha=0.6)
ax1.set_xlabel("Month")
ax1.set_ylabel("Snow (in)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.set_ylim(0, grouped["SNOW"].max())

# Custom x-ticks
ax1.set_xticks(np.arange(1, 13))
ax1.set_xticklabels(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
)

# Title and legend
plt.title("Monthly Total Snow and Temperature Range")
fig.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3)

# Grid
ax2.grid(True, alpha=0.3)

# Show plot
plt.tight_layout()
plt.show()

# %% [markdown]
# # Temperature Line Plot
#
# This Chart shows what the fill_between is but focused more on the temperatures only.
#

# %%
# KEEP
fig, ax1 = plt.subplots(figsize=(10, 5))

plt.plot(
    grouped["MONTH"],
    grouped["TMAX"],
    color="red",
    marker="x",
    label="Max Temperature (F)",
)
plt.plot(
    grouped["MONTH"],
    (grouped["TMAX"] + grouped["TMIN"]) / 2,
    color="grey",
    marker="x",
    label="Mean Temperature (F)",
)
plt.plot(
    grouped["MONTH"],
    grouped["TMIN"],
    color="blue",
    marker="o",
    label="Min Temperature (F)",
)
plt.xlabel("Month")
plt.ylabel("Temperature (F)")
plt.title("Monthly Max, Mean, & Min Temperatures 2023")
plt.legend()
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.show()

# %% [markdown]
# # TMAX & TMIN Stacked Bar Graph
#
# This is a stacked chart showing the frequency of the TMAX and TMIN. This shows theres a lot more even distribution in the TMAX than the TMIN with some temps getting really cold with a better cleaned distribution 0-50 degrees with some outliners below 0 and even below -20.
#

# %%
max_bins = range(10, 105, 5)
min_bins = range(-30, 65, 5)
fig, (ax1, ax2) = plt.subplots(2, 1)

cleaned23.hist(column="TMAX", ax=ax1, bins=max_bins, facecolor="red", edgecolor="white")
cleaned23.hist(
    column="TMIN", ax=ax2, bins=min_bins, facecolor="blue", edgecolor="white"
)

ax1.set_title("Yellowstone Mammoth Max Temperatures", fontsize=10)
ax2.set_title("Yellowstone Mammoth Min Temperatures", fontsize=10)

ax1.set_xlabel("Temperature (°F)", fontsize=16)
ax2.set_xlabel("Temperature (°F)", fontsize=16)

ax1.set_ylabel("Frequency", fontsize=10)
ax2.set_ylabel("Frequency", fontsize=10)

ax1.grid(alpha=0.25)
ax2.grid(alpha=0.25)
ax1.set_axisbelow(True)
ax2.set_axisbelow(True)

plt.tight_layout()
plt.show()

# %%
