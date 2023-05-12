import numpy as np
import xarray as xr
import pandas as pd

class netcdf_modifier:
    def __init__(self, directory:str) -> None:
        self.directory = directory
        pass

    def modify_conc(
        self,
        FileName:str,
        RowStart:int,
        RowEnd:int,
        ColumnStart:int,
        ColumnEnd:int,
        LayerStart:int,
        LayerEnd:int,
        RowIndexAvg:list,
        ColumnIndexAvg:list,
        LayerIndexAvg:list,
    ):
        """
        This function modifies CAMx output concentration.
        ...
        Parameters
        ----------
        FileName : str
            a formatted string to give a input file
        RowStart : int
            starting index for the row where you want to clip the
            netCDF file
        RowEnd : int
            Ending index for the row where you want to clip the
            netCDF file
        ColumnStart : int
            starting index for the column where you want to clip
            the netCDF file
        ColumnEnd : int
            Ending index for the column where you want to clip
            the netCDF file
        LayerStart : int
            starting index for the layer where you want to clip
            the netCDF file
        LayerEnd : int
            ending index for the layer where you want to clip
            the netCDF file
        RowIndexAvg : list
            range of row indecies in a form of list containing
            two integers where you want to take an average of
            concentration values
        ColumnIndexAvg : list
            range of column indecies in a form of list containing
            two integers where you want to take an average of
            concentration values
        LayerIndexAvg : list
            range of layer indecies in a form of list containing
            two integers where you want to take an average of
            concentration values
        
        Raises
        ------
        ValueError:
            - if the start index in bigger ot equal to end
            index
            - if length of RowIndexAvg, ColumnIndexAvg, and
            LayerIndexAvg are not equal two.
        
        Returns
        -------
        netCDF dataset
            that is the modified netCDF file.

        Example
        -------
        new_ds = modifying_netcdf(
            FileName="../inputs/Input_netCDF.nc",
            RowStart = 0,
            RowEnd = 10,
            ColumnStart = 0,
            ColumnEnd = 5,
            LayerStart = 0,
            LayerEnd = 2,
            RowIndexAvg = [20,40],
            ColumnIndexAvg = [30,60],
            LayerIndexAvg = [0,2],
        )
        Caveat
        -------
        All layers, columns, and rows on the final file will be filled with the
        average value for each hour.
        """
        # ----------------------------------------------------------------------
        # Error checking
        if (len(RowIndexAvg)!=2):
            raise ValueError("RowIndexAvg must have a length of two.")
        if (len(ColumnIndexAvg)!=2):
            raise ValueError("ColumnIndexAvg must have a length of two.")
        if (len(LayerIndexAvg)!=2):
            raise ValueError("LayerIndexAvg must have a length of two.")
        # ---
        if (ColumnEnd<=ColumnStart):
            raise ValueError("ColumnStart is bigger than or equal to ColumnEnd")
        if (RowEnd<RowStart):
            raise ValueError("RowStart is bigger than or equal to RowEnd")
        if (LayerEnd<LayerStart):
            raise ValueError("LayerStart is bigger than or equal to LayerEnd")
        # -----------------------------------------------------------------------
        
        # read the file
        ds = xr.open_dataset(f"{self.directory}/{FileName}")
        
        # select the window you want to take a mean
        selected_ds = ds.isel(
            COL=slice(ColumnIndexAvg[0], ColumnIndexAvg[1]),
            ROW=slice(RowIndexAvg[0], RowIndexAvg[1]),
            LAY=slice(LayerIndexAvg[0], LayerIndexAvg[1]),
        )
        # take the mean
        mean_ds = selected_ds.mean(dim=["ROW", "COL", "LAY"])
        mean_ds_noavglay = selected_ds.mean(dim=["ROW", "COL"])
        
        # select the window you need for your simulation
        new_ds = ds.isel(
            COL=slice(ColumnStart, ColumnEnd),
            ROW=slice(RowStart, RowEnd),
            LAY=slice(LayerStart, LayerEnd),
        )
        
        # replace the values with the average value for each variable at the surface
        excluded_variable = ["X", "Y", "layer", "TFLAG", "ETFLAG", "topo", "z", "longitude", "latitude"]
        for i, variable in enumerate(new_ds.variables):
            if variable not in excluded_variable:
                for z in range(new_ds.dims["LAY"]):
                    for t in range(new_ds[variable].shape[0]):
                        new_ds[variable][t,z,:,:] = mean_ds[variable][t]
        
        # to create excel file
        excel_mean_noavglay = {}
        for i, variable in enumerate(mean_ds.variables):
            if variable not in excluded_variable:
                df = pd.DataFrame()
                df['hour\layer'] = [i for i in range(24)]
                for z in mean_ds_noavglay["layer"].values:
                    df[z] = mean_ds_noavglay[variable][:,z-1]
                df["averaged"] = mean_ds[variable][:].values.tolist()
                excel_mean_noavglay[variable] = df
        
        # editing the attributes
        new_ds.attrs["NCOLS"] = ColumnEnd-ColumnStart
        new_ds.attrs["NROWS"] = RowEnd-RowStart
        new_ds.attrs["NLAYS"] = LayerEnd-LayerStart

        return new_ds, excel_mean_noavglay
    
    def to_excel(
        self,
        Dictionary:dict,
        OutputDir:str,
        OutputFile:str,
    ) -> None:
        with pd.ExcelWriter(f'{OutputDir}/{OutputFile}') as writer:
            for key, df in Dictionary.items():
                df.to_excel(writer, sheet_name=key, index=False)
        pass

    def to_netcdf(
        self,
        nc_dataset:xr.Dataset,
        OutputDirectory:str,
        OutputName:str,
    ) -> None:
        nc_dataset.to_netcdf(f"{OutputDirectory}/{OutputName}")
        pass

    def modify_met_kv(
        self,
        FileName:str,
        RowStart:int,
        RowEnd:int,
        ColumnStart:int,
        ColumnEnd:int,
        LayerStart:int,
        LayerEnd:int,
    ):
        # ----------------------------------------------------------------------
        # Error checking
        if (ColumnEnd<=ColumnStart):
            raise ValueError("ColumnStart is bigger than or equal to ColumnEnd")
        if (RowEnd<RowStart):
            raise ValueError("RowStart is bigger than or equal to RowEnd")
        if (LayerEnd<LayerStart):
            raise ValueError("LayerStart is bigger than or equal to LayerEnd")
        # -----------------------------------------------------------------------
        
        # read the file
        ds = xr.open_dataset(f"{self.directory}/{FileName}")
        
        # select the window you need for your simulation
        new_ds = ds.isel(
            COL=slice(ColumnStart, ColumnEnd),
            ROW=slice(RowStart, RowEnd),
            LAY=slice(LayerStart, LayerEnd),
        )
                
        # editing the attributes
        new_ds.attrs["NCOLS"] = ColumnEnd-ColumnStart
        new_ds.attrs["NROWS"] = RowEnd-RowStart
        new_ds.attrs["NLAYS"] = LayerEnd-LayerStart
        
        new_ds.variables['kv'].values[:] = 0.1

        return new_ds
    
    def modify_met_2d(
        self,
        FileName:str,
        RowStart:int,
        RowEnd:int,
        ColumnStart:int,
        ColumnEnd:int,
        LayerStart:int,
        LayerEnd:int,
        RowIndexAvg:list,
        ColumnIndexAvg:list,
    ):
        # ----------------------------------------------------------------------
        # Error checking
        if (len(RowIndexAvg)!=2):
            raise ValueError("RowIndexAvg must have a length of two.")
        if (len(ColumnIndexAvg)!=2):
            raise ValueError("ColumnIndexAvg must have a length of two.")
        # ---
        if (ColumnEnd<=ColumnStart):
            raise ValueError("ColumnStart is bigger than or equal to ColumnEnd")
        if (RowEnd<RowStart):
            raise ValueError("RowStart is bigger than or equal to RowEnd")
        if (LayerEnd<LayerStart):
            raise ValueError("LayerStart is bigger than or equal to LayerEnd")
        # -----------------------------------------------------------------------

        # read the file
        ds = xr.open_dataset(f"{self.directory}/{FileName}")

        # select the window you want to take a mean
        selected_ds = ds.isel(
            COL=slice(ColumnIndexAvg[0], ColumnIndexAvg[1]),
            ROW=slice(RowIndexAvg[0], RowIndexAvg[1]),
        )
        # take the mean
        mean_ds = selected_ds.mean(dim=["ROW", "COL"])

        # select the window you need for your simulation
        new_ds = ds.isel(
            COL=slice(ColumnStart, ColumnEnd),
            ROW=slice(RowStart, RowEnd),
        )

        # replace the values with the average value for each variable at the surface
        excluded_variable = ["X", "Y", "layer", "TFLAG", "ETFLAG", "topo", "z", "longitude", "latitude"]
        for i, variable in enumerate(new_ds.variables):
            if variable not in excluded_variable:
                for z in range(new_ds.dims["LAY"]):
                    for t in range(new_ds[variable].shape[0]):
                        new_ds[variable][t,z,:,:] = mean_ds[variable][t]

        for var in ['snowewd', 'snowage', 'tcloudod', 'preciprate', 'cloudtop']:
            new_ds[var][:] = 0.0

        for var in ['pblwrf', 'pblcmaq', 'pblysu']:
            new_ds.variables[var].values[new_ds.variables[var].values<100] = 100
            new_ds.variables[var].values[new_ds.variables[var].values<2500] = 2500

        # to create excel file
        excel_mean = {}
        df = pd.DataFrame()
        df['hour\layer'] = [i for i in range(25)]
        for i, variable in enumerate(mean_ds.variables):
            if variable not in excluded_variable:
                df[variable] = mean_ds[variable][:,0]
        excel_mean['all'] = df

        # editing the attributes
        new_ds.attrs["NCOLS"] = ColumnEnd-ColumnStart
        new_ds.attrs["NROWS"] = RowEnd-RowStart
        new_ds.attrs["NLAYS"] = LayerEnd-LayerStart

    return new_ds, excel_mean

    def modify_met_3d(
        self,
        Dataset2D,
        FileName:str,
        RowStart:int,
        RowEnd:int,
        ColumnStart:int,
        ColumnEnd:int,
        LayerStart:int,
        LayerEnd:int,
        RowIndexAvg:list,
        ColumnIndexAvg:list,
        LayerIndexAvg:list,
    ):
        # ----------------------------------------------------------------------
        # Error checking
        if (len(RowIndexAvg)!=2):
            raise ValueError("RowIndexAvg must have a length of two.")
        if (len(ColumnIndexAvg)!=2):
            raise ValueError("ColumnIndexAvg must have a length of two.")
        if (len(LayerIndexAvg)!=2):
            raise ValueError("LayerIndexAvg must have a length of two.")
        # ---
        if (ColumnEnd<=ColumnStart):
            raise ValueError("ColumnStart is bigger than or equal to ColumnEnd")
        if (RowEnd<RowStart):
            raise ValueError("RowStart is bigger than or equal to RowEnd")
        if (LayerEnd<LayerStart):
            raise ValueError("LayerStart is bigger than or equal to LayerEnd")
        # -----------------------------------------------------------------------

        # read the file
        ds = xr.open_dataset(f"{self.directory}/{FileName}")

        # select the window you want to take a mean
        selected_ds = ds.isel(
            COL=slice(ColumnIndexAvg[0], ColumnIndexAvg[1]),
            ROW=slice(RowIndexAvg[0], RowIndexAvg[1]),
        )
        # take the mean
        mean_ds = selected_ds.mean(dim=["ROW", "COL"])

        # select the window you need for your simulation
        new_ds = ds.isel(
            COL=slice(ColumnStart, ColumnEnd),
            ROW=slice(RowStart, RowEnd),
        )

        # replace the values with the average value for each variable at the surface
        excluded_variable = ["X", "Y", "layer", "TFLAG", "ETFLAG", "topo", "z", "longitude", "latitude"]
        for i, variable in enumerate(new_ds.variables):
            if variable not in excluded_variable:
                for z in range(new_ds.dims["LAY"]):
                    for t in range(new_ds[variable].shape[0]):
                        new_ds[variable][t,z,:,:] = mean_ds[variable][t,z]

        for var in ['cloudwater', 'rainwater', 'grplwater', 'cloudod']:
            new_ds[var][:] = 0.0

        # set the height of second layer to 3000 m
        new_ds.variables['z'].values[:,1,:,:] = 3000.
        # set the height of first layer to pbl height from 2D netcdf file
        new_ds.variables['z'].values[:,0,:,:] = Dataset2D.variables['pblwrf'].values[:,0,:,:]
        # set u wind speed to zero 
        new_ds.variables['uwind'].values[:] = 0
        # set v wind speed to zero 
        new_ds.variables['vwind'].values[:] = 0.0926 # m/s (purging layer 2 with 12 hr lifetime)

        # to create excel file
        excel_mean = {}
        for i, variable in enumerate(mean_ds.variables):
            if variable not in excluded_variable:
                df = pd.DataFrame()
                df['hour\layer'] = [i for i in range(25)]
                for z in mean_ds["layer"].values:
                    z = int(z)
                    df[z] = mean_ds[variable].values[:,z-1]
                df["averaged"] = np.nanmean(mean_ds[variable][:].values, axis=1).tolist()
                excel_mean[variable] = df

        # editing the attributes
        new_ds.attrs["NCOLS"] = ColumnEnd-ColumnStart
        new_ds.attrs["NROWS"] = RowEnd-RowStart
        new_ds.attrs["NLAYS"] = LayerEnd-LayerStart

    return new_ds, excel_mean
