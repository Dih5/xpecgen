# How to test xpecgen

This document is made to help the JOSS reviewer to check the application is working.

Since the results should be compared with those of the mathematical model, unit tests would have the same complexity as the application itself.
The GUI may be used to test the library is behaving properly. The following lines may guide the process:

## Calculate tab
- Press the calculate button with the default parameters. A spectrum should be calculated and plotted. Check it is qualitatively similar with those in the paper of the model. Note that the one in the image in the readme does look like those, in case you don't have access to that article.
- Check the spectrum changes when recalculated with E0 values as low as 50 and as high as 500.
- Other parameters may also varied

## Analyze tab
- Check the normalization functionality: use the normalize tab to fix the norm according to any of the available criteria. Check in the parameter table below the norm meets the demanded criterion.
- Check the attenuation functionality: when a spectrum is attenuated norms should decrease. The spectrum shape should also change.
- Check the export functionality: use the "export" button to save the data as an xlsx document. This file includes a plot that should look similar to the one in the GUI. You can also check the values in the csv when exporting to that format.

## Overall quantitative check:
- The HVL ("half-value-layers") are values that depend on the calculated spectrum and on the attenuation functionality. Thus, they can be used to check the results are quantitatively similar to those published in the model paper.
The values in the paper refer to a calculation with theta=12, phi=0, and attenuated by 1.2 mm of Al and 100 cm of air.
The script test_hvl.py in the demo directory is prepared to perform this calculations. When it is run the values it displays at the end of its execution should be similar to {2.37, 1.85, 1.20} mm, which the values in the publication.
Yes, this could have been written as a unit test... but fixing those values as "the good ones" would make no sense, because if model was changed, they should change.
