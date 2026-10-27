# N.B.A.A.S.C

## The National Basketball Association Advanced Statistics Calculator

A calculator for advanced stats for basketball. You can either calculate using your own stats, or look them up using the nba_api library. Note that some stats are available only with the lookup, either due to their nature (such as with team based stats) or because I just haven't gotten to adding them to the manual calculations.

### Install Tutorial

1. Clone using the command:

  ```bash
  git clone https://github.com/KermitTheMagnificant/N.B.A.A.S.C
  ```
2. Install nba_api if you don't already have it:

  ```bash
  pip install nba_api
  ```
3. Finally, run the program (when in the directory of the file, of course)! There is currently no loop, so for each calculation, you will have to run it again.

  ```bash
  python3 main.py
  ```
### Current Features

TS%, eFG%, VORP, USG%, player lookup for TS% and eFG%, VORP, USG%, Per 36 Stats, and 3 point attempt rate.

### Planned Features

More stats, a leaderboard for players' advanced stats (e.g., who led in TS% this week?), and a GUI.
