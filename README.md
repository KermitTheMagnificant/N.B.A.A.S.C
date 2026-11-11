# N.B.A.A.S.C
# AS OF 11/11/26 THERE IS A BUG WHICH PREVENTS THE GUI FROM BEING LAUNCHED
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
4. To be able to run the program anywhere in Linux, run the 'install.sh' file

```bash
./install.sh
```

5. Then, run the GUI from anywhere using the name of the program.

```bash
nbaasc
```
NOTE: This only works on Linux as of 11/11/2026
### Current Features

TS%, eFG%, VORP, USG%, player lookup for TS% and eFG%, VORP, USG%, Per 36 Stats, 3 Point Attempt Rate, and Player Efficiency Rating.
There is also a weekly statistic leaderboard, where you can see the leaders in PPG, RPG, APG, True Shooting Percentage, and Efficient Field goal Percentage.

There is also now a gui, which you can run with:

```bash
python3 gui.py
```

The GUI includes calculator and player-stat lookup screens, plus a weekly leaderboard for PPG, RPG, APG, TS%, and eFG%. The leaderboard can be refreshed from the Leaderboard screen and loads results without blocking the interface.

### Planned Features

More stats, if you have any recs, please reach out (im out of ideas :p)
