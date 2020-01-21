import io

# This class will test your output against the given file list. This class will be OVERWRITTEN on our end.
# run the code?


import sys

# adjust location to your code
from keeble_erica.main.ColorText import *
from keeble_erica.main import MainStarter

CHECK_CAP = False
CHECK_LEFT_SPACING = False
CHECK_RIGHT_SPACING = False
CHECK_NEW_LINE = False


def printError(resultLine, ansLine):
    sys.stderr.write(">>>>>>>Error>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    sys.stderr.write("Got.....|")
    sys.stderr.write(resultLine + "|")
    if (not CHECK_RIGHT_SPACING or not CHECK_NEW_LINE):
        sys.stderr.write("\n")
    sys.stderr.write("Needed..|")
    sys.stderr.write(ansLine + "|")
    if (not CHECK_RIGHT_SPACING or not CHECK_NEW_LINE):
        sys.stderr.write("\n")


def cleanInput(lines, i):
    if (not CHECK_NEW_LINE):
        while (i < len(lines) and len(lines[i].strip()) == 0):
            i = i + 1

    line = lines[i]
    if not CHECK_CAP:
        line = line.lower()

    if not CHECK_LEFT_SPACING:
        line = line.lstrip()

    if not CHECK_RIGHT_SPACING:
        line = line.rstrip()

    return line, i


if len(sys.argv) > 1:
    tests = ["..\\tier1", "..\\tier2", "..\\tier3", "..\\tier4", "..\\tier5"
        , "..\\tier6" , "..\\tier7", "..\\tier8", "..\\tier9", "..\\tier10"]

    for base in tests:
        file = base + ".txt"
        outFile = base + "-student.out"
        answerFile = base + ".out"

        # redirect input and output
        output = open(outFile, "w")
        sys.stdout = output
        inf = open(file)
        input = "".join(inf.readlines())
        sys.stdin = io.StringIO(input)

        MainStarter.main()  # TODO you may need to adjust this to your code

        inf.close()
        output.close()

        answer = open(answerFile)
        result = open(outFile)

        sys.stderr.write(ColorText.fg.black + "\n\n\n\n\n\n" + ColorText.reset)
        sys.stderr.write(ColorText.fg.black +
                         "----------------------------" + base + "-----------------------------" + ColorText.reset + "\n")

        # check for a mismatch pass
        ansLines = answer.readlines()
        resultLines = result.readlines()
        error = False

        # check if any lines are different
        i = 0
        j = 0
        while i < len(ansLines) and j < len(resultLines):
            ansLine, i = cleanInput(ansLines, i)
            resultLine, j = cleanInput(resultLines, j)

            i = i + 1
            j = j + 1

            if ansLine != resultLine:
                error = True
                break

        # if I didn't complete parsing, there is extra lines in one file
        if i < len(ansLines) or j < len(resultLines):
            error = True

        # output pass, or the file with the problem lines
        if not error:
            sys.stderr.write(ColorText.fg.black + "Passed" + ColorText.reset + "")
        else:
            i = 0
            j = 0
            while i < len(ansLines) and j < len(resultLines):

                ansLine, i = cleanInput(ansLines, i)
                resultLine, j = cleanInput(resultLines, j)

                if ansLine == resultLine:
                    sys.stderr.write(ColorText.fg.black + ansLines[i] + ColorText.reset + "")
                else:
                    printError(resultLines[j], ansLines[i])

                i = i + 1
                j = j + 1

            while j < len(resultLines):
                printError(resultLines[j], "")
                j = j + 1

            while i < len(ansLines):
                printError("", ansLines[i])
                i = i + 1

    sys.exit()
