import nba_api

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

print("------------------------------------------------------------------")
print("The National Basketball Association Advanced Statistics Calculator")
print("------------------------------------------------------------------")
print("Shooting Stats")
print("     1) TS%")
print("     2) eFG%")
print("Team-Based Stats")
print("     3) VORP")
choice = int(input("Choice: "))
# True Shooting Percentage Calculator
if choice == 1:
    points = int(input("Points?: "))
    fga = int(input("Field goal attempts?: "))
    fta = int(input("Free throw attempts?: "))
    ts = tsper(points, fga, fta)
    print(f"The TS% is: {ts:.1%}")

# Efficiency Field Goal Percentage
if choice == 2:
    fgm = int(input("Total field goals made?: "))
    tpm = int(input("Total 3-Pointers made?: "))
    fga = int(input("Field Goal Attempts?: "))
    efg = efgper(fgm, tpm, fga)
    print(f"eFG%: {efg}")

# Value over Replacement Player
if choice == 3:
    boxPm = float(input("Box +/- (Plus/Minus)?: "))
    minPlay = int(input("Total minutes played this season?: "))
    teamGames = int(input("Total Number of Team Games Played so far?: "))
    minPer = minPlay / (48 * teamGames)
    vorp = vorpcalc(boxPm, minPer, teamGames)
    print(f"VORP: {vorp:.3f}")