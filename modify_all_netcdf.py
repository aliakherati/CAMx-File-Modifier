from netcdf_modifier import *
import argparse


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process netCDF concentration file')
    parser.add_argument(
        "-d", "--directory",
        type=str, required=True,
        help='directory where the input netCDF files are.'
    )
    parser.add_argument(
        "-fc", "--fnameconc",
        type=str, required=True,
        help='input conc filename'
    )
    parser.add_argument(
        "-fkv", "--fnamekv",
        type=str, required=True,
        help='input kv filename'
    )
    parser.add_argument(
        "-fm2", "--fnamemet2d",
        type=str, required=True,
        help='input met 2D filename'
    )
    parser.add_argument(
        "-fm3", "--fnamemet3d",
        type=str, required=True,
        help='input met 3D filename'
    )
    parser.add_argument(
        "-rs", "--rowstart",
        type=int, required=True,
        help='starting index for the row where you want to clip the netCDF file'
    )
    parser.add_argument(
        "-re", "--rowend",
        type=int, required=True,
        help='ending index for the row where you want to clip the netCDF file'
    )
    parser.add_argument(
        "-cs", "--colstart",
        type=int, required=True,
        help='starting index for the column where you want to clip the netCDF file'
    )
    parser.add_argument(
        "-ce", "--colend",
        type=int, required=True,
        help='ending index for the column where you want to clip the netCDF file'
    )
    parser.add_argument(
        "-ls", "--laystart",
        type=int, required=True,
        help='starting index for the layer where you want to clip the netCDF file'
    )
    parser.add_argument(
        "-le", "--layend",
        type=int, required=True,
        help='ending index for the layer where you want to clip the netCDF file'
    )
    parser.add_argument(
        "-ra", "--rowindexavg",
        type=str, required=True,
        help='range of row indecies in a form of comma separated string containing two '+
        'integers where you want to take an average of concentration values'
    )
    parser.add_argument(
        "-ca", "--columnindexavg",
        type=str, required=True,
        help='range of column indecies in a form of comma separated string '+ 
        'containing two integers where you want to take an average of concentration values'
    )
    parser.add_argument(
        "-la", "--layerindexavg",
        type=str, required=True,
        help='range of layer indecies in a form of comma separated string containing '+ 
        'two integers where you want to take an average of concentration values'
    )
    parser.add_argument(
        "-od", "--outputdir",
        type=str, required=True,
        help='output directory'
    )
    parser.add_argument(
        "-on", "--outputname",
        type=str, required=True,
        help='output filename'
    )

    args = parser.parse_args()
    
    nc_modify = netcdf_modifier(args.directory)
    
    new_conc_netcdf, excel_dict_conc = nc_modify.modify_conc(
        args.fnameconc,
        args.rowstart,
        args.rowend,
        args.colstart,
        args.colend,
        args.laystart,
        args.layend,
        [int(i) for i in args.rowindexavg.split(',')],
        [int(i) for i in args.columnindexavg.split(',')],
        [int(i) for i in args.layerindexavg.split(',')],
    )

    nc_modify.to_excel(excel_dict_conc, args.outputdir, args.outputname+"_conc.xlsx")
    nc_modify.to_netcdf(new_conc_netcdf, args.outputdir, args.outputname+"_conc.nc")


    new_kv_netcdf = nc_modify.modify_met_kv(
        args.fnamekv,
        args.rowstart,
        args.rowend,
        args.colstart,
        args.colend,
        args.laystart,
        args.layend,
    )

    nc_modify.to_netcdf(new_kv_netcdf, args.outputdir, args.outputname+"_kv.nc")

    new_met2d_netcdf, excel_dict_met2d = nc_modify.modify_met_2d(
        args.fnamemet2d,
        args.rowstart,
        args.rowend,
        args.colstart,
        args.colend,
        [int(i) for i in args.rowindexavg.split(',')],
        [int(i) for i in args.columnindexavg.split(',')],
    )

    nc_modify.to_excel(excel_dict_met2d, args.outputdir, args.outputname+"_met2d.xlsx")
    nc_modify.to_netcdf(new_met2d_netcdf, args.outputdir, args.outputname+"_met2d.nc")

    new_met3d_netcdf, excel_dict_met3d = nc_modify.modify_met_3d(
        new_met2d_netcdf,
        args.fnamemet3d,
        args.rowstart,
        args.rowend,
        args.colstart,
        args.colend,
        args.laystart,
        args.layend,
        [int(i) for i in args.rowindexavg.split(',')],
        [int(i) for i in args.columnindexavg.split(',')],
        [int(i) for i in args.layerindexavg.split(',')],
    )

    nc_modify.to_excel(excel_dict_met3d, args.outputdir, args.outputname+"_met3d.xlsx")
    nc_modify.to_netcdf(new_met3d_netcdf, args.outputdir, args.outputname+"_met3d.nc")
