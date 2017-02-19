#!python
#
#
#
#
#
#  Inputs:  frequency
#           distance
#           txAntenanDiameter
#           rxAntenanDiameter
#           txAntenanGain
#           rxAntenanGain
#           txPower
#           rxSensetiviy
#           txCableLosses
#           rxCableLosses
#
#
#  Calculated Fields:
#           freeSpaceLoss
#           powerAtRx
#           fadeMargin
#           linkAvailability
#           fresnelRadius
#           fresnelRadiusPoints[]
#           angleTo MidPointfresnel
#           farFieldStart
#
#
#

import os
import sys

import cgi
import cgitb
import math

cgitb.enable()


# Template location
TempPath = os.path.join("..", "Resources", "Templates", os.path.splitext(os.path.basename(__file__))[0] + ".html")




def calcAeGain(radius, frequency):
    return 17.8*20*math.log10(radius*frequency)

def calcLinkAvailability(a, b, frequency, distance, fadeMargin):
    return 1-(a*b*(10^(-5))*frequency*0.62/4*(distance^3)*(10^(-fadeMargin/10)))

def calcFreSpaceLoss(distance, frequency):
    return 20*math.log10(4*3.142*distance*1000/(3/(frequency*10)))


def fresnelRadius(distance, frequency):
    return 17.32*math.sqrt((distance/(4*frequency)))

def fresnelShape(frequency,distance, u):

    incremument = distance/100
    pointDistance = 0
    pointCount = 0
    fresnelShape = []

    for pointDistance in range(distance):
        next_point  = math.sqrt(((300000000/(frequency*1000000000))*u*(pointDistance*1000-u))/(u+(pointDistance*1000-(u))))
        fresnelShape.append({'xcoord':pointCount, 'pointDiameter' :next_point})

        pointDistance += incremument
        ++pointCount

    return fresnelShape


def farField(txAntenanDiameter, frequency):
    return (2*txAntenanDiameter^2)/(300000000/(frequency*1000000000))




def main(pars):
    global Tiles
    profilePoints = []

    resp = ""
    error = frequency = distance = txAntenanDiameter = rxAntenanDiameter\
        = txAntenanGain = rxAntenanGain = txPower = rxSensetiviy = txCableLosses = rxCableLosses = None
    args = sys.argv[1:]

    print ' '.join(args)
    try:
        # frequency = float(pars.getvalue("frequency"))
        frequency = float(sys.argv[1])
    except Exception:
        error = True
        resp += "<p>ERROR: required frequency parameter missing!</p>\n"

    try:
        # distance = float(pars.getvalue("distance"))
        distance = float(sys.argv[2])
    except Exception:
        error = True
        resp += "<p>ERROR: required distance parameter missing!</p>\n"

    try:
        # txAntenanDiameter = float(pars.getvalue("txAntenanDiameter"))
        txAntenanDiameter = float(sys.argv[3])
    except Exception:
        error = True
        # resp	+= "<p>ERROR: required txAntenanDiameter parameter missing!</p>\n"
        pass

    try:
        # rxAntenanDiameter = float(pars.getvalue("rxAntenanDiameter"))
        rxAntenanDiameter = float(sys.argv[4])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required rxAntenanDiameter parameter missing!</p>\n"
        pass

    try:
        # txAntenanGain = float(pars.getvalue("txAntenanGain"))
        txAntenanGain = float(sys.argv[4])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required txAntenanGain parameter missing!</p>\n"
        pass

    try:
        # rxAntenanGain = float(pars.getvalue("rxAntenanGain"))
        rxAntenanGain = float(sys.argv[4])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required rxAntenanGain parameter missing!</p>\n"
        pass

    try:
        # txPower = float(pars.getvalue("txPower"))
        txPower = float(sys.argv[4])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required txPower parameter missing!</p>\n"
        pass

    try:
        # rxSensetiviy = float(pars.getvalue("rxSensetiviy"))
        rxSensetiviy = float(sys.argv[4])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required rxSensetiviy parameter missing!</p>\n"
        pass

    try:
        # txCableLosses = float(pars.getvalue("txCableLosses"))
        txCableLosses = float(sys.argv[4])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required txCableLosses parameter missing!</p>\n"
        pass

    try:
        # rxCableLosses = float(pars.getvalue("rxCableLosses"))
        rxCableLosses = float(sys.argv[4])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required rxCableLosses parameter missing!</p>\n"
        pass



    profilePoints.append({'fadeMargin':fadeMargin,
                          'linkAvailability' :calcLinkAvailability(a, b, frequency, distance, rxSensetiviy+powerAtRx),
                          'farFieldStart':farFieldStart})

    profilePoints.append({'fresnelShape':fresnelShape(frequency,distance, u)})


    print json.dumps(profilePoints)
