import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json

# Get df data from pairsData.ipynb
with open ("Numpy, Pandas, Matplotlib/Project/filePath.json", "r") as file:
    content = json.load(file)
    file_path_pkl = content["pairs_data"]

df = pd.read_pickle(file_path_pkl)

# Signals when to buy/sell
df["Long_A"] = df["Z_Score"] > 2
df["Short_B"] = df["Z_Score"] > 2
df["Long_B"] = df["Z_Score"] < -2
df["Short_A"] = df["Z_Score"] < -2
df["Sell"] = (-1 < df["Z_Score"]) | (df["Z_Score"] < 1)

conditions_A = [(df["Long_A"]), 
                (df["Short_B"]),
                (df["Sell"])]
conditions_B = [(df["Long_B"]), 
                (df["Short_A"]),
                (df["Sell"])]
options = [1,-1,0]

# Are we in a stock or not
df["Stance_A"] = np.select(conditions_A, options)
df["Stance_A"] = df["Stance_A"].ffill().fillna(0)
df["Stance_B"] = np.select(conditions_B, options)
df["Stance_B"] = df["Stance_B"].ffill().fillna(0)

# Tracking Strategy performance
df["Daily_Portfolio"] = df["Daily_A"]*df["Stance_A"].shift(1) + df["Daily_B"]*df["Stance_B"].shift(1)
df["Cum_Portfolio"] = (1+df["Daily_Portfolio"].fillna(0)).cumprod()

# Visuals

fig, ax = plt.subplots(1,3,sharex=True,figsize=(15,8))
font = dict(fontfamily="times new roman", fontsize=11, fontweight="bold")
legend = dict(family="times new roman", size=10)

ax[0].plot(df["Date"],df["Daily_A_Norm"], color="red", linewidth=1.5, label="Coca-Cola (KO)")
ax[0].plot(df["Date"],df["Daily_B_Norm"], color="blue", linewidth=1.5, label="Pepsi (PEP)")
ax[0].set_xlabel("Date", **font)
ax[0].set_ylabel("Normalized Close Price", **font)
ax[0].set_title("Figure 1: Pepsi & Coca-Cola Normalized Close Price (1-2023 to 1-2026)", **font)
ax[0].legend(loc="upper left", prop=legend)

ax[1].plot(df["Date"],df["Z_Score"], color="black", linewidth=1.5, label="Z-Scores")
ax[1].axhline(y=2, color="limegreen", linewidth=2, linestyle="dotted")
ax[1].axhline(y=-2, color="limegreen", linewidth=2, linestyle="dotted")
ax[1].set_xlabel("Date",**font)
ax[1].set_ylabel("Z-Score of Difference in Normalized Close Price (PEP-KO)", **font)
ax[1].set_title("Figure 2: Pepsi & Coca-Cola Spread Z-Scores (1-2023 to 1-2026)", **font)
ax[1].legend(loc="upper right", prop=legend)

ax[2].plot(df["Date"],df["Cum_Stock"], color="orange", linewidth=1.5, label="Cumulative 50/50 Lazy Return")
ax[2].plot(df["Date"], df["Cum_Portfolio"], color="skyblue", linewidth=1.5, label="Cumulative Pairs Trading Return")
ax[2].set_xlabel("Date",**font)
ax[2].set_ylabel("USD ($)", **font)
ax[2].set_title("Figure 3: Lazy vs. Pairs Trading\nfor Pepsi & Coca-Cola (1-2023 to 1-2026)", **font)
ax[2].legend(loc="upper left", prop=legend)

for element in ax:
    element.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    element.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    element.tick_params(axis="both", labelsize=10)

for axis in ax:
    for label in axis.get_xticklabels():
        label.set_fontfamily("times new roman")

plt.tight_layout()
plt.show()
