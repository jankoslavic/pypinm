import numpy as np
import requests

DOVOLJENI_TIPI = ['str', 'int', 'ndarray', 'float', 'tuple', 'list']
MAX_LEN = 15


def pripravi_resitev(odgovor):
    """ Funkcija pripravi rešitev za posredovanje na strežnik.

    Rezultat je: tip;
                 povprečna vrednost;
                 shape;
                 korak podatkov (1, če so podani vsi)
                 dolžina morebiti krajšanih flat podatkov;
                 flat podatki
    """
    # preverjanje tipa
    dovoljeni_tipi = ', '.join(DOVOLJENI_TIPI)
    out = []
    tip = type(odgovor).__name__
    if tip in ['Float', 'Zero', 'float64']:
        tip = 'float'
        odgovor = float(odgovor)
    if tip in ['int32']:
        tip = 'int'
        odgovor = int(odgovor)
    if tip in ['tuple', 'list']:
        if all(isinstance(x, (int, float)) for x in odgovor):
            odgovor = np.array(odgovor, dtype='float')
            tip = 'float'
    if tip not in DOVOLJENI_TIPI:
        raise Exception('Napaka: rezultat tipa {0:s} ne ustreza pričakovanim tipom: {1:s}!'.format(tip, dovoljeni_tipi))
    out.append(tip)

    if tip in ['str']:
        if ';' in odgovor or '\t' in odgovor or '\n' in odgovor:
            raise Exception('Napaka: odgovor ne sme vsebovati podpičja (;)\
             ali tabulatorja ali prehoda v novo vrstico!\n Glej odgovor:{:s}'.format(odgovor))
        out.append(' ')
        out.append(' ')
        out.append(' ')
        out.append(' ')
        out.append(odgovor[:200])
    elif tip in ['tuple', 'list']:
        odgovor = '|'.join([str(e) for e in odgovor])
        if ';' in odgovor:
            raise Exception('Napaka: odgovor ne sme vsebovati podpičja (;)\
             ali tabulatorja ali prehoda v novo vrstico!\n Glej odgovor:{:s}'.format(odgovor))
        out.append(' ')
        out.append(' ')
        out.append(' ')
        out.append(' ')
        out.append(odgovor[:200])
    else:
        val = np.asarray(odgovor)
        out.append(np.array2string(np.mean(val)))
        out.append(str(val.shape))

        flat = val.flatten()
        vsak = 1
        if len(flat) > MAX_LEN:
            vsak = len(flat) // MAX_LEN + 1
            flat = flat[::vsak]
        out.append(str(vsak))
        out.append(str(len(flat)))
        out.append(np.array2string(flat, max_line_width=1e6, separator=',')[1:-1])

    return ';'.join(out)


def poslji(odgovor, id, st):
    """ Funkcija pošlje rešitev na strežnik.

    :param odgovor: spremenljivka nosilka odgovora
    :param id: identifikacijska številka naloge
    :param st: zaporedna številka odgovora
    """
    url = 'https://ladiskhomework-hrd.appspot.com/'
    r = requests.post(url + 'StudentData',
                      {'what': 'resitev',
                       'sa_id': id,
                       'odgovor': pripravi_resitev(odgovor),
                       'st': st})
    print(r.json()['status'])
