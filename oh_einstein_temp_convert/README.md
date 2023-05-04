# oh_einstein_temp_convert

oh_einstein_temp_convert is a Python package which translates temperatures originally calculated from OH*(6-2) transiton spectra using a certain set of Einstein coefficients to a new set of Einstein coefficients with no need of the original data.

### Author
Rowan Dayton-Oxland
[University of Southampton](https://www.southampton.ac.uk/people/5z2prx/miss-rowan-dayton-oxland)
[Github](https://github.com/r-daytonoxland)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install oh_einstein_temp_convert.

```bash
pip install oh_einstein_temp_convert
```

## Requirements
- Python >= 3.10
- numpy, pandas
- OS independent

## Einstein A coefficient sources
 
**Ain** (int) - Original Einstein coefficient source index (see table)  
**Aout** (int) - Desired output Einstein coefficient source index (see table)  

| Einstein A Source            | Index |
|:-------------------------    |:------|
| Mies et al., 1974            | 0     |
| Loo and Groenenboom, 2008    | 1     |
| Langhoff et al., 1986        | 2     |
| Goldman et al., 1998         | 3     |
| Turnbull and Lowe, 1989      | 4     |

## Usage

```python
import oh_einstein_temp_convert as oh

Temperatures = []  # List of temperatures

# Temperatures originally calculated from e.g. Mies et al., 1974 coefficients
Ain_index = 0  # Choose index of input temperatures
# Output temperatures calculated from e.g. Loo and Groenenboom, 2008 coefficients. 
Aout_index = 1  # Choose index of output temperatures

# returns list of converted temperatures
Result = oh.convert_temperatures(Temperatures, Ain_index, Aout_index)
```

## Algorithm

- Get the original temperature and original Einstein coefficient set
- Calculate $ln(\frac{I}{Ain \cdot 2(2J' + 1)})$ and add a correction term for the new Einstein coefficient set $ln(\frac{Ain}{Aout})$ for each $F(J')$ value in the OH*(6-2) P-branch.
- Plot the corrected $ln(\frac{I}{Aout \cdot 2(2J' + 1)})$ term against $F(J')$
- Extract the output temperature from the gradient of the line by linear fit

This comes from the following equation;
$$
ln(\frac{I}{A \cdot 2(2J' + 1)}) = \frac{-(h c)}{(k T)} * F(J') + ln(\frac{N}{QR}) 
$$

$I$ The spectral line intensity
$A$ The Einstein A coefficient
$J'$ The rotational quantum state
$h$ The Planck constant
$c$ The speed of light in the vacuum
$k$ The Boltzmann constant
$T$ The rotational temperature
$F(J')$ The rotational energy term
$ln(\frac{N}{QR})$ The partition function (constant for any single branch in the spectrum)

## Contributing

Pull requests are welcome on Github. For major changes, please open an issue first to discuss what you would like to change.

## References
Einstein and other quantum coefficients, and general inspiration from the [Synthetic Hydroxyl Spectrum Generator](http://kho.unis.no/Software/SyntheticOH/default.htm) 
[Sigernes, F., Shumilov, N., Deehr, C.S., Nielsen, K.P., Svenøe, T., and Havnes, O., The Hydroxyl rotational temperature record from the Auroral Station in Adventdalen, Svalbard (78°N, 15°E) , Journal of Geophysical Research, Vol 108 (A9), 1342, doi 1029/2001JA009023, 2003.](https://doi.org/10.1029/2001JA009023)

[Holmen, S., Trends and variability of polar mesopause region temperatures attributed to atmospheric dynamics and solar activity, PhD Thesis, UiT The Arctic University of Norway, 2016.](https://hdl.handle.net/10037/10740)

[Mies, F. H. (1974). Calculated vibrational transition probabilities of OH($X^2\Pi$). Journal of Molecular Spectroscopy,53(2), 150–188.](https://ui.adsabs.harvard.edu/link_gateway/1974JMoSp..53..150M/doi:10.1016/0022-2852(74)90125-8)

[Mark P. J. van der Loo, Gerrit C. Groenenboom (2008) Theoretical transition probabilities for the OH Meinel system. J. Chem. Phys. 21 March 2007; 126 (11): 114314.](https://doi.org/10.1063/1.2646859)

[Langhoff, S. R., Werner, H. J., & Rosmus, P. (1986). Theoretical transition probabilities for the OH Meinel system. Journal of Molecular Spectroscopy, 118(2), 507-529](https://doi.org/10.1016/0022-2852(86)90186-4)

[Goldman, A., Schoenfeld, W. G., Goorvitch, D., Chackerian, J., C., Dothe, H., Mélen, F., … Selby, J. E. A. (1998). Updated line parameters for $OH X^2II-X^2II$ ($\upsilon″\upsilon’$) transitions. Journal of Quantitative Spectroscopy and Radiative Transfer, 59(3–5), 453–469. ](https://ui.adsabs.harvard.edu/link_gateway/1998JQSRT..59..453G/doi:10.1016/S0022-4073(97)00112-X)
   
[D.N. Turnbull, R.P. Lowe, New hydroxyl transition probabilities and their importance in airglow studies, Planetary and Space Science, 37(6), 1989, 723-738, 0032-0633](https://doi.org/10.1016/0032-0633(89)90042-1)

## License

[GNU GPLv3.0](https://choosealicense.com/licenses/gpl-3.0/)

