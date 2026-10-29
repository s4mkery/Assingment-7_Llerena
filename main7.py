import pandas as pd
import numpy as np
from scipy import integrate, stats, interpolate

data = pd.read_csv("NBA_Data.csv")
df_filtered = data[data["Stage"] == "Regular_Season"]
top_player = df_filtered["Player"].mode()[0]
player_df = df_filtered[df_filtered["Player"] == top_player].copy()

player_df["3P_Accuracy"] = ((player_df["3PM"] / player_df["3PA"]) * 100).fillna(0)

player_df["Year"] = (
    player_df["Season"].str.split("-").str[0].astype(int)
)

x = player_df["Year"].to_numpy(dtype=float)
y = player_df["3P_Accuracy"].to_numpy(dtype=float)


reg_line = stats.linregress(x, y)
def best_fit (x):
    return reg_line.slope * x + reg_line.intercept

a=2000
b=2019

num , error = integrate.quad(best_fit, a,b) 

mean_accuracy = num/(b-a)
#How does this value compared to the actual average number of 3-pointers made by this player? 36.99 vs 36.88

linespline =  interpolate.interp1d(x, y, kind="linear")
missed_years = np.array([2002,2015], dtype=float)

preds = linespline(missed_years)
print(f"Prediction for 2002: {preds[0]} \nPrediction for 2015: {preds[1]}\n")

#Part 2
clean_data = df_filtered.dropna(subset=["FGM", "FGA"])
fgm = clean_data["FGM"].dropna().to_numpy()
fga = clean_data["FGA"].dropna().to_numpy()

for name, data in [("FGM", fgm), ("FGA", fga)]:
   
    mean_val = stats.tmean(data)       
    var_val = stats.tvar(data)         
    skew_val = stats.skew(data)        
    kurt_val = stats.kurtosis(data)

    print(f"{name}")
    print(f"Mean:     {mean_val}")
    print(f"Variance: {var_val}")
    print(f"Skew:     {skew_val}")
    print(f"Kurtosis: {kurt_val}\n")

ind_t_fgm = stats.ttest_1samp(fgm, 0)
ind_t_fga = stats.ttest_1samp(fga, 0)
rel_test = stats.ttest_rel(fgm, fga)

print(f"Individual FGM: t = {ind_t_fgm.statistic}, p = {ind_t_fgm.pvalue}")
print(f"Individual FGA: t = {ind_t_fga.statistic}, p = {ind_t_fga.pvalue}")
print(f"Related Samples: t = {rel_test.statistic}, p = {rel_test.pvalue}")