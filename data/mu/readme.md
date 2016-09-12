#Mu data
This folder contains files describing attenuation coefficients.

**Origin:** the NIST tabulations by [Hubbell & Berger](https://www.nist.gov/pml/x-ray-mass-attenuation-coefficients).

**How obtained:** The tabulation done was fetched with the [PhysDataFetch](https://github.com/Dih5/PhysDataFetch) Mathematica package, using densities from the Mathematica database.


**File list:**
- [Z.csv](74.csv)
- [GetMu.nb](getmu.nb)

## Z.csv
- First row: energy in keV
- Second row: attenuation coefficient in cm^-1

## GetMu.nb
The Mathematica notebook used to get this data.
