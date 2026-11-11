from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashteamstats
from datetime import date, timedelta
from nba_api.stats.endpoints import leaguedashplayerstats

# gets the current season
def currentSeason():
    today = date.today()
    startYear = today.year if today.month >= 10 else today.year - 1
    return f"{startYear}-{str(startYear + 1)[-2:]}"

# gets stats for the week
def getWeekStats():
    today = date.today()
    weekAgo = today - timedelta(days=7)
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=currentSeason(),
        per_mode_detailed="Totals",
        date_from_nullable=weekAgo.strftime("%m/%d/%Y"),
        date_to_nullable=today.strftime("%m/%d/%Y"),
        timeout=30
    )
    return stats.get_data_frames()[0]

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

# Three Point Attempt Rate
def threeparate(fg3a, fga):
    if fga == 0:
        return 0
    return fg3a / fga

def percalc(pts, trb, ast, stl, blk, fgmi, ftmi, tov, gp):
    if gp == 0:
        return 0
    return (pts + trb + ast + stl + blk - fgmi - ftmi - tov) / gp

# used for player lookup
def promptForSeasonRow():
    name = input("What is the name of the player? (ex: LeBron James): ")
    season = input("What season would you like to lookup? (ex: 2025-26): ")
    playerID = findPlayerID(name)
    if playerID is None:
        print("Player not found. Follow name convention in example.")
        return None, None, None
    row = getSeasonRow(playerID, season)
    if row is None:
        print("No stats for that season. Check the format and year.")
        return None, None, None
    return name, season, row


def compareStatRows(stat_choice, row1, row2, team1=None, team2=None, box_pm1=None, box_pm2=None):
    if stat_choice == "1":
        return tsper(row1["PTS"], row1["FGA"], row1["FTA"]), tsper(row2["PTS"], row2["FGA"], row2["FTA"])
    if stat_choice == "2":
        return efgper(row1["FGM"], row1["FG3M"], row1["FGA"]), efgper(row2["FGM"], row2["FG3M"], row2["FGA"])
    if stat_choice == "3":
        if team1 is None or team2 is None:
            raise ValueError("Team rows are required for VORP comparison.")
        if box_pm1 is None or box_pm2 is None:
            raise ValueError("Box +/- values are required for VORP comparison.")
        min_per1 = row1["MIN"] / (48 * team1["GP"])
        min_per2 = row2["MIN"] / (48 * team2["GP"])
        return vorpcalc(float(box_pm1), min_per1, team1["GP"]), vorpcalc(float(box_pm2), min_per2, team2["GP"])
    if stat_choice == "4":
        if team1 is None or team2 is None:
            raise ValueError("Team rows are required for USG comparison.")
        team_mp1 = team1["MIN"] * 5
        team_mp2 = team2["MIN"] * 5
        left = usgcalc(row1["FGA"], row1["FTA"], row1["TOV"], row1["MIN"], team1["FGA"], team1["FTA"], team1["TOV"], team_mp1)
        right = usgcalc(row2["FGA"], row2["FTA"], row2["TOV"], row2["MIN"], team2["FGA"], team2["FTA"], team2["TOV"], team_mp2)
        return left, right
    if stat_choice == "5":
        stats = [("PTS", "PTS"), ("REB", "REB"), ("AST", "AST"), ("BLK", "BLK"), ("STL", "STL"), ("TOV", "TOV")]
        left = []
        right = []
        for _, column in stats:
            left.append(per36(row1[column], row1["MIN"]))
            right.append(per36(row2[column], row2["MIN"]))
        return left, right
    raise ValueError(f"Unsupported stat choice: {stat_choice}")

# function for option 5
def comparePlayersByStat(stat_choice):
    if stat_choice not in ["1", "2", "3", "4", "5"]:
        print("That isn't one of the options.")
        return

    name1, season1, row1 = promptForSeasonRow()
    name2, season2, row2 = promptForSeasonRow()
    if row1 is None or row2 is None:
        return

    team1 = team2 = None
    box_pm1 = box_pm2 = None

    if stat_choice in ["3", "4"]:
        if row1["TEAM_ID"] == 0 or row2["TEAM_ID"] == 0:
            print("One of these players was traded midseason, so the team lookup doesn't work, sorry!")
            return
        team1 = getTeamRow(row1["TEAM_ID"], season1)
        team2 = getTeamRow(row2["TEAM_ID"], season2)
        if team1["GP"] == 0 or team2["GP"] == 0:
            print("One of these teams hasn't played any games yet!")
            return
        if stat_choice == "3":
            box_pm1 = float(input(f"What was {name1}'s Box +/- for that season?: "))
            box_pm2 = float(input(f"What was {name2}'s Box +/- for that season?: "))

    values = compareStatRows(stat_choice, row1, row2, team1, team2, box_pm1, box_pm2)
    left, right = values

    if stat_choice == "1":
        print(f"{name1} {season1} TS%: {left:.1%}")
        print(f"{name2} {season2} TS%: {right:.1%}")
    elif stat_choice == "2":
        print(f"{name1} {season1} eFG%: {left:.1%}")
        print(f"{name2} {season2} eFG%: {right:.1%}")
    elif stat_choice == "3":
        print(f"{name1} {season1} VORP: {left:.1f}")
        print(f"{name2} {season2} VORP: {right:.1f}")
    elif stat_choice == "4":
        print(f"{name1} {season1} USG%: {left:.1%}")
        print(f"{name2} {season2} USG%: {right:.1%}")
    elif stat_choice == "5":
        stats = [("Points", "PTS"), ("Rebounds", "REB"), ("Assists", "AST"), ("Blocks", "BLK"), ("Steals", "STL"), ("Turnovers", "TOV")]
        print(f"{name1}, {season1} stats per 36 minutes:")
        for (label, _), value in zip(stats, left):
            print(f"      {label}: {value:.1f}")
        print(f"{name2}, {season2} stats per 36 minutes:")
        for (label, _), value in zip(stats, right):
            print(f"      {label}: {value:.1f}")


def lookupPlayerStat(choice):
    if choice not in range(1, 8):
        print("That isn't one of the options.")
        return

    name, season, row = promptForSeasonRow()
    if row is None:
        return

    if choice == 1:
        value = tsper(row["PTS"], row["FGA"], row["FTA"])
        print(f"{name} {season} TS%: {value:.1%}")
    elif choice == 2:
        value = efgper(row["FGM"], row["FG3M"], row["FGA"])
        print(f"{name} {season} eFG%: {value:.1%}")
    elif choice == 3:
        boxPm = float(input("What was the Box +/- for that season (look on Basketball Reference)?: "))
        if row["TEAM_ID"] == 0:
            print("This player was traded midseason, so the team lookup doesn't work, sorry!")
            return
        team = getTeamRow(row["TEAM_ID"], season)
        teamGames = team["GP"]
        if teamGames == 0:
            print(f"The {team['TEAM_NAME']} haven't played any games yet!")
            return
        minPer = row["MIN"] / (48 * teamGames)
        value = vorpcalc(boxPm, minPer, teamGames)
        print(f"{name} {season} VORP: {value:.1f}")
    elif choice == 4:
        if row["TEAM_ID"] == 0:
            print("This player was traded midseason, so the team lookup doesn't work, sorry!")
            return
        team = getTeamRow(row["TEAM_ID"], season)
        teamMp = team["MIN"] * 5
        value = usgcalc(
            row["FGA"], row["FTA"], row["TOV"], row["MIN"],
            team["FGA"], team["FTA"], team["TOV"], teamMp,
        )
        print(f"{name} {season} USG%: {value:.1f}")
    elif choice == 5:
        print(f"{name}, {season} stats per 36 minutes:")
        stats = [("Points", "PTS"), ("Rebounds", "REB"), ("Assists", "AST"),
                 ("Blocks", "BLK"), ("Steals", "STL"), ("Turnovers", "TOV")]
        for label, column in stats:
            value = per36(row[column], row["MIN"])
            print(f"      {label}: {value:.1f}")
    elif choice == 6:
        value = threeparate(row["FG3A"], row["FGA"])
        print(f"{name} {season} 3 Point Attempt Rate: {value:.3f}")
    elif choice == 7:
        fgmi = row["FGA"] - row["FGM"]
        ftmi = row["FTA"] - row["FTM"]
        value = percalc(
            row["PTS"], row["REB"], row["AST"], row["STL"], row["BLK"],
            fgmi, ftmi, row["TOV"], row["GP"],
        )
        print(f"{name} {season} Player Efficiency Rating: {value:.3f}")


leaderboardStats = {
    "1": {"label": "Points per game",
          "calc": lambda r: r["PTS"] / r["GP"], "percent": False, "minFga": 0},
    "2": {"label": "Rebounds per game",
          "calc": lambda r: r["REB"] / r["GP"], "percent": False, "minFga": 0},
    "3": {"label": "Assists per game",
          "calc": lambda r: r["AST"] / r["GP"], "percent": False, "minFga": 0},
    "4": {"label": "True Shooting % (TS%)",
          "calc": lambda r: tsper(r["PTS"], r["FGA"], r["FTA"]), "percent": True, "minFga": 20},
    "5": {"label": "Effective FG% (eFG%)",
          "calc": lambda r: efgper(r["FGM"], r["FG3M"], r["FGA"]), "percent": True, "minFga": 20},
}

def buildLeaderboard(df, statFunc, minGames, minFga):
    results = []
    for index, row in df.iterrows():
        if row["GP"] < minGames:
            continue
        if row["FGA"] < minFga:
            continue
        value = statFunc(row)
        results.append((row["PLAYER_NAME"], row["TEAM_ABBREVIATION"], value))
    results.sort(key=lambda item: item[2], reverse=True)
    return results

def printLeaderboard(results, label, isPercent, topN=10):
    print(f"Top {topN} this week: {label}")
    for rank, (name, team, value) in enumerate(results[:topN], start=1):
        if isPercent:
            shown = f"{value:.1%}"
        else:
            shown = f"{value:.1f}"
        print(f"  {rank:>2}. {name} ({team}): {shown}")


def readMenuChoice(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a numeric menu choice.")
        return None


def main_loop():
    running = True

    while running:
        print("----------------------------------------------------------------------")
        print("| The National Basketball Association Advanced Statistics Calculator |")
        print("----------------------------------------------------------------------")
        print("     1) Custom Calculator")
        print("     2) Stat Lookup")
        print("     3) Stat Leaderboard")
        print("     4) Player Stat Comparison")
        choice = readMenuChoice("Choice: ")
        if choice is None:
            continue

        # all custom calculation choices
        if choice == 1:
            print("What Statistic would you like to calculate?")
            print("     1) True Shooting Percentage (TS%)")
            print("     2) Effective Field Goal Percentage (eFG%)")
            print("     3) Value Over Replacement Player (VORP)")
            print("     4) Usage Rate Percentage (USG%)")
            choice = readMenuChoice("Choice?: ")
            if choice is None:
                continue

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
                print(f"Usage Rate Percentage: {usg:.1f}")

        # player advanced-stat lookup
        elif choice == 2:
            print("First, what Advanced Statistic would you like to lookup?")
            print("     1) True Shooting Percentage (TS%)")
            print("     2) Effective Field Goal Percentage (eFG%)")
            print("     3) Value Over Replacement Player (VORP)")
            print("     4) Usage Rate Percentage (USG%)")
            print("     5) Players Per 36 Minutes Stats")
            print("     6) Three Point Attempt Rate")
            print("     7) Player Efficiency Rating (PER)")
            statChoice = readMenuChoice("Choice?: ")
            if statChoice is None:
                continue
            lookupPlayerStat(statChoice)

        # weekly stat leaderboard
        elif choice == 3:
            print("Which stat would you like the weekly leaders for?")
            for key, info in leaderboardStats.items():
                print(f"     {key}) {info['label']}")
            pick = input("Choice?: ")
            if pick not in leaderboardStats:
                print("That isn't one of the options.")
            else:
                info = leaderboardStats[pick]
                df = getWeekStats()
                if df.empty:
                    print("No games found in the last 7 days.")
                else:
                    results = buildLeaderboard(df, info["calc"], 2, info["minFga"])
                    printLeaderboard(results, info["label"], info["percent"])

        # player stat comparison
        elif choice == 4:
            print("What statistic would you like to compare?")
            print("     1) True Shooting Percentage (TS%)")
            print("     2) Effective Field Goal Percentage (eFG%)")
            print("     3) Value Over Replacement Player (VORP)")
            print("     4) Usage Rate Percentage (USG%)")
            print("     5) Players Per 36 Minutes Stats")
            stat = input("Enter choice (1-5): ")
            comparePlayersByStat(stat)


if __name__ == "__main__":
    main_loop()