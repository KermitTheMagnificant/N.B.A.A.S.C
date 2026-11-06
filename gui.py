import tkinter as tk
from main import (
    currentSeason, efgper, findPlayerID, getSeasonRow, getTeamRow,
    per36, percalc, threeparate, tsper, usgcalc, vorpcalc,
)

# =====================================================================
# SECTION 1: WINDOW SETUP
# =====================================================================
BG = "#F3F6FB"
CARD = "#FFFFFF"
NAVY = "#10243A"
NAVY_HOVER = "#1C3855"
ORANGE = "#F47B35"
ORANGE_HOVER = "#D96120"
TEXT = "#172B42"
MUTED = "#66778A"
BORDER = "#DCE4ED"
FONT = "Segoe UI"

root = tk.Tk()

root.title("National Basketball Association Advanced Statistics Calculator")
root.geometry("920x820")
root.minsize(760, 680)
root.configure(bg = BG)

header = tk.Frame(root, bg = NAVY, height = 112)
header.pack(fill = "x")
header.pack_propagate(False)

tk.Label(header, text = "COURTSIDE  /  NBA ADVANCED STATS", font = (FONT, 10, "bold"),
         bg = NAVY, fg = "#F6A46F").pack(anchor = "w", padx = 32, pady = (18, 3))
tk.Label(header, text = "Basketball Statistics Studio", font = (FONT, 23, "bold"),
         bg = NAVY, fg = "#FFFFFF").pack(anchor = "w", padx = 32)
tk.Label(header, text = "Calculate custom metrics or explore a player's season.",
         font = (FONT, 10), bg = NAVY, fg = "#C2D0DE").pack(anchor = "w", padx = 34, pady = (2, 0))

navBar = tk.Frame(root, bg = BG, height = 58)
navBar.pack(fill = "x", padx = 24, pady = (10, 4))
navBar.pack_propagate(False)

contentArea = tk.Frame(root, bg = BG)
contentArea.pack(fill = "both", expand = True, padx = 24, pady = (0, 20))

# =====================================================================
# SECTION 2: THE THREE SCREENS (frames stacked in the same spot)
# =====================================================================
pageCalc = tk.Frame(contentArea, bg = BG)
pageStats = tk.Frame(contentArea, bg = BG)
pageLeader = tk.Frame(contentArea, bg = BG)

for page in (pageCalc, pageStats, pageLeader):
    page.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

leaderCard = tk.Frame(pageLeader, bg = CARD, highlightbackground = BORDER, highlightthickness = 1)
leaderCard.place(relx = 0.5, rely = 0.15, relwidth = 0.86, relheight = 0.72, anchor = "n")
tk.Label(leaderCard, text = "Leaderboard", font = (FONT, 19, "bold"),
         bg = CARD, fg = TEXT).pack(pady = (42, 8))
tk.Label(leaderCard, text = "Weekly player leaders are coming soon.", font = (FONT, 11),
         bg = CARD, fg = MUTED).pack()

# =====================================================================
# SECTION 3: SCREEN SWITCHING AND THE TOP BUTTONS
# =====================================================================
def showPage(page):
    page.tkraise()
    for navPage, button in navButtons.items():
        isActive = navPage == page
        button.configure(
            bg = ORANGE if isActive else CARD,
            fg = "#FFFFFF" if isActive else TEXT,
            activebackground = ORANGE_HOVER if isActive else "#E8EEF5",
            activeforeground = "#FFFFFF" if isActive else TEXT,
            relief = "flat",
        )

navButtons = {}
for page, label in ((pageCalc, "Calculator"), (pageStats, "Statistics"),
                    (pageLeader, "Leaderboard")):
    button = tk.Button(
        navBar, text = label, command = lambda selectedPage = page: showPage(selectedPage),
        font = (FONT, 10, "bold"), bd = 0, padx = 20, pady = 9, cursor = "hand2",
        bg = CARD, fg = TEXT, activebackground = "#E8EEF5", activeforeground = TEXT,
        relief = "flat", highlightthickness = 1, highlightbackground = BORDER,
    )
    button.pack(side = "left", padx = (0, 9), pady = 7)
    navButtons[page] = button

buttonCalc = navButtons[pageCalc]
buttonStats = navButtons[pageStats]
buttonLeader = navButtons[pageLeader]

# =====================================================================
# SECTION 4: CALCULATOR SCREEN - form-building helper
# =====================================================================
def makeCalcForm(parent, title, fields, calculate):
    frame = tk.Frame(parent, bg = CARD, highlightbackground = BORDER, highlightthickness = 1)
    frame.place(relx = 0.5, rely = 0.14, relwidth = 0.86, relheight = 0.83, anchor = "n")
    tk.Label(frame, text = title, font = (FONT, 17, "bold"),
             bg = CARD, fg = TEXT).pack(pady = (18, 12))

    entries = []
    for labelText in fields:
        tk.Label(frame, text = labelText, font = (FONT, 9, "bold"),
                 bg = CARD, fg = MUTED).pack(pady = (3, 2))
        entry = tk.Entry(frame, font = (FONT, 10), width = 32, bd = 0,
                         bg = "#F5F7FA", fg = TEXT, insertbackground = TEXT,
                         highlightthickness = 1, highlightbackground = BORDER,
                         highlightcolor = ORANGE)
        entry.pack()
        entries.append(entry)

    labelResult = tk.Label(frame, text = "", font = (FONT, 12, "bold"),
                           bg = CARD, fg = TEXT, wraplength = 620)

    def onClick():
        try:
            values = [float(e.get()) for e in entries]
        except ValueError:
            labelResult.config(text = "Please enter numbers only.")
            return
        labelResult.config(text = calculate(*values))

    tk.Button(frame, text = "Calculate", command = onClick, font = (FONT, 10, "bold"),
              bg = ORANGE, fg = "#FFFFFF", activebackground = ORANGE_HOVER,
              activeforeground = "#FFFFFF", bd = 0, padx = 24, pady = 9,
              cursor = "hand2", relief = "flat").pack(pady = 14)
    labelResult.pack(pady = (3, 10))
    return frame

# =====================================================================
# SECTION 5: CALCULATOR SCREEN - one small function per stat
# =====================================================================
def calcTS(points, fga, fta):
    return f"TS%: {tsper(points, fga, fta):.1%}"

def calcEFG(fgm, tpm, fga):
    return f"eFG%: {efgper(fgm, tpm, fga):.1%}"

def calcVORP(boxPm, minPlay, teamGames):
    if teamGames == 0:
        return "Team games can't be 0."
    minPer = minPlay / (48 * teamGames)
    return f"VORP: {vorpcalc(boxPm, minPer, teamGames):.1f}"

def calcUSG(fga, fta, tov, mp, tmFga, tmFta, tmMp, tmTov):
    usg = usgcalc(fga, fta, tov, mp, tmFga, tmFta, tmTov, tmMp)
    return f"USG%: {usg:.1f}"

# =====================================================================
# SECTION 6: STATISTICS SCREEN - Form Building 
# =====================================================================
def makeStatsForm(parent, title, fields, lookup):
    frame = tk.Frame(parent, bg = CARD, highlightbackground = BORDER, highlightthickness = 1)
    frame.place(relx = 0.5, rely = 0.14, relwidth = 0.86, relheight = 0.83, anchor = "n")
    tk.Label(frame, text = title, font = (FONT, 17, "bold"),
             bg = CARD, fg = TEXT).pack(pady = (22, 16))

    entries = []
    for labelText in fields:
        tk.Label(frame, text = labelText, font = (FONT, 9, "bold"),
                 bg = CARD, fg = MUTED).pack(pady = (6, 3))
        entry = tk.Entry(frame, font = (FONT, 10), width = 34, bd = 0,
                         bg = "#F5F7FA", fg = TEXT, insertbackground = TEXT,
                         highlightthickness = 1, highlightbackground = BORDER,
                         highlightcolor = ORANGE)
        if labelText == "Season":
            entry.insert(0, currentSeason())
        entry.pack()
        entries.append(entry)

    labelResult = tk.Label(frame, text = "", font = (FONT, 11, "bold"),
                           bg = CARD, fg = TEXT, wraplength = 620)

    def onClick():
        values = [entry.get().strip() for entry in entries]
        if any(not value for value in values):
            labelResult.config(text = "Please fill in every field.")
            return
        try:
            labelResult.config(text = lookup(*values))
        except ValueError:
            labelResult.config(text = "Please enter a valid number for Box +/-." )
        except Exception:
            labelResult.config(text = "Statistics lookup failed. Check your connection and inputs.")

    tk.Button(frame, text = "Look up statistics", command = onClick,
              font = (FONT, 10, "bold"), bg = ORANGE, fg = "#FFFFFF",
              activebackground = ORANGE_HOVER, activeforeground = "#FFFFFF",
              bd = 0, padx = 24, pady = 9, cursor = "hand2", relief = "flat").pack(pady = 16)
    labelResult.pack(pady = 5)
    return frame


def getStatsRow(name, season):
    playerID = findPlayerID(name)
    if playerID is None:
        return None, "Player not found. Check the player's full name."
    row = getSeasonRow(playerID, season)
    if row is None:
        return None, "No stats found for that player and season."
    return row, None


def lookupTS(name, season):
    row, error = getStatsRow(name, season)
    if error:
        return error
    return f"{name} {season} TS%: {tsper(row['PTS'], row['FGA'], row['FTA']):.1%}"


def lookupEFG(name, season):
    row, error = getStatsRow(name, season)
    if error:
        return error
    return f"{name} {season} eFG%: {efgper(row['FGM'], row['FG3M'], row['FGA']):.1%}"


def lookupVORP(name, season, boxPm):
    row, error = getStatsRow(name, season)
    if error:
        return error
    if row['TEAM_ID'] == 0:
        return "Team stats are unavailable for players traded midseason."
    team = getTeamRow(row['TEAM_ID'], season)
    teamGames = team['GP']
    if teamGames == 0:
        return "The player's team has not played any games this season."
    minPer = row['MIN'] / (48 * teamGames)
    return f"{name} {season} VORP: {vorpcalc(float(boxPm), minPer, teamGames):.1f}"


def lookupUSG(name, season):
    row, error = getStatsRow(name, season)
    if error:
        return error
    if row['TEAM_ID'] == 0:
        return "Team stats are unavailable for players traded midseason."
    team = getTeamRow(row['TEAM_ID'], season)
    teamMp = team['MIN'] * 5
    value = usgcalc(
        row['FGA'], row['FTA'], row['TOV'], row['MIN'],
        team['FGA'], team['FTA'], team['TOV'], teamMp,
    )
    return f"{name} {season} USG%: {value:.1f}"


def lookupPer36(name, season):
    row, error = getStatsRow(name, season)
    if error:
        return error
    stats = [("Points", "PTS"), ("Rebounds", "REB"), ("Assists", "AST"),
             ("Blocks", "BLK"), ("Steals", "STL"), ("Turnovers", "TOV")]
    lines = [f"{name} {season} per 36 minutes:"]
    lines.extend(f"{label}: {per36(row[column], row['MIN']):.1f}" for label, column in stats)
    return "\n".join(lines)


def lookupThreePointRate(name, season):
    row, error = getStatsRow(name, season)
    if error:
        return error
    value = threeparate(row['FG3A'], row['FGA'])
    return f"{name} {season} 3-point attempt rate: {value:.3f}"


def lookupPER(name, season):
    row, error = getStatsRow(name, season)
    if error:
        return error
    value = percalc(
        row['PTS'], row['REB'], row['AST'], row['STL'], row['BLK'],
        row['FGA'] - row['FGM'], row['FTA'] - row['FTM'], row['TOV'], row['GP'],
    )
    return f"{name} {season} Player Efficiency Rating: {value:.3f}"


# =====================================================================
# SECTION 7: CALCULATOR AND STATISTICS SCREEN FORMS
# =====================================================================
forms = {
    "True Shooting % (TS%)": makeCalcForm(pageCalc, "True Shooting % (TS%)",
        ["Points", "Field goal attempts", "Free throw attempts"], calcTS),
    "Effective FG% (eFG%)": makeCalcForm(pageCalc, "Effective FG% (eFG%)",
        ["Field goals made", "3-pointers made", "Field goal attempts"], calcEFG),
    "VORP": makeCalcForm(pageCalc, "Value Over Replacement Player (VORP)",
        ["Box +/-", "Total minutes played", "Team games played"], calcVORP),
    "Usage Rate (USG%)": makeCalcForm(pageCalc, "Usage Rate (USG%)",
        ["Field goals attempted", "Free throws attempted", "Turnovers", "Minutes played",
         "Team FGA", "Team FTA", "Team minutes", "Team turnovers"], calcUSG),
}

selectedCalc = tk.StringVar(value = "True Shooting % (TS%)")

def styleOptionMenu(widget):
    widget.configure(
        font = (FONT, 10, "bold"), bg = CARD, fg = TEXT,
        activebackground = "#E8EEF5", activeforeground = TEXT,
        bd = 0, padx = 12, pady = 7, cursor = "hand2",
        highlightthickness = 1, highlightbackground = BORDER, relief = "flat",
    )
    widget["menu"].configure(
        font = (FONT, 10), bg = CARD, fg = TEXT,
        activebackground = "#E8EEF5", activeforeground = TEXT,
        bd = 0, relief = "flat",
    )

def onPickCalc(name):
    forms[name].tkraise()

menuCalc = tk.OptionMenu(pageCalc, selectedCalc, *forms.keys(), command = onPickCalc)
menuCalc.place(relx = 0.5, rely = 0.05, anchor = "center")
styleOptionMenu(menuCalc)

onPickCalc(selectedCalc.get())

statsForms = {
    "True Shooting % (TS%)": makeStatsForm(pageStats, "True Shooting % (TS%)",
        ["Player name", "Season"], lookupTS),
    "Effective FG% (eFG%)": makeStatsForm(pageStats, "Effective FG% (eFG%)",
        ["Player name", "Season"], lookupEFG),
    "VORP": makeStatsForm(pageStats, "Value Over Replacement Player (VORP)",
        ["Player name", "Season", "Box +/-"], lookupVORP),
    "Usage Rate (USG%)": makeStatsForm(pageStats, "Usage Rate (USG%)",
        ["Player name", "Season"], lookupUSG),
    "Per 36 Minutes": makeStatsForm(pageStats, "Player Stats Per 36 Minutes",
        ["Player name", "Season"], lookupPer36),
    "Three Point Attempt Rate": makeStatsForm(pageStats, "Three Point Attempt Rate",
        ["Player name", "Season"], lookupThreePointRate),
    "Player Efficiency Rating (PER)": makeStatsForm(pageStats, "Player Efficiency Rating (PER)",
        ["Player name", "Season"], lookupPER),
}

selectedStats = tk.StringVar(value = "True Shooting % (TS%)")

def onPickStats(name):
    statsForms[name].tkraise()

menuStats = tk.OptionMenu(pageStats, selectedStats, *statsForms.keys(), command = onPickStats)
menuStats.place(relx = 0.5, rely = 0.05, anchor = "center")
styleOptionMenu(menuStats)

onPickStats(selectedStats.get())

# =====================================================================
# SECTION 8: START THE APP (keep these last)
# =====================================================================
showPage(pageCalc)

root.mainloop()