import nba_api

# does the TS% calculations
def tsper(points, fga, fta):
    tsa = fga + 0.44 * fta 
    if tsa == 0:
        return 0.0
    return points / (2 * tsa)

print("------------------------------------------------------------------")
print("The National Basketball Association Advanced Statistics Calculator")
print("------------------------------------------------------------------")
print("1) TS%")
print("2) eFG%")
choice = int(input("Choice: "))
# True Shooting Percentage Calculator
if choice == 1:
    points = int(input("Points?: "))
    fga = int(input("Field goal attempts?: "))
    fta = int(input("Free throw attempts?: "))
    ts = tsper(points, fga, fta)
    print(f"The TS% is: {ts:.1%}")