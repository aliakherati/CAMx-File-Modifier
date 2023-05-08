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
        "-f", "--filename",
        type=str, required=True,
        help='input filename'
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
        help='range of row indicies in a form of comma separated string containing two '+
        'integers where you want to take an average of concentration values'
    )
    parser.add_argument(
        "-ca", "--columnindexavg",
        type=str, required=True,
        help='range of column indicies in a form of comma separated string '+ 
        'containing two integers where you want to take an average of concentration values'
    )
    parser.add_argument(
        "-la", "--layerindexavg",
        type=str, required=True,
        help='range of layer indicies in a form of comma separated string containing '+ 
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
    
    new_netcdf = nc_modify.modify_conc(
        args.filename,
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

    nc_modify.export(new_netcdf, args.outputdir, args.outputname)



