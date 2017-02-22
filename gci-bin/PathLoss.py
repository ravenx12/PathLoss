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

def calcAeGain(AntenanDiameter, frequency):
    return 17.8+20*math.log10(AntenanDiameter*frequency)

def calcFreSpaceLoss(distance, frequency):
    return -20*math.log10(4*3.142*distance*1000/(3/(frequency*10)))

def calcLinkAvailability(frequency, distance, fadeMargin):

    environmentalFactor = [2,0.3]

    return 1-(environmentalFactor[0]*environmentalFactor[1]
              *(math.pow(10,(-5)))*frequency*0.62/4*(math.pow(distance,3))*(math.pow(10,(-fadeMargin/10))))

def calcFresnelRadius(distance, frequency):

    frezrad =  17.32*math.sqrt((distance/(4*frequency)))
   # print "frezrad " ,frezrad

    return frezrad

def fresnelShape(frequency,distance):

    sizeOfIncrument = 100
    Increment = distance/sizeOfIncrument
    pointDistance = 1
    pointcount = 0
    next_point = 0
    fresnelShape = []
    pointDistance = Increment

#http://www.4gon.co.uk/solutions/technical_fresnel_zones.php
    while pointDistance < distance-Increment:
        mantisa = float((3/(frequency))*pointDistance*(distance-pointDistance))
        exponant = float(pointDistance+(distance-(pointDistance)))
        next_point  = round(10* float(math.sqrt(mantisa/exponant)),3)

        fresnelShape.append({'pointDistance':round(pointDistance,3), 'pointDiameter' :next_point})

        pointDistance = pointDistance + Increment
      #  print "test data: " , pointDistance
      #  print "Increment " , Increment
      #  print "pointcount " , pointcount
        pointcount += 1

    return fresnelShape


def calcFarField(txAntenanDiameter, frequency):
    return (2*math.pow(txAntenanDiameter,2))/(3/(frequency*10))

#frequency distance txAntenanDiameter rxAntenanDiameter txAntenanGain rxAntenanGain txPower rxSensetiviy
#txConnectorLosses rxConnectorLosses txCableLosses rxCableLosses
# Test Data args
#18 26.083 1.8 0.8 48.0109 40.96725 15 -100 0 0 0 0

def main(pars):

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

   # print ' '.join(args)
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


    powertAtRx = round(txPower - txConnectorLosses - txCableLosses + txAntenanGain + \
                calcFreSpaceLoss(distance, frequency) + rxAntenanGain - \
                 rxCableLosses - rxConnectorLosses,3)


   # print "TX AE Gain " , calcAeGain(txAntenanDiameter, frequency)
   # print "RX AE Gain " , calcAeGain(rxAntenanDiameter, frequency)

    fadeMargine = round(-rxSensetiviy + powertAtRx,3)

    fresnelradius = round(calcFresnelRadius(distance, frequency),3)

    farFieldStart = round(calcFarField(txAntenanDiameter, frequency),3)

    linkCalculations = {'fadeMargin':fadeMargine,
                          'linkAvailability' :round(calcLinkAvailability(frequency, distance, -rxSensetiviy + powertAtRx),3),
                          'farFieldStart':farFieldStart,
                          'Fresnel Radius':fresnelradius}

    fresnelArray = fresnelShape(frequency,distance)

    data = {"fresnelArray":fresnelArray, "linkCalculations":linkCalculations }
  #  print profilePoints
    print json.dumps(data , sort_keys=True, indent=2, separators=(',', ': '))

main(cgi.FieldStorage())

