import graphics as gfx

import math
from pathlib import Path

import common

_PATH = "../res/highscores.txt"

def _highscoresExist():
    path = Path(_PATH)
    return path.is_file()


def _createFile():
    open(_PATH, "w").close()


def _loadScores():
    '''Loads the raw data from the highscore file'''
    if not _highscoresExist():
        _createFile()

    with open(_PATH) as inFile:
        data = inFile.read()
    return data

def _writeScores(scores):
    '''Writes list of tuple(name, score) to the highscore file'''
    with open(_PATH, "w") as outFile:
        for nameScore in scores:
            #Writes the tuple to the file, with a space between the elements
            outFile.write(" ".join(str(x) for x in nameScore) + "\n")

def _extractScores(data):
    '''Extracts the highscores, and returns a list of tuple(name, score)'''
    highscores = []
    data = data.split()
    for i in range(0, len(data) - 1, 2):
        pair = (data[i], int(data[i + 1]))
        highscores.append(pair)
    return highscores

def _getScoresList():
    return _extractScores(_loadScores())

def submitScore(name, score):
    '''Adds a score to the highscores'''
    highscores = _getScoresList()
    highscores.append((name, score))
    highscores = sorted(highscores, key = lambda x: x[1])
    highscores = highscores[::-1]
    _writeScores(highscores)

def createHighscoresDisplay(window):
    '''Creation of the GUI for the highscores screen'''
    highscores = _getScoresList()
    sprites = []

    #Create title bar
    sprites.append(common.createTitle("HIGHSCORES"))

    gap = common.WINDOW_WIDTH / 4
    rankXLocation  = gap
    nameXLocation  = gap * 2
    scoreXLocation = gap * 3
    colours = ["tan1", "chocolate1"] * (len(highscores) // 2 + 1)
    for i in range(len(highscores)):
        rank  = str(i + 1)
        name  = str(highscores[i][0])
        score = str(highscores[i][1])
        y     = i * 20 + 100 + 10
        rect = gfx.Rectangle(gfx.Point(0, y - 10), gfx.Point(common.WINDOW_WIDTH, y + 10))
        rect.setFill(colours[i])
        sprites.append(rect)
        sprites.append(gfx.Text(gfx.Point(rankXLocation,  y), rank))
        sprites.append(gfx.Text(gfx.Point(nameXLocation,  y), name))
        sprites.append(gfx.Text(gfx.Point(scoreXLocation, y), score))
        if i + 1 == 25:
            break

    common.drawList(sprites, window)
    return sprites