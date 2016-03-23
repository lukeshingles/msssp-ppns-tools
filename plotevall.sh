./plotev.py -ycode 12 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-CentralDensity.pdf
./plotev.py -ycode 13 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-CentralTemperature.pdf
./plotev.py -ycode 14 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-CentralPressure.pdf
./plotev.py -ycode 16 -ymin 1e4 -ymax 50000 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-LH.pdf
./plotev.py -logscaley -ycode 17 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-LHe.pdf
./plotev.py -ycode 31 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-MidHShellRadius.pdf
./plotev.py -ycode 32 -ymin 2e7 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-MidHShellTemperature.pdf
./plotev.py -ycode 33 -ymin 8 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-MidHShellDensity.pdf
./plotev.py -ycode 39 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-BottomHeShellRadius.pdf
./plotev.py -ycode 40 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-BottomHeShellTemperature.pdf
./plotev.py -ycode 41 -ymin 1e4 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-BottomHeShellDensity.pdf
./plotev.py -ycode 42 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-MidHeShellRadius.pdf
./plotev.py -ycode 43 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-MidHeShellTemperature.pdf
./plotev.py -logscaley -ycode 44 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-MidHeShellDensity.pdf
./plotev.py -ycode 45 marmot_backup/evoln_code/m3z0006y40/evagb.dat marmot_backup/evoln_code/m4z0006y30/evagb.dat
mv plotev.pdf plot-TopHeShellMass.pdf
