import nba_api
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashteamstats

# gets season stats for a player
def getSeasonRow(player_id, season):
    career = playercareerstats.PlayerCareerStats(player_id=player_id, timeout=30)
    df = career.get_data_frames()[0]
    season_rows = df[df["SEASON_ID"] == season]
    if season_rows.empty:
        return None
    return season_rows.iloc[0]

#gets a player id from their name
def findPlayerID(name):
    matches = players.find_players_by_full_name
    if not matches:
        return None
    return matches[0]["id"]

# gets team totals, only rly needed for usg% as of rn
def getTeamRow(team_id, season):
    teams = leaguedashteamstats.LeagueDashTeamStats(
        season=season, per_mode_detailed="Totals", timeout=30
    )
    df = teams.get_data_frames()[0]
    return df[df["TEAM_ID"] == team_id].iloc[0]

# does the TS% calculations
def tsper(points, fga, fta):
    tsa = fga + 0.44 * fta 
    if tsa == 0:
        return 0.0
    return points / (2 * tsa)

# does the eFG% calculations
def efgper(fgm, tpm, fga):
    if fga == 0:
        return 0.0
    efg = (fgm + 0.5 * tpm) / fga
    return round(efg, 3)

# does the VORP calculations, Box +/-, % of Minutes Played, Team games (games played so far in the season)
def vorpcalc(boxPm, minPer, teamGames):
    vorp = (boxPm - (-2.0)) * minPer * (teamGames / 82)
    return vorp

# does the Usage % calcs
def usgcalc(fga, fta, tov, mp, tmFga, tmFta, tmTov, tmMp):
    if mp == 0:
        return 0.0
    player_poss = fga + 0.44 * fta + tov
    team_poss = tmFga + 0.44 * tmFta + tmTov
    if team_poss == 0:
        return 0.0
    usgper = 100 * (player_poss * (tmMp / 5)) / (mp * team_poss)
    return usgper

print("------------------------------------------------------------------")
print("The National Basketball Association Advanced Statistics Calculator")
print("------------------------------------------------------------------")
print("Efficiency Stats")
print("     1) TS%")
print("     2) eFG%")
print("     3) USG%")
print("Season Long Stats")
print("     4) VORP")
choice = int(input("Choice: "))
# True Shooting Percentage Calculator
if choice == 1:
    points = int(input("Points?: "))
    fga = int(input("Field goal attempts?: "))
    fta = int(input("Free throw attempts?: "))
    ts = tsper(points, fga, fta)
    print(f"The TS% is: {ts:.1%}")

# Efficiency Field Goal Percentage
elif choice == 2:
    fgm = int(input("Total field goals made?: "))
    tpm = int(input("Total 3-Pointers made?: "))
    fga = int(input("Field Goal Attempts?: "))
    efg = efgper(fgm, tpm, fga)
    print(f"eFG%: {efg}")

# Usage Rate Percentage
elif choice == 3:
    fga = int(input("Field goals attempted?: "))
    fta = int(input("Free throws attempted?:"))
    tov = int(input("Turnovers?: "))
    mp = int(input("Minutes Played?: "))
    tmFga = int(input("Team Field Goals Attempted?: "))
    tmFta = int(input("Team Free Throws Attempted?: "))
    tmMp = int(input("Team Minutes Played?: "))
    tmTov = int(input("Team Turnovers?: "))
    usg = usgcalc(fga, fta, tov, mp, tmFga, tmFta, tmTov, tmMp)
    print(f"Usage Rate Percentage: {usg:3f}")

# Value over Replacement Player
elif choice == 4:
    boxPm = float(input("Box +/- (Plus/Minus)?: "))
    minPlay = int(input("Total minutes played this season?: "))
    teamGames = int(input("Total Number of Team Games Played so far?: "))
    minPer = minPlay / (48 * teamGames)
    vorp = vorpcalc(boxPm, minPer, teamGames)
    print(f"VORP: {vorp:.1f}%")