import nba_api
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.endpoints import boxscoretraditionalv3

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
    matches = players.find_players_by_full_name(name)
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

# does per 36 minute calculations, only for player lookup
def per36(stat, minutes):
    if minutes == 0:
        return 0.0
    return stat / minutes * 36


print("----------------------------------------------------------------------")
print("| The National Basketball Association Advanced Statistics Calculator |")
print("----------------------------------------------------------------------")
print("     1) Custom Calculator")
print("     2) Stat Lookup")
choice = int(input("Choice: "))

# all custom calculation choices
if choice == 1:
    print("What Statistic would you like to calculate?")
    print("     1) True Shooting Percentage (TS%)")
    print("     2) Effective Field Goal Percentage (eFG%)")
    print("     3) Value Over Replacement Player (VORP)")
    print("     4) Usage Rate Percentage (USG%)")
    choice = int(input("Choice?: "))

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

    # Value over Replacement Player
    elif choice == 3:
        boxPm = float(input("Box +/- (Plus/Minus)?: "))
        minPlay = int(input("Total minutes played this season?: "))
        teamGames = int(input("Total Number of Team Games Played so far?: "))
        minPer = minPlay / (48 * teamGames)
        vorp = vorpcalc(boxPm, minPer, teamGames)
        print(f"VORP: {vorp:.1f}")

    # Usage Rate Percentage
    elif choice == 4:
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

# player advstat lookup
elif choice == 2:
    print("First, what Advanced Statistic would you like to lookup?")
    print("     1) True Shooting Percentage (TS%)")
    print("     2) Effective Field Goal Percentage (eFG%)")
    print("     3) Value Over Replacement Player (VORP)")
    print("     4) Usage Rate Percentage (USG%)")
    print("     5) Players Per 36 Minutes Stats")
    choice = int(input("Choice?: "))

    # True Shooting percentage
    if choice == 1:
        name = str(input("What is the name of the player? (ex: LeBron James): "))
        season = str(input("What season would you like to lookup? (ex: 2025-26): "))
        playerID = findPlayerID(name)
        if playerID is None:
            print("Player not found. Follow name convention in example.")
        else:
            row = getSeasonRow(playerID, season)
            if row is None:
                print("No stats for that season. Make sure you followed the convention in the example or entered the correct year.")
            else:
                ts = tsper(row["PTS"], row["FGA"], row["FTA"])
                print(f"{name} {season} TS%: {ts:.1%}")

    # Effective Field Goal Percentage
    elif choice == 2:
        name = str(input("What is the name of the player? (ex: LeBron James): "))
        season = str(input("What season would you like to lookup? (ex: 2025-26): "))
        playerID = findPlayerID(name)
        if playerID is None:
            print("Player not found. Follow name convention in example.")
        else:
            row = getSeasonRow(playerID, season)
            if row is None:
                print("No stats for that season. Make sure you followed the convention in the example or entered the correct year.")
            else:
                efg = efgper(row["FGM"], row["FG3M"], row["FGA"])
                print(f"{name} {season} eFG%: {efg:.1%}")

    # Value Over Replacement Player
    elif choice == 3:
        name = str(input("What is the name of the player? (ex: LeBron James): "))
        season = str(input("What season would you like to lookup? (ex: 2025-26): "))
        boxPm = float(input("What was the Box +/- for that season (look on Basketball Reference)?: "))
        playerID = findPlayerID(name)
        if playerID is None:
            print("Player not found. Follow name convention in example.")
        else:
            row = getSeasonRow(playerID, season)
            if row is None:
                print("No stats for that season. Make sure you followed the convention in the example or entered the correct year.")
            elif row["TEAM_ID"] == 0:
                print("This player was traded midseason, so the team lookup doesn't work, sorry!")
            else:
                team = getTeamRow(row["TEAM_ID"], season)
                teamGames = team["GP"]
                if teamGames == 0:
                    print(f"The {team['TEAM_NAME']} haven't played any games yet!")
                else:
                    minPer = row["MIN"] / (48 * teamGames)
                    vorp = vorpcalc(boxPm, minPer, teamGames)
                    print(f"{name} {season} VORP: {vorp:.1f}")

    # Usage Rate Percentage
    elif choice == 4: 
        name = str(input("What is the name of the player? (ex: LeBron James): "))
        season = str(input("What season would you like to lookup? (ex: 2025-26): "))
        playerID = findPlayerID(name)
        if playerID is None:
            print("Player not found. Follow name convention in example.")
        else:
            row = getSeasonRow(playerID, season)
            if row is None:
                print("No stats for that season. Make sure you followed the convention in the example or entered the correct year.")
            elif row["TEAM_ID"] == 0:
                print("This player was traded midseason, so the team lookup doesn't work, sorry!")
            else:
                team = getTeamRow(row["TEAM_ID"], season)
                teamMp = team["MIN"] * 5
                usg = usgcalc(
                    row["FGA"], row["FTA"], row["TOV"], row["MIN"],
                    team["FGA"], team["FTA"], team["TOV"], teamMp                    
                    )
                print(f"{name} {season} USG%: {usg:.1f}")

    # Per 36
    elif choice == 5:
        name = str(input("What is the name of the player? (ex: LeBron James): "))
        season = str(input("What season would you like to lookup? (ex: 2025-26): "))
        playerID = findPlayerID(name)
        if playerID is None:
            print("Player not found. Follow name convention in example.")
        else:
            row = getSeasonRow(playerID, season)
            if row is None:
                print("No stats for that season. Make sure you followed the convention in the example or entered the correct year.")
            else:
                row = getSeasonRow(playerID, season)
                if row is None:
                    print("No statistics for the entered season.")
                else:
                    print(f"{name}, {season} stats per 36 minutes:")
                    stats = [("Points", "PTS"), ("Rebounds", "REB"), ("Assists", "AST"),
                            ("Blocks", "BLK"), ("Steals", "STL"), ("Turnovers", "TOV")]
                    for label, column in stats:
                        value = per36(row[column], row["MIN"])
                        print(f"      {label}: {value:.1f}")
