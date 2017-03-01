#!/usr/bin/python

#  Inputs:  
#       frequency           Ghz
#       distance            Km
#       txAntennaDiameter   m
#       rxAntennaDiameter   m
#       txAntennaGain       dB
#       rxAntennaGain       dB
#       txPower             watts
#       rxSensetivity        dB
#       txConnectorLosses   dB
#       rxConnectorLosses   dB
##      txCableLosses       dB
#       rxCableLosses       dB
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

#cgitb.enable()

def calcAeGain(AntenanDiameter, frequency):
    return 17.8+20*math.log10(AntenanDiameter*frequency)

def calcFreSpaceLoss(distance, frequency):
    return -20*math.log10(4*3.142*distance*1000/(3/(frequency*10)))

def calcLinkAvailability(frequency, distance, fadeMargin):
    environmentalFactor = [2,0.3]
    return 1-(environmentalFactor[0]*environmentalFactor[1]*(math.pow(10,(-5)))*frequency*0.62/4*(math.pow(distance,3))*(math.pow(10,(-fadeMargin/10))))

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
        pointcount += 1

    return fresnelShape

def calcFarField(txAntennaDiameter, frequency):
    return (2*math.pow(txAntennaDiameter,2))/(3/(frequency*10))

#frequency distance txAntennaDiameter rxAntennaDiameter txAntennaGain rxAntennaGain txPower rxSensetivity
#txConnectorLosses rxConnectorLosses txCableLosses rxCableLosses
# Test Data args
#18 26.083 1.8 0.8 48.0109 40.96725 15 -100 0 0 0 0

def main(pars):
    global Tiles
    profilePoints = []
    frequency = 0
    distance  = 0
    txAntennaDiameter = 0
    rxAntennaDiameter = 0
    txAntennaGain = 0
    rxAntennaGain = 0
    txPower = 0
    rxSensetivity = 0
    txConnectorLosses = 0
    rxConnectorLosses = 0
    txCableLosses = 0
    rxCableLosses = 0
    error = False

    resp = ""
    #  error = frequency = distance = txAntennaDiameter = rxAntennaDiameter\
    #     = txAntennaGain = rxAntennaGain = txPower = rxSensetivity = txCableLosses = rxCableLosses = None
    #args = sys.argv[1:]

    # print ' '.join(args)
    try:
        frequency = float(pars["frequency"].value)
        #frequency = float(sys.argv[1])
    except Exception:
        error = True
        resp += "<p>ERROR: required frequency parameter missing!</p>\n"
        pass
    
    try:
        distance = float(pars["distance"].value)
        #distance = float(sys.argv[2])
    except Exception:
        error = True
        resp += "<p>ERROR: required distance parameter missing!</p>\n"
        pass

    try:
        txAntennaDiameter = float(pars["txAntennaDiameter"].value)
        #txAntennaDiameter = float(sys.argv[3])
    except Exception:
        error = True
        resp	+= "<p>ERROR: required txAntennaDiameter parameter missing!</p>\n"
        pass

    try:
        rxAntennaDiameter = float(pars["rxAntennaDiameter"].value)
        #rxAntennaDiameter = float(sys.argv[4])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required rxAntennaDiameter parameter missing!</p>\n"
        pass

    try:
        txAntennaGain = float(pars["txAntennaGain"].value)
        #txAntennaGain = float(sys.argv[5])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required txAntennaGain parameter missing!</p>\n"
        pass

    try:
        rxAntennaGain = float(pars["rxAntennaGain"].value)
        #rxAntennaGain = float(sys.argv[6])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required rxAntennaGain parameter missing!</p>\n"
        pass

    try:
        txPower = float(pars["txPower"].value)
        #txPower = float(sys.argv[7])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required txPower parameter missing!</p>\n"
        pass

    try:
        rxSensetivity = float(pars["rxSensetivity"].value)
        #rxSensetivity = float(sys.argv[8])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required rxSensetivity parameter missing!</p>\n"
        pass

    try:
        txConnectorLosses = float(pars["txConnectorLosses"].value)
        #txConnectorLosses = float(sys.argv[9])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required txConnectorLosses parameter missing!</p>\n"
        pass

    try:
        rxConnectorLosses = float(pars["rxConnectorLosses"].value)
        #rxConnectorLosses = float(sys.argv[10])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required rxConnectorLosses parameter missing!</p>\n"
        pass

    try:
        txCableLosses = float(pars["txCableLosses"].value)
        #txCableLosses = float(sys.argv[11])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required txCableLosses parameter missing!</p>\n"
        pass

    try:
        rxCableLosses = float(pars["rxCableLosses"].value)
        #rxCableLosses = float(sys.argv[12])
    except Exception:
        error	= True
        resp	+= "<p>ERROR: required rxCableLosses parameter missing!</p>\n"
        pass

    if error:
        print "Content-Type: application/json\n\n"
        print resp
    else:
        powertAtRx = round(txPower - txConnectorLosses - txCableLosses + txAntennaGain + \
        calcFreSpaceLoss(distance, frequency) + rxAntennaGain - \
        rxCableLosses - rxConnectorLosses,3)

        fadeMargine = round(-rxSensetivity + powertAtRx,3)

        fresnelradius = round(calcFresnelRadius(distance, frequency),3)

        farFieldStart = round(calcFarField(txAntennaDiameter, frequency),3)

        linkCalculations = {'fadeMargin':fadeMargine,
                'linkAvailability' :round(calcLinkAvailability(frequency, distance, -rxSensetivity + powertAtRx),3),
                'farFieldStart':farFieldStart,
                'fresnelRadius':fresnelradius}

        fresnelArray = fresnelShape(frequency,distance)

        data = {"fresnelArray":fresnelArray, "linkCalculations":linkCalculations }
        print "Content-Type: application/json\n\n"
        print json.dumps(data , sort_keys=True, indent=2, separators=(',', ': '))

main(cgi.FieldStorage())
