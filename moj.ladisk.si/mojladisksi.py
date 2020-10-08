import numpy as np
import os
import json
from sys import getsizeof
import requests

DOVOLJENI_TIPI = ['str', 'int', 'float', 'ndarray', 'tuple', 'list', 'dict']
MAX_LEN = 15
MAX_SIZE = 10e3 #bit

int_type_names = [_.__name__ for _ in np.sctypes['int'] + np.sctypes['uint']] + ['int']
float_type_names = [_.__name__ for _ in np.sctypes['float']] + ['float', 'Float', 'Zero']


def pripravi_resitev(odgovor):
    """ 
    Funkcija pripravi rešitev za posredovanje na strežnik.
    Poimenovanje ključev je pomembno pri preverjanju odgovorov - naj se ne spreminja!
    Rezultat je: tip                (vsi)
                 vrednost           (NE ndarray)
                 dtype              (ndarray)
                 mean               (ndarray)
                 shape              (ndarray)
                 flat               (ndarray)
                 flat_size          (ndarray)
    """
    dovoljeni_tipi = ', '.join(DOVOLJENI_TIPI)
    out = dict()

    tip = type(odgovor).__name__

    if tip in int_type_names:
        out['tip'] = 'int'
        out['vrednost'] = int(odgovor)
        return out
    
    elif tip in float_type_names:
        out['tip'] = 'float'
        out['vrednost'] = float(odgovor)
        return out
    
    elif tip in ['str', 'list', 'tuple', 'dict']:
        bit_size = getsizeof(odgovor)
        if bit_size < MAX_SIZE:
            out['tip'] = tip
            out['vrednost'] = odgovor
            return out
        elif tip in ['list', 'tuple'] and len(odgovor) > MAX_LEN:
            korak = len(odgovor) // MAX_LEN + 1
            out['tip'] = tip
            out['korak'] = korak
            out['vrednost'] = odgovor[::korak]
            return out
        else:
            raise Exception(f'Napaka: Oddan odgovor, z velikostjo {bit_size/1e3:5.2f} kb, presega največjo dovoljeno velikost {MAX_SIZE/1e3:5.2f} kb.')
    
    elif tip in ['ndarray']:
        out.update(prepare_ndarray(odgovor))
        return out
    
    else:
        raise Exception('Napaka: rezultat tipa \'{0:s}\' ne ustreza pričakovanim tipom: {1:s}!'.format(tip, dovoljeni_tipi))


def prepare_ndarray(array, MAX_LEN=15):
    """
    Pripravi numpy.ndarray za oddajo - flatten, skrajša na MAX_LEN , pretvori v seznam 
    in zapakira v dict (tip:'ndarray', dtype, mean, shape, flat, flat_size).
    Poimenovanje ključev je pomembno pri preverjanju odgovorov - naj se ne spreminja!
    """
    flat = array.flatten()
    inc = 1
    if len(flat) > MAX_LEN:
        inc = len(flat) // MAX_LEN + 1
        flat = flat[::inc]
    flat_list = flat.tolist()
    return {
        'tip': 'ndarray',
        'dtype': array.dtype.name,
        'mean': np.mean(array),
        'shape': array.shape,
        'flat': flat_list,
        'flat_size': len(flat_list),
        'korak': inc
    }


def data_to_json(object):
    """
    Pripravi posredovan objekt za JSON serilizacijo. Uporabljen v primeur, ko
    pride do napake pri pretvorbi objekta v JSON.
    """
    if isinstance(object, np.ndarray):
        return prepare_ndarray(object)

    if isinstance(object, complex):
        return (object.real, object.imag)

    if type(object) in np.sctypes['int'] + np.sctypes['uint']:
        return int(object)
    
    if type(object) in np.sctypes['float']:
        return float(object)

    raise TypeError(f'Napaka pri pretvorbi podatka tipa {type(object)} v JSON. Preverite posredovan odgovor!')


def poslji(odgovor, id, st):
    """ Funkcija pošlje rešitev na strežnik.
    :param odgovor: spremenljivka nosilka odgovora
    :param id: identifikacijska številka naloge
    :param st: zaporedna številka odgovora
    """
    url = 'https://moj.ladisk.si/'
    client = requests.session()
    r = client.get(url + 'get_token')
    csrftoken = client.cookies['csrftoken']
    cookies = dict(client.cookies)
    headers = {'Content-type':'application/json', "X-CSRFToken":csrftoken, 'Referer':url}
    
    data = {
        'sa_id': id,
        'odgovor': pripravi_resitev(odgovor),
        'st': st,
       }

    json_data = json.dumps(data, default=data_to_json)

    r = requests.post(url + 'StudentData',
                        json=json_data, #json_data, če rabiš default data_to_json funkcijo
                        headers=headers,
                        cookies=cookies)

    return r.json()['status']