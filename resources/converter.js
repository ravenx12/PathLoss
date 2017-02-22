
//This function simply takes in power
// and returns the decibel value
function dbConvert(power)
{
    dB = 10*Math.log10( power/1);
    return dB;
}

//This function  takes in decibel
// and returns the power value
function powerConvert(dB)
{
    power = math.power(10,D7/10);
    return power;
}

