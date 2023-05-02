# oh-temperature-convertor
This repo contains code which translates temperatures originally calculated from OH*(6-2) transiton spectra using a certain set of Einstein coefficients to a new set of Einstein coefficients with no need of the original data.

This repo contains the following files;

ConversionFinal.ipynb : Jupyter notebook including plots and more explanation of the method
oh_einstein_temp_convert : Downloadable Python package which does the conversion on any list of temperatures

GSC,LG,MIES_QUANT.txt : Text files containing the necessary Einstein coefficient and quantum data, download them and put them in the same folder as the package or Jupyter notebook.


"""
Created: 2023-04-28

Author: Rowan Alethea Dayton-Oxland

Contact: R.A.Dayton-Oxland@soton.ac.uk

This script converts a OH*(6-2) temperature between different Einstein coefficients.

- Read in the temperature T1
- Calculate the line intensity I for each PA(B) using A1
- Fit using A2 log(I/A2*2(2J+1))
- Extract T2 assuming constant partition function 


INPUTS
---
Tin : Input temperature in Kelvin

Ain : Original Einstein coefficient source (see Tab)

Aout : Desired output Einstein coefficient source (see Tab)



TAB
---
    Einstein A Source            Code
    ---------------------------------
    Mies 1974                       0
    Loo and Groenenboom 2008        1
    GSC (?)                         2


OUTPUTS
---
Tout : The converted OH temperature for the new Einstein coefficient source


VARIABLES
---
Ain is the original Einstein coefficient

Aout is the new Einstein coefficient

Tin is the original output temperature

J2 is the rotational angular momentum of the excited/upper state

Partition is the value of the partition term ln(N/Qr)

Fprime is the rotational term in the upper state

PHYSICAL CONSTANTS
---
h is the Planck constant

c is the speed of light in a vaccuum

k is the Boltzmann constant

UPDATES
---

"""
