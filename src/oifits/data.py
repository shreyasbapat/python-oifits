import copy
import datetime

import astropy.io.fits as fits
import numpy as np

from .utils import _array_eq, _plurals

_mjdzero = datetime.datetime(1858, 11, 17)
matchtargetbyname = False
matchstationbyname = False
refdate = datetime.datetime(2000, 1, 1)


class Data:
    """
    Class for storing the Data of OIFITS file.
    """

    def __init__(self):
        self.wavelength = {}
        self.target = np.empty(0)
        self.array = {}
        self.vis = np.empty(0)
        self.vis2 = np.empty(0)
        self.t3 = np.empty(0)

    def __add__(self, other):
        """
        Consistently combine two separate Data objects.  Note
        that targets can be matched by name only (e.g. if coordinates
        differ) by setting oifits.matchtargetbyname to True.  The same
        goes for stations of the array (controlled by
        oifits.matchstationbyname)
        """
        # Don't do anything if the two oifits objects are not CONSISTENT!
        if self.isconsistent() == False or other.isconsistent() == False:
            print("Data Objects are not consistent! Can not add!")
            return

        new = copy.deepcopy(self)
        if len(other.wavelength):
            wavelengthmap = {}
            for key in other.wavelength.keys():
                if key not in new.wavelength.keys():
                    new.wavelength[key] = copy.deepcopy(other.wavelength[key])
                elif new.wavelength[key] != other.wavelength[key]:
                    raise ValueError(
                        "Wavelength tables have the same key but differing contents."
                    )
                wavelengthmap[id(other.wavelength[key])] = new.wavelength[key]

        if len(other.target):
            targetmap = {}
            for otarget in other.target:
                for ntarget in new.target:
                    if matchtargetbyname and ntarget.target == otarget.target:
                        targetmap[id(otarget)] = ntarget
                        break
                    elif ntarget == otarget:
                        targetmap[id(otarget)] = ntarget
                        break
                    elif ntarget.target == otarget.target:
                        print(
                            "Found a target with a matching name, but some differences in the target specification.  Creating a new target.  Set oifits.matchtargetbyname to True to override this behavior."
                        )
                # If 'id(otarget)' is not in targetmap, then this is a new
                # target and should be added to the array of targets
                if id(otarget) not in targetmap.keys():
                    try:
                        newkey = new.target.keys()[-1] + 1
                    except:
                        newkey = 1
                    target = copy.deepcopy(otarget)
                    new.target = np.append(new.target, target)
                    targetmap[id(otarget)] = target

        if len(other.array):
            stationmap = {}
            arraymap = {}
            for key, otharray in other.array.iteritems():
                arraymap[id(otharray)] = key
                if key not in new.array.keys():
                    new.array[key] = copy.deepcopy(other.array[key])
                # If arrays have the same name but seem to differ, try
                # to combine the two (by including the union of both
                # sets of stations)
                for othsta in other.array[key].station:
                    for newsta in new.array[key].station:
                        if newsta == othsta:
                            stationmap[id(othsta)] = newsta
                            break
                        elif matchstationbyname and newsta.sta_name == othsta.sta_name:
                            stationmap[id(othsta)] = newsta
                            break
                        elif (
                            newsta.sta_name == othsta.sta_name
                            and matchstationbyname == False
                        ):
                            raise ValueError(
                                "Stations have matching names but conflicting data."
                            )
                    # If 'id(othsta)' is not in the stationmap
                    # dictionary, then this is a new station and
                    # should be added to the current array
                    if id(othsta) not in stationmap.keys():
                        newsta = copy.deepcopy(othsta)
                        new.array[key].station = np.append(
                            new.array[key].station, newsta
                        )
                        stationmap[id(othsta)] = newsta
                        # Make sure that staxyz of the new station is relative to the new array center
                        newsta.staxyz = (
                            othsta.staxyz
                            - other.array[key].arrxyz
                            + new.array[key].arrxyz
                        )

        for vis in other.vis:
            if vis not in new.vis:
                newvis = copy.copy(vis)
                # The wavelength, target, array and station objects
                # should point to the appropriate objects inside the
                # 'new' structure
                newvis.wavelength = wavelengthmap[id(vis.wavelength)]
                newvis.target = targetmap[id(vis.target)]
                if vis.array:
                    newvis.array = new.array[arraymap[id(vis.array)]]
                    newvis.station = [None, None]
                    newvis.station[0] = stationmap[id(vis.station[0])]
                    newvis.station[1] = stationmap[id(vis.station[1])]
                new.vis = np.append(new.vis, newvis)

        for vis2 in other.vis2:
            if vis2 not in new.vis2:
                newvis2 = copy.copy(vis2)
                # The wavelength, target, array and station objects
                # should point to the appropriate objects inside the
                # 'new' structure
                newvis2.wavelength = wavelengthmap[id(vis2.wavelength)]
                newvis2.target = targetmap[id(vis2.target)]
                if vis2.array:
                    newvis2.array = new.array[arraymap[id(vis2.array)]]
                    newvis2.station = [None, None]
                    newvis2.station[0] = stationmap[id(vis2.station[0])]
                    newvis2.station[1] = stationmap[id(vis2.station[1])]
                new.vis2 = np.append(new.vis2, newvis2)

        for t3 in other.t3:
            if t3 not in new.t3:
                newt3 = copy.copy(t3)
                # The wavelength, target, array and station objects
                # should point to the appropriate objects inside the
                # 'new' structure
                newt3.wavelength = wavelengthmap[id(t3.wavelength)]
                newt3.target = targetmap[id(t3.target)]
                if t3.array:
                    newt3.array = new.array[arraymap[id(t3.array)]]
                    newt3.station = [None, None, None]
                    newt3.station[0] = stationmap[id(t3.station[0])]
                    newt3.station[1] = stationmap[id(t3.station[1])]
                    newt3.station[2] = stationmap[id(t3.station[2])]
                new.t3 = np.append(new.t3, newt3)

        return new

    def __eq__(self, other):

        if type(self) != type(other):
            return False

        return not (
            (self.wavelength != other.wavelength)
            or (self.target != other.target).any()
            or (self.array != other.array)
            or (self.vis != other.vis).any()
            or (self.vis2 != other.vis2).any()
            or (self.t3 != other.t3).any()
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def isvalid(self):
        """
        Returns
        -------
        True
            If the Data object is both consistent (as
            determined by isconsistent()) and conforms to the OIFITS
            standard (according to Pauls et al., 2005, PASP, 117, 1255).

        False
            Otherwise
        """

        warnings = []
        errors = []
        if not self.isconsistent():
            errors.append("oifits object is not consistent")
        if not self.target.size:
            errors.append("No OI_TARGET data")
        if not self.wavelength:
            errors.append("No OI_WAVELENGTH data")
        else:
            for wavelength in self.wavelength.values():
                if len(wavelength.eff_wave) != len(wavelength.eff_band):
                    errors.append(
                        "eff_wave and eff_band are of different lengths for wavelength table"
                    )
        if self.vis.size + self.vis2.size + self.t3.size == 0:
            errors.append(
                "Need to have atleast one measurement table (vis, vis2 or t3)"
            )
        for vis in self.vis:
            nwave = len(vis.wavelength.eff_band)
            if (
                (len(vis.visamp) != nwave)
                or (len(vis.visamperr) != nwave)
                or (len(vis.visphi) != nwave)
                or (len(vis.visphierr) != nwave)
                or (len(vis.flag) != nwave)
            ):
                errors.append(
                    "Data size mismatch for visibility measurement 0x%x (wavelength table has a length of %d)"
                    % (id(vis), nwave)
                )
        for vis2 in self.vis2:
            nwave = len(vis2.wavelength.eff_band)
            if (
                (len(vis2.vis2data) != nwave)
                or (len(vis2.vis2err) != nwave)
                or (len(vis2.flag) != nwave)
            ):
                errors.append(
                    "Data size mismatch for visibility^2 measurement 0x%x (wavelength table has a length of %d)"
                    % (id(vis), nwave)
                )
        for t3 in self.t3:
            nwave = len(t3.wavelength.eff_band)
            if (
                (len(t3.t3amp) != nwave)
                or (len(t3.t3amperr) != nwave)
                or (len(t3.t3phi) != nwave)
                or (len(t3.t3phierr) != nwave)
                or (len(t3.flag) != nwave)
            ):
                errors.append(
                    "Data size mismatch for visibility measurement 0x%x (wavelength table has a length of %d)"
                    % (id(vis), nwave)
                )

        if warnings:
            print("*** %d warning%s:" % (len(warnings), _plurals(len(warnings))))
            for warning in warnings:
                print("  " + warning)
        if errors:
            print("*** %d ERROR%s:" % (len(errors), _plurals(len(errors)).upper()))
            for error in errors:
                print("  " + error)

        return not (len(warnings) or len(errors))

    def isconsistent(self):
        """
        Note that an Data object can be 'consistent' in this sense without being 'valid' as checked by isvalid().

        Returns
        -------
        True
            If the object is entirely self-contained,
        i.e. all cross-references to wavelength tables, arrays,
        stations etc. in the measurements refer to elements which are
        stored in the oifits object.

        False
            Otherwise
        """

        for vis in self.vis:
            if vis.array and (vis.array not in self.array.values()):
                print(
                    "A visibility measurement (0x%x) refers to an array which is not inside the main oifits object."
                    % id(vis)
                )
                return False
            if (vis.station[0] and (vis.station[0] not in vis.array.station)) or (
                vis.station[1] and (vis.station[1] not in vis.array.station)
            ):
                print(
                    "A visibility measurement (0x%x) refers to a station which is not inside the main oifits object."
                    % id(vis)
                )
                return False
            if vis.wavelength not in self.wavelength.values():
                print(
                    "A visibility measurement (0x%x) refers to a wavelength table which is not inside the main oifits object."
                    % id(vis)
                )
                return False
            if vis.target not in self.target:
                print(
                    "A visibility measurement (0x%x) refers to a target which is not inside the main oifits object."
                    % id(vis)
                )
                return False

        for vis2 in self.vis2:
            if vis2.array and (vis2.array not in self.array.values()):
                print(
                    "A visibility^2 measurement (0x%x) refers to an array which is not inside the main oifits object."
                    % id(vis2)
                )
                return False
            if (vis2.station[0] and (vis2.station[0] not in vis2.array.station)) or (
                vis2.station[1] and (vis2.station[1] not in vis2.array.station)
            ):
                print(
                    "A visibility^2 measurement (0x%x) refers to a station which is not inside the main oifits object."
                    % id(vis)
                )
                return False
            if vis2.wavelength not in self.wavelength.values():
                print(
                    "A visibility^2 measurement (0x%x) refers to a wavelength table which is not inside the main oifits object."
                    % id(vis2)
                )
                return False
            if vis2.target not in self.target:
                print(
                    "A visibility^2 measurement (0x%x) refers to a target which is not inside the main oifits object."
                    % id(vis2)
                )
                return False

        for t3 in self.t3:
            if t3.array and (t3.array not in self.array.values()):
                print(
                    "A closure phase measurement (0x%x) refers to an array which is not inside the main oifits object."
                    % id(t3)
                )
                return False
            if (
                (t3.station[0] and (t3.station[0] not in t3.array.station))
                or (t3.station[1] and (t3.station[1] not in t3.array.station))
                or (t3.station[2] and (t3.station[2] not in t3.array.station))
            ):
                print(
                    "A closure phase measurement (0x%x) refers to a station which is not inside the main oifits object."
                    % id(t3)
                )
                return False
            if t3.wavelength not in self.wavelength.values():
                print(
                    "A closure phase measurement (0x%x) refers to a wavelength table which is not inside the main oifits object."
                    % id(t3)
                )
                return False
            if t3.target not in self.target:
                print(
                    "A closure phase measurement (0x%x) refers to a target which is not inside the main oifits object."
                    % id(t3)
                )
                return False

        return True

    def info(self, recursive=True, verbose=0):
        """
        Print out a summary of the contents of the Data object.

        Parameters
        ----------
        recursive : bool, defaults to True
            More specific information of each components
        verbose : int
            Increases the verbosity level

        """

        if self.wavelength:
            wavelengths = 0
            if recursive:
                print(
                    "===================================================================="
                )
                print("SUMMARY OF WAVELENGTH TABLES")
                print(
                    "===================================================================="
                )
            for key in self.wavelength.keys():
                wavelengths += len(self.wavelength[key].eff_wave)
                if recursive:
                    print("'%s': %s" % (key, str(self.wavelength[key])))
            print(
                "%d wavelength table%s with %d wavelength%s in total"
                % (
                    len(self.wavelength),
                    _plurals(len(self.wavelength)),
                    wavelengths,
                    _plurals(wavelengths),
                )
            )
        if self.target.size:
            if recursive:
                print(
                    "===================================================================="
                )
                print("SUMMARY OF TARGET TABLES")
                print(
                    "===================================================================="
                )
                for target in self.target:
                    target.info()
            print("%d target%s" % (len(self.target), _plurals(len(self.target))))
        if self.array:
            stations = 0
            if recursive:
                print(
                    "===================================================================="
                )
                print("SUMMARY OF ARRAY TABLES")
                print(
                    "===================================================================="
                )
            for key in self.array.keys():
                if recursive:
                    print
                    key + ":"
                    self.array[key].info(verbose=verbose)
                stations += len(self.array[key].station)
            print(
                "%d array%s with %d station%s"
                % (
                    len(self.array),
                    _plurals(len(self.array)),
                    stations,
                    _plurals(stations),
                )
            )
        if self.vis.size:
            if recursive:
                print(
                    "===================================================================="
                )
                print("SUMMARY OF VISIBILITY MEASUREMENTS")
                print(
                    "===================================================================="
                )
                for vis in self.vis:
                    vis.info()
            print(
                "%d visibility measurement%s" % (len(self.vis), _plurals(len(self.vis)))
            )
        if self.vis2.size:
            if recursive:
                print(
                    "===================================================================="
                )
                print("SUMMARY OF VISIBILITY^2 MEASUREMENTS")
                print(
                    "===================================================================="
                )
                for vis2 in self.vis2:
                    vis2.info()
            print(
                "%d visibility^2 measurement%s"
                % (len(self.vis2), _plurals(len(self.vis2)))
            )
        if self.t3.size:
            if recursive:
                print(
                    "===================================================================="
                )
                print("SUMMARY OF T3 MEASUREMENTS")
                print(
                    "===================================================================="
                )
                for t3 in self.t3:
                    t3.info()
            print(
                "%d closure phase measurement%s"
                % (len(self.t3), _plurals(len(self.t3)))
            )

    def save(self, filename):
        """
        Write the contents of the oifits object to a file in OIFITS
        format.

        Parameters
        ----------
        filename : str
            Name of the OIFITS file to be parsed.

        Raises
        ------
        TypeError
            If the Data Clase is inconsistent.

        """

        if not self.isconsistent():
            raise TypeError

        hdulist = fits.HDUList()
        hdu = fits.PrimaryHDU()
        hdu.header.update(
            "DATE",
            datetime.datetime.now().strftime(format="%F"),
            comment="Creation date",
        )
        hdu.header.add_comment("Written by oifits version 0.1.0")
        hdu.header.add_comment("http://www.mpia-hd.mpg.de/homes/boley/oifits/")

        wavelengthmap = {}
        hdulist.append(hdu)
        for insname, wavelength in self.wavelength.iteritems():
            wavelengthmap[id(wavelength)] = insname
            hdu = fits.new_table(
                fits.ColDefs(
                    (
                        fits.Column(
                            name="EFF_WAVE",
                            format="1E",
                            unit="METERS",
                            array=wavelength.eff_wave,
                        ),
                        fits.Column(
                            name="EFF_BAND",
                            format="1E",
                            unit="METERS",
                            array=wavelength.eff_band,
                        ),
                    )
                )
            )
            hdu.header.update("EXTNAME", "OI_WAVELENGTH")
            hdu.header.update("OI_REVN", 1, "Revision number of the table definition")
            hdu.header.update(
                "INSNAME", insname, "Name of detector, for cross-referencing"
            )
            hdulist.append(hdu)

        targetmap = {}
        if self.target.size:
            target_id = []
            target = []
            raep0 = []
            decep0 = []
            equinox = []
            ra_err = []
            dec_err = []
            sysvel = []
            veltyp = []
            veldef = []
            pmra = []
            pmdec = []
            pmra_err = []
            pmdec_err = []
            parallax = []
            para_err = []
            spectyp = []
            for i, targ in enumerate(self.target):
                key = i + 1
                targetmap[id(targ)] = key
                target_id.append(key)
                target.append(targ.target)
                raep0.append(targ.raep0)
                decep0.append(targ.decep0)
                equinox.append(targ.equinox)
                ra_err.append(targ.ra_err)
                dec_err.append(targ.dec_err)
                sysvel.append(targ.sysvel)
                veltyp.append(targ.veltyp)
                veldef.append(targ.veldef)
                pmra.append(targ.pmra)
                pmdec.append(targ.pmdec)
                pmra_err.append(targ.pmra_err)
                pmdec_err.append(targ.pmdec_err)
                parallax.append(targ.parallax)
                para_err.append(targ.para_err)
                spectyp.append(targ.spectyp)

            hdu = fits.new_table(
                fits.ColDefs(
                    (
                        fits.Column(name="TARGET_ID", format="1I", array=target_id),
                        fits.Column(name="TARGET", format="16A", array=target),
                        fits.Column(
                            name="RAEP0", format="D1", unit="DEGREES", array=raep0
                        ),
                        fits.Column(
                            name="DECEP0", format="D1", unit="DEGREES", array=decep0
                        ),
                        fits.Column(
                            name="EQUINOX", format="E1", unit="YEARS", array=equinox
                        ),
                        fits.Column(
                            name="RA_ERR", format="D1", unit="DEGREES", array=ra_err
                        ),
                        fits.Column(
                            name="DEC_ERR", format="D1", unit="DEGREES", array=dec_err
                        ),
                        fits.Column(
                            name="SYSVEL", format="D1", unit="M/S", array=sysvel
                        ),
                        fits.Column(name="VELTYP", format="A8", array=veltyp),
                        fits.Column(name="VELDEF", format="A8", array=veldef),
                        fits.Column(
                            name="PMRA", format="D1", unit="DEG/YR", array=pmra
                        ),
                        fits.Column(
                            name="PMDEC", format="D1", unit="DEG/YR", array=pmdec
                        ),
                        fits.Column(
                            name="PMRA_ERR", format="D1", unit="DEG/YR", array=pmra_err
                        ),
                        fits.Column(
                            name="PMDEC_ERR",
                            format="D1",
                            unit="DEG/YR",
                            array=pmdec_err,
                        ),
                        fits.Column(
                            name="PARALLAX", format="E1", unit="DEGREES", array=parallax
                        ),
                        fits.Column(
                            name="PARA_ERR", format="E1", unit="DEGREES", array=para_err
                        ),
                        fits.Column(name="SPECTYP", format="A16", array=spectyp),
                    )
                )
            )
            hdu.header.update("EXTNAME", "OI_TARGET")
            hdu.header.update("OI_REVN", 1, "Revision number of the table definition")
            hdulist.append(hdu)

        arraymap = {}
        stationmap = {}
        for arrname, array in self.array.iteritems():
            arraymap[id(array)] = arrname
            tel_name = []
            sta_name = []
            sta_index = []
            diameter = []
            staxyz = []
            if array.station.size:
                for i, station in enumerate(array.station, 1):
                    stationmap[id(station)] = i
                    tel_name.append(station.tel_name)
                    sta_name.append(station.sta_name)
                    sta_index.append(i)
                    diameter.append(station.diameter)
                    staxyz.append(station.staxyz)
                hdu = fits.new_table(
                    fits.ColDefs(
                        (
                            fits.Column(name="TEL_NAME", format="16A", array=tel_name),
                            fits.Column(name="STA_NAME", format="16A", array=sta_name),
                            fits.Column(name="STA_INDEX", format="1I", array=sta_index),
                            fits.Column(
                                name="DIAMETER",
                                unit="METERS",
                                format="1E",
                                array=diameter,
                            ),
                            fits.Column(
                                name="STAXYZ", unit="METERS", format="3D", array=staxyz
                            ),
                        )
                    )
                )
            hdu.header.update("EXTNAME", "OI_ARRAY")
            hdu.header.update("OI_REVN", 1, "Revision number of the table definition")
            hdu.header.update(
                "ARRNAME", arrname, comment="Array name, for cross-referencing"
            )
            hdu.header.update("FRAME", array.frame, comment="Coordinate frame")
            hdu.header.update(
                "ARRAYX", array.arrxyz[0], comment="Array center x coordinate (m)"
            )
            hdu.header.update(
                "ARRAYY", array.arrxyz[1], comment="Array center y coordinate (m)"
            )
            hdu.header.update(
                "ARRAYZ", array.arrxyz[2], comment="Array center z coordinate (m)"
            )
            hdulist.append(hdu)

        if self.vis.size:
            # The tables are grouped by ARRNAME and INSNAME -- all
            # observations which have the same ARRNAME and INSNAME are
            # put into a single FITS binary table.
            tables = {}
            for vis in self.vis:
                nwave = vis.wavelength.eff_wave.size
                if vis.array:
                    key = (arraymap[id(vis.array)], wavelengthmap[id(vis.wavelength)])
                else:
                    key = (None, wavelengthmap[id(vis.wavelength)])
                if key in tables.keys():
                    data = tables[key]
                else:
                    data = tables[key] = {
                        "target_id": [],
                        "time": [],
                        "mjd": [],
                        "int_time": [],
                        "visamp": [],
                        "visamperr": [],
                        "visphi": [],
                        "visphierr": [],
                        "cflux": [],
                        "cfluxerr": [],
                        "ucoord": [],
                        "vcoord": [],
                        "sta_index": [],
                        "flag": [],
                    }
                data["target_id"].append(targetmap[id(vis.target)])
                if vis.timeobs:
                    time = vis.timeobs - refdate
                    data["time"].append(time.days * 24.0 * 3600.0 + time.seconds)
                    mjd = (vis.timeobs - _mjdzero).days + (
                        vis.timeobs - _mjdzero
                    ).seconds / 3600.0 / 24.0
                    data["mjd"].append(mjd)
                else:
                    data["time"].append(None)
                    data["mjd"].append(None)
                data["int_time"].append(vis.int_time)
                if nwave == 1:
                    data["visamp"].append(vis.visamp[0])
                    data["visamperr"].append(vis.visamperr[0])
                    data["visphi"].append(vis.visphi[0])
                    data["visphierr"].append(vis.visphierr[0])
                    data["flag"].append(vis.flag[0])
                    if vis.cflux != None:
                        data["cflux"].append(vis.cflux[0])
                    else:
                        data["cflux"].append(None)
                    if vis.cfluxerr != None:
                        data["cfluxerr"].append(vis.cfluxerr[0])
                    else:
                        data["cfluxerr"].append(None)
                else:
                    data["visamp"].append(vis.visamp)
                    data["visamperr"].append(vis.visamperr)
                    data["visphi"].append(vis.visphi)
                    data["visphierr"].append(vis.visphierr)
                    data["flag"].append(vis.flag)
                    if vis.cflux != None:
                        data["cflux"].append(vis.cflux)
                    else:
                        cflux = np.empty(nwave)
                        cflux[:] = None
                        data["cflux"].append(cflux)
                    if vis.cfluxerr != None:
                        data["cfluxerr"].append(vis.cfluxerr)
                    else:
                        cfluxerr = np.empty(nwave)
                        cfluxerr[:] = None
                        data["cfluxerr"].append(cfluxerr)
                data["ucoord"].append(vis.ucoord)
                data["vcoord"].append(vis.vcoord)
                if vis.station[0] and vis.station[1]:
                    data["sta_index"].append(
                        [stationmap[id(vis.station[0])], stationmap[id(vis.station[1])]]
                    )
                else:
                    data["sta_index"].append([-1, -1])
            for key in tables.keys():
                data = tables[key]
                nwave = self.wavelength[key[1]].eff_wave.size

                hdu = fits.new_table(
                    fits.ColDefs(
                        [
                            fits.Column(
                                name="TARGET_ID", format="1I", array=data["target_id"]
                            ),
                            fits.Column(
                                name="TIME",
                                format="1D",
                                unit="SECONDS",
                                array=data["time"],
                            ),
                            fits.Column(
                                name="MJD", unit="DAY", format="1D", array=data["mjd"]
                            ),
                            fits.Column(
                                name="INT_TIME",
                                format="1D",
                                unit="SECONDS",
                                array=data["int_time"],
                            ),
                            fits.Column(
                                name="VISAMP",
                                format="%dD" % nwave,
                                array=data["visamp"],
                            ),
                            fits.Column(
                                name="VISAMPERR",
                                format="%dD" % nwave,
                                array=data["visamperr"],
                            ),
                            fits.Column(
                                name="VISPHI",
                                unit="DEGREES",
                                format="%dD" % nwave,
                                array=data["visphi"],
                            ),
                            fits.Column(
                                name="VISPHIERR",
                                unit="DEGREES",
                                format="%dD" % nwave,
                                array=data["visphierr"],
                            ),
                            fits.Column(
                                name="CFLUX", format="%dD" % nwave, array=data["cflux"]
                            ),
                            fits.Column(
                                name="CFLUXERR",
                                format="%dD" % nwave,
                                array=data["cfluxerr"],
                            ),
                            fits.Column(
                                name="UCOORD",
                                format="1D",
                                unit="METERS",
                                array=data["ucoord"],
                            ),
                            fits.Column(
                                name="VCOORD",
                                format="1D",
                                unit="METERS",
                                array=data["vcoord"],
                            ),
                            fits.Column(
                                name="STA_INDEX",
                                format="2I",
                                array=data["sta_index"],
                                null=-1,
                            ),
                            fits.Column(name="FLAG", format="%dL" % nwave),
                        ]
                    )
                )

                # Setting the data of logical field via the
                # fits.Column call above with length > 1 (eg
                # format='171L' above) seems to be broken, atleast as
                # of fits 2.2.2
                hdu.data.field("FLAG").setfield(data["flag"], bool)
                hdu.header.update("EXTNAME", "OI_VIS")
                hdu.header.update(
                    "OI_REVN", 1, "Revision number of the table definition"
                )
                hdu.header.update(
                    "DATE-OBS",
                    refdate.strftime("%F"),
                    comment="Zero-point for table (UTC)",
                )
                if key[0]:
                    hdu.header.update(
                        "ARRNAME", key[0], "Identifies corresponding OI_ARRAY"
                    )
                hdu.header.update(
                    "INSNAME", key[1], "Identifies corresponding OI_WAVELENGTH table"
                )
                hdulist.append(hdu)

        if self.vis2.size:
            tables = {}
            for vis in self.vis2:
                nwave = vis.wavelength.eff_wave.size
                if vis.array:
                    key = (arraymap[id(vis.array)], wavelengthmap[id(vis.wavelength)])
                else:
                    key = (None, wavelengthmap[id(vis.wavelength)])
                if key in tables.keys():
                    data = tables[key]
                else:
                    data = tables[key] = {
                        "target_id": [],
                        "time": [],
                        "mjd": [],
                        "int_time": [],
                        "vis2data": [],
                        "vis2err": [],
                        "ucoord": [],
                        "vcoord": [],
                        "sta_index": [],
                        "flag": [],
                    }
                data["target_id"].append(targetmap[id(vis.target)])
                if vis.timeobs:
                    time = vis.timeobs - refdate
                    data["time"].append(time.days * 24.0 * 3600.0 + time.seconds)
                    mjd = (vis.timeobs - _mjdzero).days + (
                        vis.timeobs - _mjdzero
                    ).seconds / 3600.0 / 24.0
                    data["mjd"].append(mjd)
                else:
                    data["time"].append(None)
                    data["mjd"].append(None)
                data["int_time"].append(vis.int_time)
                if nwave == 1:
                    data["vis2data"].append(vis.vis2data[0])
                    data["vis2err"].append(vis.vis2err[0])
                    data["flag"].append(vis.flag[0])
                else:
                    data["vis2data"].append(vis.vis2data)
                    data["vis2err"].append(vis.vis2err)
                    data["flag"].append(vis.flag)
                data["ucoord"].append(vis.ucoord)
                data["vcoord"].append(vis.vcoord)
                if vis.station[0] and vis.station[1]:
                    data["sta_index"].append(
                        [stationmap[id(vis.station[0])], stationmap[id(vis.station[1])]]
                    )
                else:
                    data["sta_index"].append([-1, -1])
            for key in tables.keys():
                data = tables[key]
                nwave = self.wavelength[key[1]].eff_wave.size

                hdu = fits.new_table(
                    fits.ColDefs(
                        [
                            fits.Column(
                                name="TARGET_ID", format="1I", array=data["target_id"]
                            ),
                            fits.Column(
                                name="TIME",
                                format="1D",
                                unit="SECONDS",
                                array=data["time"],
                            ),
                            fits.Column(
                                name="MJD", format="1D", unit="DAY", array=data["mjd"]
                            ),
                            fits.Column(
                                name="INT_TIME",
                                format="1D",
                                unit="SECONDS",
                                array=data["int_time"],
                            ),
                            fits.Column(
                                name="VIS2DATA",
                                format="%dD" % nwave,
                                array=data["vis2data"],
                            ),
                            fits.Column(
                                name="VIS2ERR",
                                format="%dD" % nwave,
                                array=data["vis2err"],
                            ),
                            fits.Column(
                                name="UCOORD",
                                format="1D",
                                unit="METERS",
                                array=data["ucoord"],
                            ),
                            fits.Column(
                                name="VCOORD",
                                format="1D",
                                unit="METERS",
                                array=data["vcoord"],
                            ),
                            fits.Column(
                                name="STA_INDEX",
                                format="2I",
                                array=data["sta_index"],
                                null=-1,
                            ),
                            fits.Column(
                                name="FLAG", format="%dL" % nwave, array=data["flag"]
                            ),
                        ]
                    )
                )
                # Setting the data of logical field via the
                # fits.Column call above with length > 1 (eg
                # format='171L' above) seems to be broken, atleast as
                # of fits 2.2.2
                hdu.data.field("FLAG").setfield(data["flag"], bool)
                hdu.header.update("EXTNAME", "OI_VIS2")
                hdu.header.update(
                    "OI_REVN", 1, "Revision number of the table definition"
                )
                hdu.header.update(
                    "DATE-OBS",
                    refdate.strftime("%F"),
                    comment="Zero-point for table (UTC)",
                )
                if key[0]:
                    hdu.header.update(
                        "ARRNAME", key[0], "Identifies corresponding OI_ARRAY"
                    )
                hdu.header.update(
                    "INSNAME", key[1], "Identifies corresponding OI_WAVELENGTH table"
                )
                hdulist.append(hdu)

        if self.t3.size:
            tables = {}
            for t3 in self.t3:
                nwave = t3.wavelength.eff_wave.size
                if t3.array:
                    key = (arraymap[id(t3.array)], wavelengthmap[id(t3.wavelength)])
                else:
                    key = (None, wavelengthmap[id(t3.wavelength)])
                if key in tables.keys():
                    data = tables[key]
                else:
                    data = tables[key] = {
                        "target_id": [],
                        "time": [],
                        "mjd": [],
                        "int_time": [],
                        "t3amp": [],
                        "t3amperr": [],
                        "t3phi": [],
                        "t3phierr": [],
                        "u1coord": [],
                        "v1coord": [],
                        "u2coord": [],
                        "v2coord": [],
                        "sta_index": [],
                        "flag": [],
                    }
                data["target_id"].append(targetmap[id(t3.target)])
                if t3.timeobs:
                    time = t3.timeobs - refdate
                    data["time"].append(time.days * 24.0 * 3600.0 + time.seconds)
                    mjd = (t3.timeobs - _mjdzero).days + (
                        t3.timeobs - _mjdzero
                    ).seconds / 3600.0 / 24.0
                    data["mjd"].append(mjd)
                else:
                    data["time"].append(None)
                    data["mjd"].append(None)
                data["int_time"].append(t3.int_time)
                if nwave == 1:
                    data["t3amp"].append(t3.t3amp[0])
                    data["t3amperr"].append(t3.t3amperr[0])
                    data["t3phi"].append(t3.t3phi[0])
                    data["t3phierr"].append(t3.t3phierr[0])
                    data["flag"].append(t3.flag[0])
                else:
                    data["t3amp"].append(t3.t3amp)
                    data["t3amperr"].append(t3.t3amperr)
                    data["t3phi"].append(t3.t3phi)
                    data["t3phierr"].append(t3.t3phierr)
                    data["flag"].append(t3.flag)
                data["u1coord"].append(t3.u1coord)
                data["v1coord"].append(t3.v1coord)
                data["u2coord"].append(t3.u2coord)
                data["v2coord"].append(t3.v2coord)
                if t3.station[0] and t3.station[1] and t3.station[2]:
                    data["sta_index"].append(
                        [
                            stationmap[id(t3.station[0])],
                            stationmap[id(t3.station[1])],
                            stationmap[id(t3.station[2])],
                        ]
                    )
                else:
                    data["sta_index"].append([-1, -1, -1])
            for key in tables.keys():
                data = tables[key]
                nwave = self.wavelength[key[1]].eff_wave.size

                hdu = fits.new_table(
                    fits.ColDefs(
                        (
                            fits.Column(
                                name="TARGET_ID", format="1I", array=data["target_id"]
                            ),
                            fits.Column(
                                name="TIME",
                                format="1D",
                                unit="SECONDS",
                                array=data["time"],
                            ),
                            fits.Column(
                                name="MJD", format="1D", unit="DAY", array=data["mjd"]
                            ),
                            fits.Column(
                                name="INT_TIME",
                                format="1D",
                                unit="SECONDS",
                                array=data["int_time"],
                            ),
                            fits.Column(
                                name="T3AMP", format="%dD" % nwave, array=data["t3amp"]
                            ),
                            fits.Column(
                                name="T3AMPERR",
                                format="%dD" % nwave,
                                array=data["t3amperr"],
                            ),
                            fits.Column(
                                name="T3PHI",
                                format="%dD" % nwave,
                                unit="DEGREES",
                                array=data["t3phi"],
                            ),
                            fits.Column(
                                name="T3PHIERR",
                                format="%dD" % nwave,
                                unit="DEGREES",
                                array=data["t3phierr"],
                            ),
                            fits.Column(
                                name="U1COORD",
                                format="1D",
                                unit="METERS",
                                array=data["u1coord"],
                            ),
                            fits.Column(
                                name="V1COORD",
                                format="1D",
                                unit="METERS",
                                array=data["v1coord"],
                            ),
                            fits.Column(
                                name="U2COORD",
                                format="1D",
                                unit="METERS",
                                array=data["u2coord"],
                            ),
                            fits.Column(
                                name="V2COORD",
                                format="1D",
                                unit="METERS",
                                array=data["v2coord"],
                            ),
                            fits.Column(
                                name="STA_INDEX",
                                format="3I",
                                array=data["sta_index"],
                                null=-1,
                            ),
                            fits.Column(
                                name="FLAG", format="%dL" % nwave, array=data["flag"]
                            ),
                        )
                    )
                )
                # Setting the data of logical field via the
                # fits.Column call above with length > 1 (eg
                # format='171L' above) seems to be broken, atleast as
                # of fits 2.2.2
                hdu.data.field("FLAG").setfield(data["flag"], bool)
                hdu.header.update("EXTNAME", "OI_T3")
                hdu.header.update(
                    "OI_REVN", 1, "Revision number of the table definition"
                )
                hdu.header.update(
                    "DATE-OBS", refdate.strftime("%F"), "Zero-point for table (UTC)"
                )
                if key[0]:
                    hdu.header.update(
                        "ARRNAME", key[0], "Identifies corresponding OI_ARRAY"
                    )
                hdu.header.update(
                    "INSNAME", key[1], "Identifies corresponding OI_WAVELENGTH table"
                )
                hdulist.append(hdu)

        hdulist.writeto(filename, clobber=True)
