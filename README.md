 PathLoss

This program calculate the signal PathLoss of a signal between the Tx and Rx.  
Additionally it will calculate:
    The anticipated availablility of the path, 
    The fresnel zone dimentions and the point at which the far field is established.
  
  Inputs:  
    The units of the input fields are:
       frequency           Ghz  
       distance            Km
       txAntennaDiameter   m   Used to calculate the start of the far field
       rxAntennaDiameter   m   Used to calculate the start of the far field
       txAntennaGain       dB
       rxAntennaGain       dB
       txPower             dB
       rxSensetivity      -dB
       txConnectorLosses   dB  The total losses due to connectors
       rxConnectorLosses   dB  The total losses due to connectors
       txCableLosses       dB  The total losses in the connecting cables
       rxCableLosses       dB  The total losses in the connecting cables


  Calculated Fields:
           freeSpaceLoss
           powerAtRx
           fadeMargin
           linkAvailability
           fresnelRadius
           fresnelRadiusPoints[]
           farFieldStart

   Output:
           fadeMargin
           linkAvailability
           farFieldStart
           fresnelRadius
           fresnelRadiusPoints[]
