import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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

folder_name = os.path.join(os.path.expanduser("~"), "county health analysis charts")
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

#helper functions to ensure it matches R test results

def mean_ci(x):
    x = np.asarray(x, dtype=float)
    m = x.mean()
    half = stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return m, m - half, m + half

def ols(y, xs):
    d = counties.dropna(subset=[y] + xs)
    X = np.column_stack([np.ones(len(d))] + [d[x] for x in xs])
    return np.linalg.lstsq(X, d[y], rcond=None)[0]

#boxplot (question 1: paired t-tests)

for blk, whi, fname, title, ylabel in [("blk_child_pov_rate", "whi_child_pov_rate", "q1_poverty.png",
                                        "Race and Child Poverty", "Child Poverty Rate (%)"),
                                       ("blk_med_income", "whi_med_income", "q1_income.png",
                                        "Race and Median Household Income", "Median Household Income ($)")]:
    pair = counties.dropna(subset=[blk, whi])
    m, lo, hi = mean_ci(pair[blk] - pair[whi])
    t, p = stats.ttest_rel(pair[blk], pair[whi])
 
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot([pair[blk], pair[whi]], tick_labels=["Black", "White"], patch_artist=True,
               boxprops=dict(facecolor="green", edgecolor="black"),
               whiskerprops=dict(color="black"), capprops=dict(color="black"),
               medianprops=dict(color="black"), showmeans=True,
               meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black"))
    ax.set_title(title)
    ax.set_xlabel("Race")
    ax.set_ylabel(ylabel)
    if "income" in blk:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
        money = lambda v: f"-${abs(v):,.0f}" if v < 0 else f"${v:,.0f}"
        diff_text = f"{money(m)} (95% CI {money(lo)} to {money(hi)})"
    else:
        diff_text = f"{m:.1f} pts (95% CI {lo:.1f} to {hi:.1f})"
    ax.text(0.98, 0.97, f"Mean difference (Black − White): {diff_text}\n"
                        f"Paired t-test: t = {t:.2f}, p < 0.001, n = {len(pair):,} counties\n"
                        f"◇ = mean, line = median",
            transform=ax.transAxes, ha="right", va="top", fontsize=9,
            bbox=dict(facecolor="white", edgecolor="gray"))
    fig.tight_layout()
    fig.savefig(save_path(fname), dpi=150)
    plt.close(fig)
 
#splitting rural percentage into a more rural or more urban category (area type), same cutoff as R

counties["area_type"] = np.where(counties["rural_pct"] >= 50, "Rural", "Urban")
counties.loc[counties["rural_pct"].isna(), "area_type"] = np.nan
median_income = counties["med_income"].median()
 
#bar chart + scatterplot (question 2: welch t-tests and linear regressions)

for col, fname, title, ylabel in [("uninsured_rate", "q2_uninsured.png",
                                   "Rural and Uninsured Rate", "Uninsured (%)"),
                                    ("pcp_rate", "q2_pcp.png", "Rural and Primary Care Physician Access",
                                     "Primary Care Physicians per 100,000"),
                                    ("prev_hos_stays", "q2_prev_stays.png",
                                     "Rural and Preventable Hospital Stays", "Preventable Stays per 100,000")]:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
 
    rural = counties.loc[counties["area_type"] == "Rural", col].dropna()
    urban = counties.loc[counties["area_type"] == "Urban", col].dropna()
    t, p = stats.ttest_ind(rural, urban, equal_var=False)
    for i, grp in enumerate([rural, urban]):
        m, lo, hi = mean_ci(grp)
        ax1.bar(i, m, color="powderblue", edgecolor="black", width=0.6)
        ax1.errorbar(i, m, yerr=[[m - lo], [hi - m]], color="black", capsize=8, linewidth=1.5)
        ax1.text(i, hi, f"{m:,.1f}", ha="center", va="bottom")
    ax1.set_xticks([0, 1], [f"Rural (≥50%)\nn = {len(rural):,}", f"Urban (<50%)\nn = {len(urban):,}"])
    ax1.set_xlabel("Area Type")
    ax1.set_ylabel(ylabel)
    p_text = "p < 0.001" if p < 0.001 else f"p = {p:.3f}"
    ax1.set_title(f"Welch t-test: t = {t:.2f}, {p_text}\n(bars = means, whiskers = 95% CI)", fontsize=10)
 
    pts = counties.dropna(subset=["rural_pct", col])
    ax2.scatter(pts["rural_pct"], pts[col], alpha=0.2, s=10, color="red")
    raw = ols(col, ["rural_pct"])
    adj = ols(col, ["rural_pct", "med_income"])
    x = np.array([0, 100])
    ax2.plot(x, raw[0] + raw[1] * x, color="black", linestyle="--", linewidth=2,
             label=f"Rurality only: {raw[1]:+.3g} per pt")
    ax2.plot(x, adj[0] + adj[1] * x + adj[2] * median_income, color="blue", linewidth=2,
             label=f"Controlling for income: {adj[1]:+.3g} per pt")
    ax2.set_ylim(pts[col].quantile(0.01), pts[col].quantile(0.99))   #zoom in so the lines are visible
    ax2.set_xlabel("Rural Population (%) of counties")
    ax2.set_ylabel(ylabel)
    ax2.set_title("Regression lines (adjusted line drawn at median income)", fontsize=10)
    ax2.legend(loc="upper left", fontsize=9)
 
    fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(save_path(fname), dpi=150)
    plt.close(fig)
 
#strip plot (question 3: welch t-test and wilcox test)

counties["is_wv"] = np.where(counties["state"] == "WV", "WV", "Other")
wv = counties.loc[counties["is_wv"] == "WV", "od_rate"].dropna()
other = counties.loc[counties["is_wv"] == "Other", "od_rate"].dropna()
t, p = stats.ttest_ind(other, wv, equal_var=False)
w, p_w = stats.mannwhitneyu(other, wv)
 
fig, ax = plt.subplots(figsize=(8, 5))
rng = np.random.default_rng(0)   #small random sideways spread so the dots don't stack
for i, (grp, color) in enumerate([(other, "powderblue"), (wv, "red")]):
    ax.scatter(i + rng.uniform(-0.18, 0.18, len(grp)), grp, s=10, alpha=0.5, color=color, edgecolor="none")
    m, lo, hi = mean_ci(grp)
    ax.errorbar(i, m, yerr=[[m - lo], [hi - m]], fmt="D", color="black", markersize=8, capsize=10, linewidth=2)
    ax.text(i + 0.25, m, f"mean {m:.1f}", va="center")
ax.set_xticks([0, 1], [f"All other counties\nn = {len(other):,}", f"West Virginia counties\nn = {len(wv)}"])
ax.set_xlim(-0.5, 1.8)
ax.set_title("Drug Overdoses: West Virginia vs Other Counties")
ax.set_ylabel("Drug Overdose Deaths per 100,000")
ax.text(0.02, 0.97, f"Welch t-test: t = {t:.2f}, p < 0.001\n"
                    f"Wilcoxon: W = {w:,.0f}, p < 0.001\n"
                    f"◆ = mean with 95% CI, dots = counties",
        transform=ax.transAxes, va="top", fontsize=9, bbox=dict(facecolor="white", edgecolor="gray"))
fig.tight_layout()
fig.savefig(save_path("q3_overdose.png"), dpi=150)
plt.close(fig)
 
#other barchart 
od = states.dropna(subset=["od_rate"]).sort_values("od_rate", ascending=False)
colors = ["red" if s == "WV" else "powderblue" for s in od["state"]]
 
fig, ax = plt.subplots(figsize=(14, 5))
bars = ax.bar(od["state"], od["od_rate"], color=colors, edgecolor="black")
ax.bar_label(bars, labels=[f"{v:.1f}" if s == "WV" else "" for s, v in zip(od["state"], od["od_rate"])], padding=3)
ax.axhline(us["od_rate"], color="black", linestyle="--", linewidth=1,
           label=f"U.S. rate ({us['od_rate']:.1f})")   #national rate
ax.set_ylim(0, od["od_rate"].max() * 1.15)
ax.set_title("Drug Overdoses by State (state rates)")
ax.set_xlabel("States + DC")
ax.set_ylabel("Drug Overdose Deaths per 100,000")
ax.legend()
plt.xticks(rotation=90)
fig.tight_layout()
fig.savefig(save_path("q3_overdose_states.png"), dpi=150)
plt.close(fig)

#exporting the polished version as a new csv

counties.to_csv("/Users/hershoza/Downloads/County_Health_Analysis.csv")
