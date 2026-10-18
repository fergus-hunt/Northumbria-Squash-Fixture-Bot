import sys
import pandas as pd

df = pd.read_csv("data/fixtures.csv")

by_team = "--by-team" in sys.argv

# Only count Newcastle University players, excluding walkovers
home = df[(df["Home team"].str.contains("Newcastle University", na=False)) & (df["Home Player"] != "(walkover)")][["Home Player", "Home team"]]
home.columns = ["Player", "Team"]
away = df[(df["Away team"].str.contains("Newcastle University", na=False)) & (df["Away Player"] != "(walkover)")][["Away Player", "Away team"]]
away.columns = ["Player", "Team"]

combined = pd.concat([home, away])

if by_team:
    counts = combined.groupby(["Player", "Team"]).size().reset_index(name="Matches Played")
    counts = counts.sort_values(["Team", "Matches Played"], ascending=[True, False])
    counts.to_csv("data/match_counts.csv", index=False)
    print("Saved match_counts.csv (grouped by team)")
else:
    counts = combined["Player"].value_counts().reset_index()
    counts.columns = ["Player", "Matches Played"]
    counts.to_csv("data/match_counts.csv", index=False)
    print("Saved match_counts.csv")
