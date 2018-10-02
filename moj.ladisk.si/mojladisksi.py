import numpy as np
import os
import json
from sys import getsizeof
import requests

DOVOLJENI_TIPI = ['str', 'int', 'ndarray', 'float', 'tuple', 'list']
MAX_LEN = 15
MAX_SIZE = 10e3 #bit

def pripravi_resitev(odgovor):
    """ Funkcija pripravi rešitev za posredovanje na strežnik.

    Rezultat je: tip                (vsi)
                 vrednost           (NE ndarray)
                 povprečna vrednost (ndarray)
                 shape              (ndarray)
                 flat               (ndarray)
                 flat_size          (ndarray)
    """
    dovoljeni_tipi = ', '.join(DOVOLJENI_TIPI)
    out = dict()

    tip = type(odgovor).__name__

    if tip in ['int', 'int32']:
        out['tip'] = 'int'
        out['vrednost'] = int(odgovor)
        return out
    
    elif tip in ['float', 'Float', 'Zero', 'float64']:
        out['tip'] = 'float'
        out['vrednost'] = float(odgovor)
        return out
    
    elif tip in ['str', 'list', 'tuple']:
        bit_size = getsizeof(odgovor)
        if bit_size < MAX_SIZE:
            out['tip'] = tip
            out['vrednost'] = odgovor
            return out
        else:
            raise Exception(f'Napaka: Oddan odgovor, z velikostjo {bit_size/1e3:5.2f} kb, presega največjo dovoljeno velikost {MAX_SIZE/1e3:5.2f} kb.')
    
    elif tip in ['ndarray']:
        val = np.asarray(odgovor)

        out['tip'] = tip
        out['dtype'] = str(val.dtype)
        out['povprecna_vrednost'] = np.mean(val)
        out['shape'] = val.shape

        flat = val.flatten()
        vsak = 1
        if len(flat) > MAX_LEN:
            vsak = len(flat) // MAX_LEN + 1
            flat = flat[::vsak]
        
        out['flat'] = flat.tolist()
        out['flat_size'] = len(flat)
        return out
    
    else:
        raise Exception('Napaka: rezultat tipa \'{0:s}\' ne ustreza pričakovanim tipom: {1:s}!'.format(tip, dovoljeni_tipi))


def data_to_json(object):
    """
    Pripravi posredovan objekt za JSON serilizacijo. V `pripravi_resitev`?
    """
    if isinstance(object, np.ndarray):
        return {'type': str(np.ndarray), 'dtype': str(object.dtype), 'tolist': object.tolist()}

    if isinstance(object, complex):
        return (object.real, object.imag)

    raise TypeError(f'Object of type {type(object)} not serializable')


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
