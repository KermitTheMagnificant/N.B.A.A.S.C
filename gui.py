import tkinter as tk
from main import tsper, efgper, vorpcalc, usgcalc

# =====================================================================
# SECTION 1: WINDOW SETUP
# =====================================================================
root = tk.Tk()

root.title("National Basketball Association Advanced Statistics Calculator")
root.geometry("500x600")

# =====================================================================
# SECTION 2: THE THREE SCREENS (frames stacked in the same spot)
# =====================================================================
pageCalc = tk.Frame(root)
pageStats = tk.Frame(root)
pageLeader = tk.Frame(root)

for page in (pageCalc, pageStats, pageLeader):
    page.place(relx = 0, rely = 0.15, relwidth = 1, relheight = 0.85)

# placeholder content for the screens we haven't built yet
tk.Label(pageStats, text = "Statistics screen", font = ("Arial", 16)).pack(pady = 20)
tk.Label(pageLeader, text = "Leaderboard screen", font = ("Arial", 16)).pack(pady = 20)

# =====================================================================
# SECTION 3: SCREEN SWITCHING AND THE TOP BUTTONS
# =====================================================================
def showPage(page):
    page.tkraise()

buttonCalc = tk.Button(root, text = "Calculator", command = lambda: showPage(pageCalc))
buttonCalc.place(relx = 0.1, rely = 0.08, anchor = "center")

buttonStats = tk.Button(root, text = "Statistics", command = lambda: showPage(pageStats))
buttonStats.place(relx = 0.3, rely = 0.08, anchor = "center")

buttonLeader = tk.Button(root, text = "Leaderboard", command = lambda: showPage(pageLeader))
buttonLeader.place(relx = 0.5, rely = 0.08, anchor = "center")

# =====================================================================
# SECTION 4: CALCULATOR SCREEN - form-building helper
# =====================================================================
def makeCalcForm(parent, title, fields, calculate):
    frame = tk.Frame(parent)
    frame.place(relx = 0, rely = 0.12, relwidth = 1, relheight = 0.88)
    tk.Label(frame, text = title, font = ("Arial", 14)).pack(pady = 10)

    entries = []
    for labelText in fields:
        tk.Label(frame, text = labelText).pack()
        entry = tk.Entry(frame)
        entry.pack()
        entries.append(entry)

    labelResult = tk.Label(frame, text = "", font = ("Arial", 14))

    def onClick():
        try:
            values = [float(e.get()) for e in entries]
        except ValueError:
            labelResult.config(text = "Please enter numbers only.")
            return
        labelResult.config(text = calculate(*values))

    tk.Button(frame, text = "Calculate", command = onClick).pack(pady = 10)
    labelResult.pack()
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
# SECTION 6: CALCULATOR SCREEN - build the forms and the dropdown
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

def onPickCalc(name):
    forms[name].tkraise()

menuCalc = tk.OptionMenu(pageCalc, selectedCalc, *forms.keys(), command = onPickCalc)
menuCalc.place(relx = 0.5, rely = 0.05, anchor = "center")

onPickCalc(selectedCalc.get())

# =====================================================================
# SECTION 7: START THE APP (keep these last)
# =====================================================================
showPage(pageCalc)

root.mainloop()