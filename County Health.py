import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#since the csv is way too large, a keep function is necessary rather than dropping countless columns
keep = ["5-digit FIPS Code", "State Abbreviation", "Name", "County FIPS Code",
        "Children in Poverty (Black)", "Children in Poverty (White)", 
        "Median Household Income (Black)", "Median Household Income (White)",
        "% Rural raw value", "Uninsured raw value", "Primary Care Physicians raw value",
        "Preventable Hospital Stays raw value", "Median Household Income raw value",
        "Drug Overdose Deaths raw value", "Drug Overdose Deaths numerator", 
        "Drug Overdose Deaths denominator"]

csv_path = Path("/Users/hershoza/Downloads/analytic_data2025_v3.csv")

df = pd.read_csv(csv_path, usecols=keep, skiprows=[1], dtype={"5-digit FIPS Code": str, "County FIPS Code": str},)

#where my charts will be saved as a separate folder
folder_name = os.path.join(os.path.expanduser("~"), "health charts")
os.makedirs(folder_name, exist_ok=True)

def save_path(filename):
    return os.path.join(folder_name, filename)

print(f"Charts will be saved in: {folder_name}")

#brief synonpsis
print(df.shape)
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())

#changing the csv

df = df.rename(columns={"5-digit FIPS Code": "fips", "State Abbreviation": "state", "Name": "county", "County FIPS Code": "county_fips",
        "Children in Poverty (Black)": "blk_child_pov_rate", "Children in Poverty (White)": "whi_child_pov_rate", 
        "Median Household Income (Black)": "blk_med_income", "Median Household Income (White)": "whi_med_income",
        "% Rural raw value": "rural_pct", "Uninsured raw value": "uninsured_rate", "Primary Care Physicians raw value": "pcp_rate",
        "Preventable Hospital Stays raw value": "prev_hos_stays", "Median Household Income raw value": "med_income",
        "Drug Overdose Deaths raw value": "od_rate", "Drug Overdose Deaths numerator": "od_deaths", 
        "Drug Overdose Deaths denominator": "od_pop"})

df["fips"] = df["fips"].astype(str).str.zfill(5)
df["county_fips"] = df["county_fips"].astype(str).str.zfill(3)

round_cols = ["uninsured_rate", "blk_child_pov_rate", "whi_child_pov_rate", "rural_pct"]
df[round_cols] = (df[round_cols] * 100).round(2)

df["pcp_rate"] = (df["pcp_rate"] * 100000).round(2)
df["od_rate"] = df["od_rate"].round(2)

int_cols = ["prev_hos_stays", "od_deaths", "od_pop",
            "med_income", "blk_med_income", "whi_med_income"]
df[int_cols] = df[int_cols].astype("Int64")

#splitting into county rows and state rows
counties = df[df["county_fips"] != "000"].copy()
states = df[(df["county_fips"] == "000") & (df["state"] != "US")].copy()
us = df[df["state"] == "US"].iloc[0]

counties[int_cols] = counties[int_cols].astype(float)
states[int_cols] = states[int_cols].astype(float)

counties["od_pop"] = (counties["od_pop"] / 3).round()
counties["od_deaths"] = (counties["od_deaths"] / 3).round()

#boxplot
pov = counties.dropna(subset=["blk_child_pov_rate", "whi_child_pov_rate"])
pov_long = pov.melt(value_vars=["blk_child_pov_rate", "whi_child_pov_rate"],
                    var_name="race", value_name="child_pov")
pov_long["race"] = pov_long["race"].map({"blk_child_pov_rate": "Black", "whi_child_pov_rate": "White"})
 
fig, ax = plt.subplots(figsize=(8, 5))
pov_long.boxplot(column="child_pov", by="race", ax=ax, grid=False,
                 patch_artist=True,
                 boxprops=dict(facecolor="green", edgecolor="black"),
                 color=dict(whiskers="black", caps="black", medians="black"))
ax.set_title("Race and Child Poverty")
fig.suptitle("")
ax.set_xlabel("Race")
ax.set_ylabel("Child Poverty Rate (%)")
fig.tight_layout()
fig.savefig(save_path("q1_poverty.png"), dpi=150)
plt.close(fig)
 
inc = counties.dropna(subset=["blk_med_income", "whi_med_income"])
inc_long = inc.melt(value_vars=["blk_med_income", "whi_med_income"],
                    var_name="race", value_name="income_val")
inc_long["race"] = inc_long["race"].map({"blk_med_income": "Black", "whi_med_income": "White"})
 
fig, ax = plt.subplots(figsize=(8, 5))
inc_long.boxplot(column="income_val", by="race", ax=ax, grid=False,
                 patch_artist=True,
                 boxprops=dict(facecolor="green", edgecolor="black"),
                 color=dict(whiskers="black", caps="black", medians="black"))
ax.set_title("Race and Median Income")
fig.suptitle("")
ax.set_xlabel("Race")
ax.set_ylabel("Median Income")
fig.tight_layout()
fig.savefig(save_path("q1_income.png"), dpi=150)
plt.close(fig)

#scatterplot
for col, fname, title, ylabel in [("uninsured_rate", "q2_uninsured.png",
                                   "Rural and Uninsured Rate", "Uninsured (%)"),
                                    ("pcp_rate", "q2_pcp.png", "Rural and Primary Care Physican Access", 
                                     "Primary Care Physicans per 100,000"),
                                    ("prev_hos_stays", "q2_prev_stays.png",
                                     "Rural and Preventable Hospital Stays", "Preventable Stays per 100,000")]:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(counties["rural_pct"], counties[col], alpha=0.4, s=10, color="red")
    ax.set_title(title)
    ax.set_xlabel("Rural Population (%) of counties")
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(save_path(fname), dpi=150)
    plt.close(fig)

#barchart
od = states.dropna(subset=["od_rate"]).sort_values("od_rate", ascending=False)
colors = ["red" if s == "WV" else "powderblue" for s in od["state"]]
 
fig, ax = plt.subplots(figsize=(14, 5))
bars = ax.bar(od["state"], od["od_rate"], color=colors, edgecolor="black")
ax.bar_label(bars, labels=[f"{v:.1f}" if s == "WV" else "" for s, v in zip(od["state"], od["od_rate"])], padding=3)
ax.axhline(us["od_rate"], color="black", linestyle="--", linewidth=1)   #national rate
ax.set_ylim(0, od["od_rate"].max() * 1.15)
ax.set_title("Drug Overdoses by State")
ax.set_xlabel("States + DC")
ax.set_ylabel("Drug Overdose Deaths per 100,000")
plt.xticks(rotation=90)
fig.tight_layout()
fig.savefig(save_path("q3_overdose.png"), dpi=150)
plt.close(fig)

#exporting the polished version as a new csv
counties.to_csv("/Users/hershoza/Downloads/County_Health_Analysis.csv")
