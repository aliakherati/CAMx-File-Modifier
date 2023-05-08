# Modifying CAMx netCDF files

There scripts are:
- `netcdf_modifier.py`: It is a library that contains the functions
- `modify_conc_netcdf.py`: It is the python script to modify CAMx output concentration file

## How to use
1. You need to create a virtual environment in the repo first by `$ python3 -m venv venv`
2. Activate the virtual environment by running this command: `$ source venv/bin/activate`
3. Update `pip` to install packages by running this command: `$ pip install --upgrade pip`
4. Install the required libraries by using `requirements.txt`: `$ pip install -r requirements.txt`

### How to run `modify_conc_netcdf.py`
The required flags are:
Input information
1. `-d`/`--directory`: input directory name as a `string`
2. `-f`/`--filename`: input filename as a `string`
The followings are all starting index (included, and note that index in python starts from zero) for the row/column/layer where you want to clip the netCDF file as an `integer`:
3. `-rs`/`--rowstart`
4. `-cs`/`--colstart`
5. `-ls`/`--laystart`
The followings are all ending index (not included) for the row/column/layer where you want to clip the netCDF file as an `integer`  
6. `-re`/`--rowend`
7. `-ce`/`--colend`
8. `-le`/`--layend`
The followings are range of row/column/layer indicies in a form of comma separated `string` containing two `integer`s where you want to take an average of concentration values
9. `-ra`/`--rowindexavg`
10. `-ca`/`--columnindexavg`
11. `-la`/`--layerindexavg`
Output information
12. `-od`/`--outputdir`: output directory as a `string`
13. `-on`/`--outputname`: output filename as a `string`

You can follow the example below:
```
python3 modify-conc-netcdf.py -d "../netcdf-files/" -f "camx720_cb6r5_avrg.20190723.txo3.bc19_19jul.v2d_v2a.2019_wrf415_noah_ysu_lyr45t30.txs_4km.nc" -rs 0 -re 10 -cs 0 -ce 20 -ls 0 -le 2 -ra "20, 50" -ca "30,60" -la "0,2" -od "../output/" -on "out_argparse.nc"
```
