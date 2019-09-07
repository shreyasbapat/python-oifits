import astropy.io.fits as fits
import numpy as np

from .data import Data
from .dataclasses import *


class OIParser:
    """
    Class for operations on OIFITS data.
    """

    def __init__(self, filename):
        self.hdulist = fits.open(filename)
        self.data = self.process()
        self.hdulist.close()
        self.t3data = None

    @property
    def info(self):
        return self.hdulist.info()

    @classmethod
    def read(cls, filename):
        return cls(filename=filename)

    def process(self):
        """
        Method to process a OIFITS file.

        Returns
        -------
        dataobj : ~oifits.data.Data
            Object containing all the data
        """
        dataobj = Data()
        targetmap = {}
        sta_indices = {}
        hdulist = self.hdulist
        # First get all the OI_TARGET, OI_WAVELENGTH and OI_ARRAY tables
        for hdu in hdulist:
            header = hdu.header
            data = hdu.data
            if hdu.name == "OI_WAVELENGTH":
                if dataobj.wavelength == None:
                    dataobj.wavelength = {}
                insname = header["INSNAME"]
                dataobj.wavelength[insname] = OI_WAVELENGTH(
                    data.field("EFF_WAVE"), data.field("EFF_BAND")
                )
            elif hdu.name == "OI_TARGET":
                for row in data:
                    target_id = row["TARGET_ID"]
                    target = OI_TARGET(
                        target=row["TARGET"],
                        raep0=row["RAEP0"],
                        decep0=row["DECEP0"],
                        equinox=row["EQUINOX"],
                        ra_err=row["RA_ERR"],
                        dec_err=row["DEC_ERR"],
                        sysvel=row["SYSVEL"],
                        veltyp=row["VELTYP"],
                        veldef=row["VELDEF"],
                        pmra=row["PMRA"],
                        pmdec=row["PMDEC"],
                        pmra_err=row["PMRA_ERR"],
                        pmdec_err=row["PMDEC_ERR"],
                        parallax=row["PARALLAX"],
                        para_err=row["PARA_ERR"],
                        spectyp=row["SPECTYP"],
                    )
                    dataobj.target = np.append(dataobj.target, target)
                    targetmap[target_id] = target
            elif hdu.name == "OI_ARRAY":
                if dataobj.array == None:
                    dataobj.array = {}
                arrname = header["ARRNAME"]
                frame = header["FRAME"]
                arrxyz = np.array(
                    [header["ARRAYX"], header["ARRAYY"], header["ARRAYZ"]]
                )
                dataobj.array[arrname] = OI_ARRAY(frame, arrxyz, stations=data)
                # Save the sta_index for each array, as we will need it
                # later to match measurements to stations
                sta_indices[arrname] = data.field("sta_index")

        # Then get any science measurements
        for hdu in hdulist:
            header = hdu.header
            data = hdu.data
            if hdu.name in ("OI_VIS", "OI_VIS2", "OI_T3"):
                if "ARRNAME" in header.keys():
                    arrname = header["ARRNAME"]
                else:
                    arrname = None
                if arrname and dataobj.array:
                    array = dataobj.array[arrname]
                else:
                    array = None
                wavelength = dataobj.wavelength[header["INSNAME"]]
            if hdu.name == "OI_VIS":
                for row in data:
                    date = header["DATE-OBS"].split("-")
                    timeobs = datetime.datetime(
                        int(date[0]), int(date[1]), int(date[2])
                    ) + datetime.timedelta(seconds=np.around(row.field("TIME"), 2))
                    int_time = row.field("INT_TIME")
                    visamp = np.reshape(row.field("VISAMP"), -1)
                    visamperr = np.reshape(row.field("VISAMPERR"), -1)
                    visphi = np.reshape(row.field("VISPHI"), -1)
                    visphierr = np.reshape(row.field("VISPHIERR"), -1)
                    if "CFLUX" in row.array.names:
                        cflux = np.reshape(row.field("CFLUX"), -1)
                    else:
                        cflux = None
                    if "CFLUXERR" in row.array.names:
                        cfluxerr = np.reshape(row.field("CFLUXERR"), -1)
                    else:
                        cfluxerr = None
                    flag = np.reshape(row.field("FLAG"), -1)
                    ucoord = row.field("UCOORD")
                    vcoord = row.field("VCOORD")
                    target = targetmap[row.field("TARGET_ID")]
                    if array:
                        sta_index = row.field("STA_INDEX")
                        s1 = array.station[sta_indices[arrname] == sta_index[0]][0]
                        s2 = array.station[sta_indices[arrname] == sta_index[1]][0]
                        station = [s1, s2]
                    else:
                        station = [None, None]
                    dataobj.vis = np.append(
                        dataobj.vis,
                        OI_VIS(
                            timeobs=timeobs,
                            int_time=int_time,
                            visamp=visamp,
                            visamperr=visamperr,
                            visphi=visphi,
                            visphierr=visphierr,
                            flag=flag,
                            ucoord=ucoord,
                            vcoord=vcoord,
                            wavelength=wavelength,
                            target=target,
                            array=array,
                            station=station,
                            cflux=cflux,
                            cfluxerr=cfluxerr,
                        ),
                    )
            elif hdu.name == "OI_VIS2":
                for row in data:
                    date = header["DATE-OBS"].split("-")
                    timeobs = datetime.datetime(
                        int(date[0]), int(date[1]), int(date[2])
                    ) + datetime.timedelta(seconds=np.around(row.field("TIME"), 2))
                    int_time = row.field("INT_TIME")
                    vis2data = np.reshape(row.field("VIS2DATA"), -1)
                    vis2err = np.reshape(row.field("VIS2ERR"), -1)
                    flag = np.reshape(row.field("FLAG"), -1)
                    ucoord = row.field("UCOORD")
                    vcoord = row.field("VCOORD")
                    target = targetmap[row.field("TARGET_ID")]
                    if array:
                        sta_index = row.field("STA_INDEX")
                        s1 = array.station[sta_indices[arrname] == sta_index[0]][0]
                        s2 = array.station[sta_indices[arrname] == sta_index[1]][0]
                        station = [s1, s2]
                    else:
                        station = [None, None]
                    dataobj.vis2 = np.append(
                        dataobj.vis2,
                        OI_VIS2(
                            timeobs=timeobs,
                            int_time=int_time,
                            vis2data=vis2data,
                            vis2err=vis2err,
                            flag=flag,
                            ucoord=ucoord,
                            vcoord=vcoord,
                            wavelength=wavelength,
                            target=target,
                            array=array,
                            station=station,
                        ),
                    )
            elif hdu.name == "OI_T3":
                for row in data:
                    date = header["DATE-OBS"].split("-")
                    timeobs = datetime.datetime(
                        int(date[0]), int(date[1]), int(date[2])
                    ) + datetime.timedelta(seconds=np.around(row.field("TIME"), 2))
                    int_time = row.field("INT_TIME")
                    t3amp = np.reshape(row.field("T3AMP"), -1)
                    t3amperr = np.reshape(row.field("T3AMPERR"), -1)
                    t3phi = np.reshape(row.field("T3PHI"), -1)
                    t3phierr = np.reshape(row.field("T3PHIERR"), -1)
                    flag = np.reshape(row.field("FLAG"), -1)
                    u1coord = row.field("U1COORD")
                    v1coord = row.field("V1COORD")
                    u2coord = row.field("U2COORD")
                    v2coord = row.field("V2COORD")
                    target = targetmap[row.field("TARGET_ID")]
                    if array:
                        sta_index = row.field("STA_INDEX")
                        s1 = array.station[sta_indices[arrname] == sta_index[0]][0]
                        s2 = array.station[sta_indices[arrname] == sta_index[1]][0]
                        s3 = array.station[sta_indices[arrname] == sta_index[2]][0]
                        station = [s1, s2, s3]
                    else:
                        station = [None, None, None]
                    dataobj.t3 = np.append(
                        dataobj.t3,
                        OI_T3(
                            timeobs=timeobs,
                            int_time=int_time,
                            t3amp=t3amp,
                            t3amperr=t3amperr,
                            t3phi=t3phi,
                            t3phierr=t3phierr,
                            flag=flag,
                            u1coord=u1coord,
                            v1coord=v1coord,
                            u2coord=u2coord,
                            v2coord=v2coord,
                            wavelength=wavelength,
                            target=target,
                            array=array,
                            station=station,
                        ),
                    )
        return dataobj

    def export_to_ascii(self):
        """
        Method to export the data in OIFITS file to ASCII as a numpy array

        Returns
        -------
        t3data : ~numpy.ndarray
            Array Containing u1, v1, u2, v2, u3, v3, t3amp, t3phi, t3err.
        """
        t3 = self.data.t3
        # get wavelength data
        wav = self.data.wavelength["WAVELENGTH_NAME"].eff_wave[0]

        # output u1, v1, u2, v2, u3, v3, t3amp, t3phi, t3err
        t3data = [
            [
                t3[i].u1coord / wav,
                t3[i].v1coord / wav,
                t3[i].u2coord / wav,
                t3[i].v2coord / wav,
                -(t3[i].u1coord + t3[i].u2coord) / wav,
                -(t3[i].v1coord + t3[i].v2coord) / wav,
                t3[i].t3amp[0],
                t3[i].t3phi[0],
                t3[i].t3amperr[0],
                t3[i].t3phierr[0],
            ]
            for i in range(len(t3))
        ]

        self.t3data = np.array(t3data)
        return self.t3data

    def save_file(self, filename):
        """
        Method to save the data in a file as ASCII

        Parameters
        ----------
        filename : str
            Name of the file with ".txt" extension

        """
        if self.t3data:
            np.savetxt(filename, self.t3data)
        else:
            self.export_to_ascii()
