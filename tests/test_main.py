import unittest

from main import compareStatRows


class CompareStatRowsTests(unittest.TestCase):
    def test_true_shooting_compare(self):
        row1 = {"PTS": 80, "FGA": 60, "FTA": 20}
        row2 = {"PTS": 100, "FGA": 80, "FTA": 25}

        left, right = compareStatRows("1", row1, row2)

        self.assertAlmostEqual(left, 0.5813953488372093, places=6)
        self.assertAlmostEqual(right, 0.5494505494505495, places=6)

    def test_effective_fg_compare(self):
        row1 = {"FGM": 30, "FG3M": 10, "FGA": 60}
        row2 = {"FGM": 40, "FG3M": 12, "FGA": 80}

        left, right = compareStatRows("2", row1, row2)

        self.assertAlmostEqual(left, 0.5833333333333333, places=6)
        self.assertAlmostEqual(right, 0.575, places=6)

    def test_usage_compare(self):
        row1 = {"FGA": 20, "FTA": 8, "TOV": 4, "MIN": 40}
        row2 = {"FGA": 15, "FTA": 6, "TOV": 3, "MIN": 35}
        team1 = {"FGA": 90, "FTA": 40, "TOV": 18, "MIN": 240}
        team2 = {"FGA": 100, "FTA": 35, "TOV": 17, "MIN": 240}

        left, right = compareStatRows("4", row1, row2, team1, team2)

        self.assertAlmostEqual(left, 131.465, places=3)
        self.assertAlmostEqual(right, 106.335, places=3)


if __name__ == "__main__":
    unittest.main()
