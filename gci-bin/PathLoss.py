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
#           txConnectorLosses
#           rxConnectorLosses
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
import json

cgitb.enable()


# Template location
TempPath = os.path.join("..", "Resources", "Templates", os.path.splitext(os.path.basename(__file__))[0] + ".html")


def calcAeGain(AntenanDiameter, frequency):
    return 17.8*20*math.log10(AntenanDiameter*frequency)

def calcFreSpaceLoss(distance, frequency):
    return -20*math.log10(4*3.142*distance*1000/(3/(frequency*10)))

def calcLinkAvailability(frequency, distance, fadeMargin):

    environmentalFactor = [2,0.3]

    return 1-(environmentalFactor[0]*environmentalFactor[1]
              *(math.pow(10,(-5)))*frequency*0.62/4*(math.pow(distance,3))*(math.pow(10,(-fadeMargin/10))))

def calcFresnelRadius(distance, frequency):
    return 17.32*math.sqrt((distance/(4*frequency)))

def fresnelShape(frequency,distance):

    sizeOfIncrument = 100
    incremument = distance/sizeOfIncrument
    print "incremument " , incremument
    pointDistance = 1
    pointcount = 0
    next_point = 0
    fresnelShape = []
    pointDistance = incremument


    for pointDistance in range(1,int(distance)):

        mantisa = float((300000000/(frequency*1000000000))*pointDistance*(pointDistance*1000-pointDistance))
        exponant = float(pointDistance+(pointDistance*1000-(pointDistance)))
        next_point  = float(math.sqrt(mantisa/exponant))

        print "mantisa/exponant ", mantisa/exponant
        print "next_point ", next_point

        fresnelShape.append({'xcoord':pointcount, 'pointDiameter' :next_point})

        pointDistance = pointDistance + incremument
        print "test data: " , pointDistance+incremument
        print "incremument " , incremument
        pointcount += 1

    return fresnelShape


def calcFarField(txAntenanDiameter, frequency):
    return (2*math.pow(txAntenanDiameter,2))/(300000000/(frequency*1000000000))

#frequency distance txAntenanDiameter rxAntenanDiameter txAntenanGain rxAntenanGain txPower rxSensetiviy
#txConnectorLosses rxConnectorLosses txCableLosses rxCableLosses

#18 23 1.2 1.2 23 23 10 -100 1 1 1 1


def main(pars):
    print "this is a test"
    global Tiles
    profilePoints = []
    frequency = 0
    distance  = 0
    txAntenanDiameter = 0
    rxAntenanDiameter = 0
    txAntenanGain = 0
    rxAntenanGain = 0
    txPower = 0
    rxSensetiviy = 0
    txConnectorLosses = 0
    rxConnectorLosses = 0
    txCableLosses = 0
    rxCableLosses = 0

    resp = ""
  #  error = frequency = distance = txAntenanDiameter = rxAntenanDiameter\
   #     = txAntenanGain = rxAntenanGain = txPower = rxSensetiviy = txCableLosses = rxCableLosses = None
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
        txAntenanGain = float(sys.argv[5])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required txAntenanGain parameter missing!</p>\n"
        pass

    try:
        # rxAntenanGain = float(pars.getvalue("rxAntenanGain"))
        rxAntenanGain = float(sys.argv[6])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required rxAntenanGain parameter missing!</p>\n"
        pass

    try:
        # txPower = float(pars.getvalue("txPower"))
        txPower = float(sys.argv[7])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required txPower parameter missing!</p>\n"
        pass

    try:
        # rxSensetiviy = float(pars.getvalue("rxSensetiviy"))
        rxSensetiviy = float(sys.argv[8])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required rxSensetiviy parameter missing!</p>\n"
        pass

    try:
        # txConnectorLosses = float(pars.getvalue("txConnectorLosses"))
        txConnectorLosses = float(sys.argv[9])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required txConnectorLosses parameter missing!</p>\n"
        pass

    try:
        # rxConnectorLosses = float(pars.getvalue("rxConnectorLosses"))
        rxConnectorLosses = float(sys.argv[10])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required rxConnectorLosses parameter missing!</p>\n"
        pass
    try:
        # txCableLosses = float(pars.getvalue("txCableLosses"))
        txCableLosses = float(sys.argv[11])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required txCableLosses parameter missing!</p>\n"
        pass

    try:
        # rxCableLosses = float(pars.getvalue("rxCableLosses"))
        rxCableLosses = float(sys.argv[12])
    except Exception:
        # error	= True
        # resp	+= "<p>ERROR: required rxCableLosses parameter missing!</p>\n"
        pass

    print "At the Start"

    powertAtRx = txPower + txConnectorLosses + txCableLosses + txAntenanGain + \
                calcFreSpaceLoss(distance, frequency) + rxAntenanGain + \
                 rxCableLosses + rxConnectorLosses

    print "powerattx %f.6"  , powertAtRx

    fadeMargine = -rxSensetiviy + powertAtRx

    fresnelRadius = calcFresnelRadius(distance, frequency)

    farFieldStart = calcFarField(txAntenanDiameter, frequency)

    profilePoints.append({'fadeMargin':fadeMargine,
                          'linkAvailability' :calcLinkAvailability(frequency, distance, -rxSensetiviy + powertAtRx),                        'farFieldStart':farFieldStart})

    profilePoints.append(fresnelShape(frequency,distance))

  #  print profilePoints
    print json.dumps(profilePoints , sort_keys=True, indent=4, separators=(',', ': '))

main(cgi.FieldStorage())
