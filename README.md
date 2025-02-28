Welcome to IPFSPy by Algovera
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## What is IPFSPy?

IPFSPy is a python library by Algovera to interact with IPFS and IPFS
ecosystem such as the common pinning services. It is designed by data
scientists for data scientists to interact with the IPFS ecosystem
without leaving the comfort of python and jupyter notebook.

You can learn more about IPFS [here](https://ipfs.io/#why).

IPFS is built using the go-lang or javascript. With IPFSPy, you can
interact with IPFS using the exposed [HTTP RPC
API](https://docs.ipfs.io/reference/http/api/#getting-started).

Ipfspy has two different implementations to interact with IPFS

1.  Access to most of what HTTP RPC API through `ipfspy.ipfshttpapi`

    With `ipfspy.ipfshttpapi`, you can either use local, infura or
    public nodes. In order to use local node, you will need a IPFS
    deamon running in the form of IPFS Desktop, IPFS Campanion or
    IPFS CLI. As an alternative, you can connect via the
    [Infura](https://infura.io/product/ipfs)’s dedicated IPFS gateway.

2.  [fsspec](https://filesystem-spec.readthedocs.io/en/latest/)-like
    implementation through `ipfspy.ipfspec`

    What is ipfsspec?

    ipfsspec is the fsspec-like implementation for IPFS. Through
    `ipfspy.ipfsspec`, you get access to both `local` and `infura` nodes
    but the `public` node is read-only. `Local` node offers both read
    and write. In order to use `local` node, you will need a local node
    running locally through IPFS Desktop or IPFS Companion or the IPFS
    CLI.

    Advantages of fsspec-like implementations

    -   many data science libraries like `dask`, `pandas` and `xarray`
        uses fsspec for path and file handling
    -   provides an uniform APIs

    Since many data science use fsspec, by implementing ipfsspec, fsspec
    supports IPFS.

## Installing

You can install the library simply through

`pip install ipfspy`

If you plan to contribute to this library, 1. clone the repo locally
`git clone https://github.com/algoveraai/ipfspy`

2.  Install an editable version of the repo `pip install -e .[dev]`

3.  submit PR

## How to use

### ipfshttpapi

Extend the IPFSApi

``` python
api = IPFSApi()
```

    Changed to local node

Change to other nodes like below. You can choose one of `local` `infura`
or `public`

``` python
api.change_gateway_type = 'infura'
```

    Changed to infura node

``` python
api.change_gateway_type = 'local'
```

    Changed to local node

To add a file to IPFS,

``` python
res, obj = api.add_items('output/test.txt'); obj
```

    [{'Name': 'test.txt', 'Bytes': 20},
     {'Name': 'test.txt',
      'Hash': 'QmbwFKzLj9m2qwBFYTVrBotf4QujvzTb1GBV9wFcNPMctm',
      'Size': '28'}]

To retrieve a file from IPFS

``` python
response, content = api.cat_items(cid='QmbwFKzLj9m2qwBFYTVrBotf4QujvzTb1GBV9wFcNPMctm'); content
```

    "\n'''\nFirst file\n'''\n"

### ipfsspec

``` python
import fsspec, io, os, asyncio
from ipfspy.ipfsspec.asyn import AsyncIPFSFileSystem
from fsspec import register_implementation
```

Register the ipfsspec to fsspec

``` python
register_implementation(AsyncIPFSFileSystem.protocol, AsyncIPFSFileSystem)
class fs:
    ipfs = fsspec.filesystem("ipfs")
    file = fsspec.filesystem("file")
```

    Changed to local node

Like `ipfspy.ipfshttpapi`, you can change the node as such

``` python
fs.ipfs.change_gateway_type = 'public'
```

    Changed to public node

``` python
fs.ipfs.change_gateway_type = 'local'
```

    Changed to local node

Add a file to IPFS using fsspec-like api

``` python
put_file_res = fs.ipfs.put(path='output/test.txt', rpath='/test_put_file'); put_file_res
```

    'QmbwFKzLj9m2qwBFYTVrBotf4QujvzTb1GBV9wFcNPMctm'

Retrieve a file from IPFs using fsspec-like api

``` python
fs.ipfs.cat('QmbwFKzLj9m2qwBFYTVrBotf4QujvzTb1GBV9wFcNPMctm')
```

    b"\n'''\nFirst file\n'''\n"
