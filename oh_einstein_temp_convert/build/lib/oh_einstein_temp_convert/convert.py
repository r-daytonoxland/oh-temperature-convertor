#!/usr/bin/env python
# coding: utf-8
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
Tin : Input temperature in Kelvin as a list [Tin]
Ain : Original Einstein coefficient source (see Tab)
Aout : Desired output Einstein coefficient source (see Tab)


TAB
---
    Einstein A Source            Code
    ---------------------------------
    Mies 1974                       0
    Loo and Groenenboom 2008        1
    GSC                             2


OUTPUTS
---
Tout : The converted OH temperature list for the new Einstein coefficient source


VARIABLES
---
Ain is the original Einstein coefficient source
Aout is the new Einstein coefficient source
Tin is the original temperature as a list
J2 is the rotational angular momentum of the excited/upper state
partition is the value of the partition term ln(N/Qr)
Fprime is the rotational term in the upper state

PHYSICAL CONSTANTS
---
h is the Planck constant
c is the speed of light in a vaccuum
k is the Boltzmann constant

UPDATES
---

"""

# # Initialisation and Data Read

import numpy as np
import pandas as pd
from pathlib import Path

# Identify filepaths to each set of Einstein coefficients
data_dir = Path(__file__).parent/'data'
file_paths = ["MIES_QUANT.txt", "LG_QUANT.txt", "LWR_QUANT.txt", "GSC_QUANT.txt", "TL_QUANT.txt"]
file_paths = [data_dir/f for f in file_paths]

# PHYSICAL CONSTANTS
h = 6.62607015e-34  # Planck constant in J·s
c = 2.99792458e8  # Speed of light in m/s
k = 1.380649e-23  # Boltzmann constant in J/K

# TRANSITION CONSTANTS
partition = 6.30163002356721E+0000  # From Values.txt in Synthetic OH

# VIBROTATIONAL CONSTANTS FOR v = 6
Y = -9.795
D = 0.0018
B = 14.349


def read_fredquantfile(file_path):
    """
    Reads data from a Fred file containing information about the OH(6-2)* transition. The file is provided as a text file
    named 'MIES_QUANT.INC', and should contain only the required information for the OH(6-2)* transition. Any non-required
    information should be commented out with a double slash (//) at the beginning of the line.

    Parameters:
    file_path (str): The path of the text file containing the required data.

    Returns:
    pandas.DataFrame: A DataFrame containing the extracted information, including the symbol, wavelength, Jprime, and A values
    for the OH(6-2)* transition.
    """

    with open(file_path, "r") as file:
        data = file.readlines()

    # Initialize lists to store extracted information
    wavelengths = []
    j2_values = []
    a_values = []
    symbols = []

    # Iterate through each line and extract required information
    for line in data:

        if line.startswith("//"):  # ignore // lines
            continue

        if line.startswith("  "):
            continue

        if "v2" not in line:
            continue

        wavelength = int(line.split()[0].strip(":"))
        j2_value = float(line.split("J2:=")[1].split(";")[0].strip())
        a_value = float(line.split("A:=")[1].split(";")[0].strip())
        symbol = line.split("symbol:='")[1].split("';")[0].strip()

        wavelengths.append(wavelength)
        j2_values.append(j2_value)
        a_values.append(a_value)
        symbols.append(symbol)

    quant = pd.DataFrame(
        {
            "Symbol": symbols,
            "Wavelength": wavelengths,
            "Jprime": j2_values,
            "A": a_values,
        }
    )

    return quant


def get_fprime(quant, B, D, Y):
    """
    Calculates the values of F(J') (Fprime) for the OH(6-2)* transition using the vibrational-rotational constants and Jprime values
    extracted from the input DataFrame.

    Parameters:
    quant (pandas.DataFrame): A DataFrame containing the extracted information from Fredware,
        including the symbol, wavelength, Jprime, and A values
        for the OH(6-2)* transition.
    B (float): The rotational constant for the transition.
    D (float): The centrifugal distortion constant for the transition.
    Y (float): The vibrational-rotational coupling constant for the transition.

    Returns:
    Fprime (list): A list containing the calculated Fprime values for the OH(6-2)* transition.
    """

    Fprime = []
    Jprime = quant["Jprime"]

    for i in range(len(quant)):

        if int(quant["Symbol"][i][1]) == 1:
            F_value = 100 * (
                B
                * (
                    (Jprime[i] + 0.5) ** 2
                    - 1
                    - (0.5 * np.sqrt(4 * (Jprime[i] + 0.5) ** 2 + Y * (Y - 4)))
                )
                - D * (Jprime[i] ** 4)
            )
            Fprime.append(F_value)

        elif int(quant["Symbol"][i][1]) == 2:
            F_value = 100 * (
                B
                * (
                    (Jprime[i] + 0.5) ** 2
                    - 1
                    + (0.5 * np.sqrt(4 * (Jprime[i] + 0.5) ** 2 + Y * (Y - 4)))
                )
                - D * (Jprime[i] ** 4)
            )
            Fprime.append(F_value)

    return Fprime


def get_parameters(Ain: str, Aout: str) -> pd.DataFrame:
    """
    Reads data from the input and output files and returns a DataFrame
    containing the necessary data for further calculations.

    Args:
        Ain: str, path to the input file
        Aout: str, path to the output file

    Returns:
        pd.DataFrame, a DataFrame containing the necessary data for calculations
    """

    # Read the input and output files
    quant = read_fredquantfile(file_paths[Ain])
    new_quant = read_fredquantfile(file_paths[Aout])

    # Rename columns for clarity
    quant.rename(columns={"A": "Ain"}, inplace=True)

    # Add Aout column to the quant DataFrame
    quant["Aout"] = new_quant["A"]

    # Calculate Fprime using the given parameters
    Fprimes = get_fprime(quant, B, D, Y)
    Fprime = pd.DataFrame(Fprimes, columns=["Fprime"])

    # Merge Fprime and quant DataFrames
    parameters = pd.merge(Fprime, quant, left_index=True, right_index=True)

    return parameters

def convert_temperatures(Tin, Ain, Aout):
    """
    Calculates the output temperature (Tout) based on the input temperature (Tin),
    and the input and output Einstein coefficients (Ain and Aout).

    Args:
        Tin: float, input temperature
        Ain: str, path to the input Einstein coefficients file
        Aout: str, path to the output Einstein coefficients file

    Returns:
        float, output temperature

    Works by fitting this linear equation;
        y = np.log( I / (A1 * (2 * ((2 * J2) + 1))))
        x = FJprime # The x axis of the gradient plot
        m = -(h * c)/(k * T1) # is the gradient based on T1
        c = np.log( N / QR) # is the partition term and y-intercept
    and adding a correction term = ln(Ain/Aout)
    """

    parameters = get_parameters(Ain, Aout)

    # # Conversion calculation

    Tout = []

    for j in range(len(Tin)):
    
        x = []  # Empty lists for the x and y values of the fitlines
        y = []

        for i in range(len(parameters)):

            x.append(parameters["Fprime"][i])  # x is just the Fprime values
            y.append(
                ((-h * c) / (k * Tin[j])) * x[i]  # from the equation of the line
                + partition
                + np.log(
                    parameters["Ain"][i] / parameters["Aout"][i]
                )  # correction term
            )
        
        # Use line fitting to extract the gradient
        grad_poly, inter_poly = np.polyfit(x, y, 1)

        # Calculate the temperature from the line gradient
        temp = (-h * c) / (k * grad_poly)
        Tout.append(temp)

    return(Tout)
