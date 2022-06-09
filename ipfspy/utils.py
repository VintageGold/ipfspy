# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_utils.ipynb (unless otherwise specified).

__all__ = ['get_coreurl', 'cat_items', 'dag_get', 'parse_response', 'DownloadDir']

# Cell
import requests
import json
from fastcore.all import *
import pandas as pd
import dag_cbor

GATEWAYS_API_READ = [
    "http://127.0.0.1:8080/api/v0",
    "http://127.0.0.1:5001/api/v0",
    "https://ipfs.io/api/v0",
    "https://gateway.pinata.cloud/api/v0",
    "https://cloudflare-ipfs.com/api/v0",
    "https://dweb.link/api/v0",
    "https://ipfs.infura.io:5001/api/v0"
]
GATEWAYS_API_WRITE = [
    "http://127.0.0.1:8080/api/v0",
    "http://127.0.0.1:5001/api/v0",
    "https://ipfs.io/api/v0",
    "https://gateway.pinata.cloud/api/v0",
    "https://cloudflare-ipfs.com/api/v0",
    "https://dweb.link/api/v0",
]

# Cell
def get_coreurl(
    local:bool=True, # If local uses local node, else uses Infura.io gateway
    write:bool=True, # If write select a gateway with write functionality
    # change:bool=False # If change, try a different url than the last time
    # idx:int=0 # Index indicating last change
):
    'Set the core url for convenience'
    
    if write:
        if local:
            return GATEWAYS_API_WRITE[0]
        else:
            return GATEWAYS_API_WRITE[2]     
    else:
        if local:
            return GATEWAYS_API_READ[0]
        else:
            return GATEWAYS_API_READ[6]


def cat_items(
    coreurl:str,
    cid:str, # The path to the IPFS object(s) to be outputted
    **kwargs
):
    'Show IPFS object data'

    params = {}
    params['arg'] = cid
    params.update(kwargs)

    return requests.post(f'{coreurl}/cat', params=params)


def dag_get(
    coreurl:str,
    path:str,
    output_codec:str='dag-cbor',
):
    'Get a DAG node from IPFS.'

    params = {}
    params['arg'] = path
    params['output-codec'] = output_codec

    return requests.post(f'{coreurl}/dag/get', params=params)

# Cell
def parse_response(
    response, # Response object
):
    "Parse response object into JSON"

    if response.text.split('\n')[-1] == "":
        return [json.loads(each) for each in response.text.split('\n')[:-1]]

    else:
        return response.json()

# Cell
class DownloadDir:
    'Download a IPFS directory to your local disk'
    def __init__(self,
        coreurl:str,
        root_cid:str, # Root CID of the directory
        output_fol:str, # Path to save in your local disk
    ):

        self.url = coreurl
        self.root = root_cid
        self.output = output_fol
        self.full_structure = None

    def _file_or_dir(self,
        name
        ):
        return 'file' if len(name.split('.')) > 1 else 'dir'

    def _get_links(self,
        cid,
        fol
    ):
        root_struct = {}
        struct = {}

        links = dag_cbor.decode(dag_get(self.url, cid).content)['Links']

        for link in links:
            name = f'{fol}/{link["Name"]}'
            hash_ = str(link['Hash'])
            type_ = self._file_or_dir(name)

            if type_ == 'dir':
                details = self._get_links(hash_, name)

            else:
                details = {'Hash': hash_, 'type': type_}

            struct[name] = details

        root_struct[fol] = struct

        return root_struct


    def _save_links(self,
        links
    ):
        for k, v in links.items():
            if len(k.split('.')) < 2:
                if not os.path.exists(k): os.mkdir(k)
                self._save_links(v)

            else:
                data = cat_items(self.url, links[k]['Hash']).content

                with open(k, 'wb') as f:
                    f.write(data)

    def download(self
    ):
        self.full_structure = self._get_links(self.root, self.output)
        self._save_links(self.full_structure)
