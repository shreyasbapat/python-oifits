import numpy as np

class OI_WAVELENGTH:
    def __init__(self, eff_wave, eff_band=None):
        self.eff_wave = np.array(eff_wave, dtype=double).reshape(-1)
        if eff_band == None:
            eff_band = np.zeros_like(eff_wave)
        self.eff_band = np.array(eff_band, dtype=double).reshape(-1)

    def __eq__(self, other):

        if type(self) != type(other): return False

        return not (
                (not _array_eq(self.eff_wave, other.eff_wave)) or
                (not _array_eq(self.eff_band, other.eff_band)))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%d wavelength%s (%.3g-%.3g um)" % (
        len(self.eff_wave), _plurals(len(self.eff_wave)), 1e6 * np.min(self.eff_wave), 1e6 * np.max(self.eff_wave))

    def info(self):
        print(str(self))
