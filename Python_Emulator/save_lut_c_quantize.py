# This code is a revised version of LUT Conversion Tool of AdaPT TEAM. The link of their code is https://github.com/dimdano/adapt/blob/main/tools/LUT_convert.ipynb
#
#  Revised By: Amirhossein Zarei
#
#  Project: Reconfigurable MAC
#
#  Creation Date: 2023-06-14
#
#  Description: reconfig_mac emulates approximate MAC calculation in our
#               new FPGA-based reconfigurable MAC architecture.
#---------------------------------------------------------------------------

import numpy as np
from Emulated_Approx_Functions import Approx_Multiply
from Emulated_Approx_Functions import Quantized_Multiply

#Make a .h file containg Approximate Multiplier LUT
def Save_LUT_C_QUANTIZE():
  nbits=8
  qbits=2
  with open('Output_Files\LUT_C'+'.h', 'w') as myfile:
    bits = int(pow(2,nbits))
    lut_size_str = str(bits)

    myfile.write('#include <stdint.h>\n\n')
    myfile.write('const int' + str(2*nbits) + '_t lut [' + lut_size_str + '][' + lut_size_str +'] = {')

    for i in range (0,bits//2):
      myfile.write('{')
      for j in range (0,bits//2):
        x = int(Quantized_Multiply(i,j,qbits) *  pow(pow(2,qbits),2))
        myfile.write('%s' % x)
        myfile.write(', ')
      for j in range (bits//2,bits):
        #x = int(Approx_Multiply(i,(bits-j)*-1) * 128)
        x = int(Quantized_Multiply(i,(bits-j)*-1,qbits)  * pow(pow(2,qbits),2))

        myfile.write('%s' % x)
        if j!=bits-1:
          myfile.write(', ')
      myfile.write('},')
      myfile.write('\n')

    for i in range (bits//2,bits):
        myfile.write('{')
        for j in range (0,bits//2):
            #x = int(Approx_Multiply((bits-i)*-1,j) * 128)
            x = int(Quantized_Multiply((bits-i)*-1,j,qbits) * pow(pow(2,qbits),2))

            myfile.write('%s' % x)
            myfile.write(', ')
        for j in range (bits//2,bits):
            #x = int(Approx_Multiply((bits-i)*-1,(bits-j)*-1) * 128)
            x = int(Quantized_Multiply((bits-i)*-1,(bits-j)*-1,qbits) * pow(pow(2,qbits),2))
            myfile.write('%s' % x)
            if j!=bits-1:
                myfile.write(', ')
        if(i!=bits-1):
            myfile.write('},')
            myfile.write('\n')
    myfile.write('}};\n')
  return