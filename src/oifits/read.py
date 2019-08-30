import astropy.io.fits as fits

class Parser:
    """
    Class for operations on OIFITS data.
    """

    def __init__(self, filename):
        self.hdulist = fits.open(filename)
        self.data =

    @property
    def info(self):
        return self.hdulist.info()

    @classmethod
    def read(cls, filename):
        return cls(filename=filename)

    def _process(self):
        for hdu in self.hdulist:
            header = hdu.header
            data = hdu.data
            if hdu.name == 'OI_WAVELENGTH':
                if newobj.wavelength == None: newobj.wavelength = {}
                insname = header['INSNAME']
                newobj.wavelength[insname] = OI_WAVELENGTH(data.field('EFF_WAVE'), data.field('EFF_BAND'))