""" Orodja za delo z matrikami
"""
__author__ = 'Janko Slavic'

import numpy as np


def zamenjaj_stolpca(matrika, iz, na):
    """ Zamenjaj stolpca

    :param matrika:
    :param iz:
    :param na:
    :return: matrika z zamenanimi vrednostmi
    """
    matrika[:, [iz, na]] = matrika[:, [na, iz]]  # tukaj uporabimo napredno rezanje!
    return matrika


def zamenjaj_vrstici(matrika, iz, na):
    """ Zamenjaj vrstici

    :param matrika:
    :param iz:
    :param na:
    :return: matrika z zamenanimi vrednostmi
    """
    # TODO preveri ali to res dela pravilno
    matrika[[na, iz], :] = matrika[[iz, na], :]
    return matrika


def gaussova_eliminacija(A, b, prikazi_korake=False):
    """ Vrne Gaussovo eliminacijo razširjene matrike koeficientov

    :param A: matrika koeficientov
    :param b: vektor konstant
    :param prikazi_korake: ali izpišem posamezne korake
    :return Ab: razširjena matrika koeficientov
    """
    Ab = np.column_stack((A, b))
    for p, pivot_vrsta in enumerate(Ab[:-1]):
        for vrsta in Ab[p + 1:]:
            if pivot_vrsta[p]:
                vrsta[p:] = vrsta[p:] - pivot_vrsta[p:] * vrsta[p] / pivot_vrsta[p]
            else:
                raise Exception('Deljenje z 0.')
        if prikazi_korake:
            print('Korak: {:g}'.format(p))
            print(Ab)
    return Ab


def gaussova_eliminacija_pivotiranje(A, b, prikazi_korake=False):
    """ Vrne Gaussovo eliminacijo razširjene matrike koeficientov, uporabi delno pivotiranje

    :param A: matrika koeficientov
    :param b: vektor konstant
    :param prikazi_korake: ali izpišem posamezne korake
    :return Ab: razširjena matrika koeficientov
    """
    Ab = np.column_stack((A, b))
    for p in range(len(Ab) - 1):
        p_max = np.argmax(np.abs(Ab[p:, p])) + p
        if p != p_max:
            Ab[[p], :], Ab[[p_max], :] = Ab[[p_max], :], Ab[[p], :]
        pivot_vrsta = Ab[p, :]
        for vrsta in Ab[p + 1:]:
            if pivot_vrsta[p]:
                vrsta[p:] = vrsta[p:] - pivot_vrsta[p:] * vrsta[p] / pivot_vrsta[p]
            else:
                raise Exception('Deljenje z 0.')
        if prikazi_korake:
            print('Korak: {:g}'.format(p))
            print('Pivot vrsta:', pivot_vrsta)
            print(Ab)
    return Ab


def gaussova_el_resitev(Ab):
    """ Glede na Gaussovo eliminacijo razširjene matrike Ab, vrne vektor rešitev x.

    :param Ab: razširjena matrika koeficientov
    :return x: vektor rešitev
    """
    v = len(Ab)
    x = np.zeros(v)
    for p, pivot_vrsta in enumerate(Ab[::-1]):
        x[v - p - 1] = (pivot_vrsta[-1] - pivot_vrsta[v - p:-1] @ x[v - p:]) / (pivot_vrsta[v - p - 1])
    return x


def LU_razcep(A):
    """ Vrne razcep A  kot ``[L\\U]`` """
    # eliminacija
    for p, pivot_vrsta in enumerate(A[:-1]):
        for i, vrsta in enumerate(A[p + 1:]):
            if pivot_vrsta[p]:
                m = vrsta[p] / pivot_vrsta[p]
                vrsta[p:] = vrsta[p:] - pivot_vrsta[p:] * m
                vrsta[p] = m
    return A


def LU_resitev(LU, b):
    """ Vrne vrednost x glede na ``[L\\U]x=b`` """
    y = np.zeros_like(b)
    x = np.zeros_like(b)
    for i, b_ in enumerate(b):
        y[i] = (b_ - np.dot(LU[i, :i], y[:i]))
    v = len(b)
    for i in range(v - 1, -1, -1):
        x[i] = (y[i] - LU[i, i + 1:] @ x[i + 1:]) / LU[i, i]
    return x


def LU_razcep_pivotiranje(A, prikazi_korake=False):
    """ Vrne razcep LU matriko in vektor zamenjanih vrstic pivotiranje, uporabi delno pivotiranje

    :param A:               matrika koeficientov
    :param prikazi_korake:  izpišem posamezne korake
    :return LU:             LU matrika
    :return pivotiranje:    vektor zamenjave vrstic (pomembno pri iskanju rešitve)
    """
    LU = A.copy()
    pivotiranje = np.arange(len(A))
    for p in range(len(LU) - 1):
        p_max = np.argmax(np.abs(LU[p:, p])) + p
        if p != p_max:
            LU[[p], :], LU[[p_max], :] = LU[[p_max], :], LU[[p], :]
            pivotiranje[p], pivotiranje[p_max] = pivotiranje[p_max], pivotiranje[p]
        pivot_vrsta = LU[p, :]
        for vrsta in LU[p + 1:]:
            if pivot_vrsta[p]:
                m = vrsta[p] / pivot_vrsta[p]
                vrsta[p:] = vrsta[p:] - pivot_vrsta[p:] * m
                vrsta[p] = m
            else:
                raise Exception('Deljenje z 0.')
        if prikazi_korake:
            print('Korak: {:g}'.format(p))
            print('Pivot vrsta:', pivot_vrsta)
            print(LU)
    return LU, pivotiranje


def LU_resitev_pivotiranje(LU, b, pivotiranje):
    """ Vrne vrednost x glede na ``[L\\U]x=b``.

        Uporabite v primeru delnega pivotiranja
    """
    y = np.zeros_like(b)
    x = np.zeros_like(b)
    for i, b_ in enumerate(b[pivotiranje]):
        y[i] = (b_ - LU[i, :i] @ y[:i])
    v = len(b)
    for i in range(v - 1, -1, -1):
        x[i] = (y[i] - LU[i, i + 1:] @ x[i + 1:]) / LU[i, i]
    return x


if __name__ == '__main__':
    import numpy as np

    a = np.arange(9).reshape((3, 3))
    b = zamenjaj_stolpca(a, 0, 1)
    print(b)
    c = zamenjaj_vrstici(a, 0, 1)  # ne smemo pozabiti: a samo kaže na spominsko mesto
    print(c)

