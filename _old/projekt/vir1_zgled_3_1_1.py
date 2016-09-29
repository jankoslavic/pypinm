__author__ = 'Luka Knez'

""" Modul izračuna rešitve za zgled 3.1.1 iz vira1
"""

# Uvoz potrebnih modulov
import numpy as np


def resi(podatki={'m': 1, 'l': 1, 'k': 10000, 'k_varphi': 10000, 'varphi_0': 0.01, 't_1': 50 / 1000}):
    """
    Preračuna vse točke pri zgledu 3.1.1 (vir 1)

    :param podatki: Slovar potrebnih spremenljivk.
                    Potrebujemo: m [kg], l [m], k [N/m], k_varphi [Nm/rad], varphi_0 [rad] in t_1 [s].
    :return:        Vrne rešitve zgleda 3.1.1

    Vir 1: Janko Slavič - Dinamika, mehanska nihanja in mehanika tekočin (2014)
    """

    m = podatki['m']
    l = podatki['l']
    k = podatki['k']
    k_varphi = podatki['k_varphi']
    varphi_0 = podatki['varphi_0']
    t_1 = podatki['t_1']

    lastna = np.sqrt(9 * k / (2 * m) + (3 * k_varphi) / (m * l**2))

    odziv = varphi_0 * np.cos(lastna * t_1)

    return dict([('w_0', lastna), ('odziv', odziv)])


if __name__ == '__main__':
    resitve = resi()

    lastna = resitve['w_0']
    odziv = resitve['odziv']

    print('Lastna krožna frekvenca znaša: {:g} rad/s.'.format(lastna))
    print('Zasuk pri času t1 znaša: {:g} rad.'.format(odziv))