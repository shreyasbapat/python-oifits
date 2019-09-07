"""
These Classes are inspired by Paul Boley's code for OIFITS Data!
Copyright (c) 2013, Paul Boley
Copyright (c) 2019, Shreyas Bapat
"""

import datetime

import numpy as np

from .utils import _angpoint, _array_eq, _plurals


class OI_TARGET:
    def __init__(
        self,
        target,
        raep0,
        decep0,
        equinox=2000.0,
        ra_err=0.0,
        dec_err=0.0,
        sysvel=0.0,
        veltyp="TOPCENT",
        veldef="OPTICAL",
        pmra=0.0,
        pmdec=0.0,
        pmra_err=0.0,
        pmdec_err=0.0,
        parallax=0.0,
        para_err=0.0,
        spectyp="UNKNOWN",
    ):
        self.target = target
        self.raep0 = _angpoint(raep0)
        self.decep0 = _angpoint(decep0)
        self.equinox = equinox
        self.ra_err = ra_err
        self.dec_err = dec_err
        self.sysvel = sysvel
        self.veltyp = veltyp
        self.veldef = veldef
        self.pmra = pmra
        self.pmdec = pmdec
        self.pmra_err = pmra_err
        self.pmdec_err = pmdec_err
        self.parallax = parallax
        self.para_err = para_err
        self.spectyp = spectyp

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        return not (
            (self.target != other.target)
            or (self.raep0 != other.raep0)
            or (self.decep0 != other.decep0)
            or (self.equinox != other.equinox)
            or (self.ra_err != other.ra_err)
            or (self.dec_err != other.dec_err)
            or (self.sysvel != other.sysvel)
            or (self.veltyp != other.veltyp)
            or (self.veldef != other.veldef)
            or (self.pmra != other.pmra)
            or (self.pmdec != other.pmdec)
            or (self.pmra_err != other.pmra_err)
            or (self.pmdec_err != other.pmdec_err)
            or (self.parallax != other.parallax)
            or (self.para_err != other.para_err)
            or (self.spectyp != other.spectyp)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "%s: %s %s (%g)" % (
            self.target,
            self.raep0.ashms(),
            self.decep0.asdms(),
            self.equinox,
        )

    def info(self):
        print(str(self))


class OI_WAVELENGTH:
    def __init__(self, eff_wave, eff_band=None):
        self.eff_wave = np.array(eff_wave, dtype=np.float64).reshape(-1)
        if eff_band == None:
            eff_band = np.zeros_like(eff_wave)
        self.eff_band = np.array(eff_band, dtype=np.float64).reshape(-1)

    def __eq__(self, other):

        if type(self) != type(other):
            return False

        return not (
            (not _array_eq(self.eff_wave, other.eff_wave))
            or (not _array_eq(self.eff_band, other.eff_band))
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%d wavelength%s (%.3g-%.3g um)" % (
            len(self.eff_wave),
            _plurals(len(self.eff_wave)),
            1e6 * np.min(self.eff_wave),
            1e6 * np.max(self.eff_wave),
        )

    def info(self):
        print(str(self))


class OI_VIS:
    """
    Class for storing visibility amplitude and differential phase data.
    To access the data, use the following hidden attributes:

    visamp, visamperr, visphi, visphierr, flag;
    and possibly cflux, cfluxerr.

    """

    def __init__(
        self,
        timeobs,
        int_time,
        visamp,
        visamperr,
        visphi,
        visphierr,
        flag,
        ucoord,
        vcoord,
        wavelength,
        target,
        array=None,
        station=(None, None),
        cflux=None,
        cfluxerr=None,
    ):
        self.timeobs = timeobs
        self.array = array
        self.wavelength = wavelength
        self.target = target
        self.int_time = int_time
        self._visamp = np.array(visamp, dtype=np.float64).reshape(-1)
        self._visamperr = np.array(visamperr, dtype=np.float64).reshape(-1)
        self._visphi = np.array(visphi, dtype=np.float64).reshape(-1)
        self._visphierr = np.array(visphierr, dtype=np.float64).reshape(-1)
        if cflux != None:
            self._cflux = np.array(cflux, dtype=np.float64).reshape(-1)
        else:
            self._cflux = None
        if cfluxerr != None:
            self._cfluxerr = np.array(cfluxerr, dtype=np.float64).reshape(-1)
        else:
            self._cfluxerr = None
        self.flag = np.array(flag, dtype=bool).reshape(-1)
        self.ucoord = ucoord
        self.vcoord = vcoord
        self.station = station

    def __eq__(self, other):

        if type(self) != type(other):
            return False

        return not (
            (self.timeobs != other.timeobs)
            or (self.array != other.array)
            or (self.wavelength != other.wavelength)
            or (self.target != other.target)
            or (self.int_time != other.int_time)
            or (self.ucoord != other.ucoord)
            or (self.vcoord != other.vcoord)
            or (self.array != other.array)
            or (self.station != other.station)
            or (not _array_eq(self.visamp, other.visamp))
            or (not _array_eq(self.visamperr, other.visamperr))
            or (not _array_eq(self.visphi, other.visphi))
            or (not _array_eq(self.visphierr, other.visphierr))
            or (not _array_eq(self.flag, other.flag))
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattr__(self, attrname):
        if attrname in ("visamp", "visamperr", "visphi", "visphierr"):
            return np.ma.masked_array(self.__dict__["_" + attrname], mask=self.flag)
        elif attrname in ("cflux", "cfluxerr"):
            if self.__dict__["_" + attrname] != None:
                return np.ma.masked_array(self.__dict__["_" + attrname], mask=self.flag)
            else:
                return None
        else:
            raise AttributeError(attrname)

    def __setattr__(self, attrname, value):
        if attrname in (
            "visamp",
            "visamperr",
            "visphi",
            "visphierr",
            "cflux",
            "cfluxerr",
        ):
            self.__dict__["_" + attrname] = value
        else:
            self.__dict__[attrname] = value

    def __repr__(self):
        meanvis = np.ma.mean(self.visamp)
        if self.station[0] and self.station[1]:
            baselinename = (
                " (" + self.station[0].sta_name + self.station[1].sta_name + ")"
            )
        else:
            baselinename = ""
        return (
            "%s %s%s: %d point%s (%d masked), B = %5.1f m, PA = %5.1f deg, <V> = %4.2g"
            % (
                self.target.target,
                self.timeobs.strftime("%F %T"),
                baselinename,
                len(self.visamp),
                _plurals(len(self.visamp)),
                np.sum(self.flag),
                np.sqrt(self.ucoord ** 2 + self.vcoord ** 2),
                np.arctan(self.ucoord / self.vcoord) * 180.0 / np.pi % 180.0,
                meanvis,
            )
        )

    def info(self):
        print(str(self))


class OI_VIS2:
    """
    Class for storing squared visibility amplitude data.
    To access the data, use the following hidden attributes:

    vis2data, vis2err

    """

    def __init__(
        self,
        timeobs,
        int_time,
        vis2data,
        vis2err,
        flag,
        ucoord,
        vcoord,
        wavelength,
        target,
        array=None,
        station=(None, None),
    ):
        self.timeobs = timeobs
        self.array = array
        self.wavelength = wavelength
        self.target = target
        self.int_time = int_time
        self._vis2data = np.array(vis2data, dtype=np.float64).reshape(-1)
        self._vis2err = np.array(vis2err, dtype=np.float64).reshape(-1)
        self.flag = np.array(flag, dtype=bool).reshape(-1)
        self.ucoord = ucoord
        self.vcoord = vcoord
        self.station = station

    def __eq__(self, other):

        if type(self) != type(other):
            return False

        return not (
            (self.timeobs != other.timeobs)
            or (self.array != other.array)
            or (self.wavelength != other.wavelength)
            or (self.target != other.target)
            or (self.int_time != other.int_time)
            or (self.ucoord != other.ucoord)
            or (self.vcoord != other.vcoord)
            or (self.array != other.array)
            or (self.station != other.station)
            or (not _array_eq(self.vis2data, other.vis2data))
            or (not _array_eq(self.vis2err, other.vis2err))
            or (not _array_eq(self.flag, other.flag))
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattr__(self, attrname):
        if attrname in ("vis2data", "vis2err"):
            return np.ma.masked_array(self.__dict__["_" + attrname], mask=self.flag)
        else:
            raise AttributeError(attrname)

    def __setattr__(self, attrname, value):
        if attrname in ("vis2data", "vis2err"):
            self.__dict__["_" + attrname] = value
        else:
            self.__dict__[attrname] = value

    def __repr__(self):
        meanvis = np.ma.mean(self.vis2data)
        if self.station[0] and self.station[1]:
            baselinename = (
                " (" + self.station[0].sta_name + self.station[1].sta_name + ")"
            )
        else:
            baselinename = ""
        return (
            "%s %s%s: %d point%s (%d masked), B = %5.1f m, PA = %5.1f deg, <V^2> = %4.2g"
            % (
                self.target.target,
                self.timeobs.strftime("%F %T"),
                baselinename,
                len(self.vis2data),
                _plurals(len(self.vis2data)),
                np.sum(self.flag),
                np.sqrt(self.ucoord ** 2 + self.vcoord ** 2),
                np.arctan(self.ucoord / self.vcoord) * 180.0 / np.pi % 180.0,
                meanvis,
            )
        )

    def info(self):
        print(str(self))


class OI_T3:
    """
    Class for storing triple product and closure phase data.
    To access the data, use the following hidden attributes:

    t3amp, t3amperr, t3phi, t3phierr

    """

    def __init__(
        self,
        timeobs,
        int_time,
        t3amp,
        t3amperr,
        t3phi,
        t3phierr,
        flag,
        u1coord,
        v1coord,
        u2coord,
        v2coord,
        wavelength,
        target,
        array=None,
        station=(None, None, None),
    ):
        self.timeobs = timeobs
        self.array = array
        self.wavelength = wavelength
        self.target = target
        self.int_time = int_time
        self._t3amp = np.array(t3amp, dtype=np.float64).reshape(-1)
        self._t3amperr = np.array(t3amperr, dtype=np.float64).reshape(-1)
        self._t3phi = np.array(t3phi, dtype=np.float64).reshape(-1)
        self._t3phierr = np.array(t3phierr, dtype=np.float64).reshape(-1)
        self.flag = np.array(flag, dtype=bool).reshape(-1)
        self.u1coord = u1coord
        self.v1coord = v1coord
        self.u2coord = u2coord
        self.v2coord = v2coord
        self.station = station

    def __eq__(self, other):

        if type(self) != type(other):
            return False

        return not (
            (self.timeobs != other.timeobs)
            or (self.array != other.array)
            or (self.wavelength != other.wavelength)
            or (self.target != other.target)
            or (self.int_time != other.int_time)
            or (self.u1coord != other.u1coord)
            or (self.v1coord != other.v1coord)
            or (self.u2coord != other.u2coord)
            or (self.v2coord != other.v2coord)
            or (self.array != other.array)
            or (self.station != other.station)
            or (not _array_eq(self.t3amp, other.t3amp))
            or (not _array_eq(self.t3amperr, other.t3amperr))
            or (not _array_eq(self.t3phi, other.t3phi))
            or (not _array_eq(self.t3phierr, other.t3phierr))
            or (not _array_eq(self.flag, other.flag))
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattr__(self, attrname):
        if attrname in ("t3amp", "t3amperr", "t3phi", "t3phierr"):
            return np.ma.masked_array(self.__dict__["_" + attrname], mask=self.flag)
        else:
            raise AttributeError(attrname)

    def __setattr__(self, attrname, value):
        if attrname in ("vis2data", "vis2err"):
            self.__dict__["_" + attrname] = value
        else:
            self.__dict__[attrname] = value

    def __repr__(self):
        meant3 = np.mean(self.t3amp[np.where(self.flag == False)])
        if self.station[0] and self.station[1] and self.station[2]:
            baselinename = (
                " ("
                + self.station[0].sta_name
                + self.station[1].sta_name
                + self.station[2].sta_name
                + ")"
            )
        else:
            baselinename = ""
        return "%s %s%s: %d point%s (%d masked), B = %5.1fm, %5.1fm, <T3> = %4.2g" % (
            self.target.target,
            self.timeobs.strftime("%F %T"),
            baselinename,
            len(self.t3amp),
            _plurals(len(self.t3amp)),
            np.sum(self.flag),
            np.sqrt(self.u1coord ** 2 + self.v1coord ** 2),
            np.sqrt(self.u2coord ** 2 + self.v2coord ** 2),
            meant3,
        )

    def info(self):
        print(str(self))


class OI_STATION:
    """ This class corresponds to a single row (i.e. single
    station/telescope) of an OI_ARRAY table."""

    def __init__(
        self, tel_name=None, sta_name=None, diameter=None, staxyz=[None, None, None]
    ):
        self.tel_name = tel_name
        self.sta_name = sta_name
        self.diameter = diameter
        self.staxyz = staxyz

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        return not (
            (self.tel_name != other.tel_name)
            or (self.sta_name != other.sta_name)
            or (self.diameter != other.diameter)
            or (not _array_eq(self.staxyz, other.staxyz))
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s/%s (%g m)" % (self.sta_name, self.tel_name, self.diameter)


class OI_ARRAY:
    """Contains all the data for a single OI_ARRAY table.  Note the
    hidden convenience attributes latitude, longitude, and altitude."""

    def __init__(self, frame, arrxyz, stations=()):
        self.frame = frame
        self.arrxyz = arrxyz
        self.station = np.empty(0)
        for station in stations:
            tel_name, sta_name, sta_index, diameter, staxyz = station
            self.station = np.append(
                self.station,
                OI_STATION(
                    tel_name=tel_name,
                    sta_name=sta_name,
                    diameter=diameter,
                    staxyz=staxyz,
                ),
            )

    def __eq__(self, other):

        if type(self) != type(other):
            return False

        equal = not (
            (self.frame != other.frame) or (not _array_eq(self.arrxyz, other.arrxyz))
        )

        if not equal:
            return False

        # If position appears to be the same, check that the stations
        # (and ordering) are also the same
        if (self.station != other.station).any():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattr__(self, attrname):
        if attrname == "latitude":
            radius = np.sqrt((self.arrxyz ** 2).sum())
            return _angpoint(np.arcsin(self.arrxyz[2] / radius) * 180.0 / np.pi)
        elif attrname == "longitude":
            radius = np.sqrt((self.arrxyz ** 2).sum())
            xylen = np.sqrt(self.arrxyz[0] ** 2 + self.arrxyz[1] ** 2)
            return _angpoint(np.arcsin(self.arrxyz[1] / xylen) * 180.0 / np.pi)
        elif attrname == "altitude":
            radius = np.sqrt((self.arrxyz ** 2).sum())
            return radius - 6378100.0
        else:
            raise AttributeError(attrname)

    def __repr__(self):
        return "%s %s %g m, %d station%s" % (
            self.latitude.asdms(),
            self.longitude.asdms(),
            self.altitude,
            len(self.station),
            _plurals(len(self.station)),
        )

    def info(self, verbose=0):
        """
        Print the array's center coordinates.
        If verbosity >= 1,
        print information about each station.
        """
        print(str(self))
        if verbose >= 1:
            for station in self.station:
                print("   %s" % str(station))

    def get_station_by_name(self, name):

        for station in self.station:
            if station.sta_name == name:
                return station

        raise LookupError("No such station %s" % name)
