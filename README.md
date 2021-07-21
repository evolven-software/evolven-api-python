# Evolven API Python
Evolven API Python is a client library for Evolven's server APIs. It provides an abstraction on top of raw Evolven API calls to interact with Evolven Server.  To get started, check out the examples or read the documentation:

- Evolven API Python documentation: [Show examples](https://github.com/evolven-software/evolven-api-python#usage)
- HTTP API documentation: [https://customers.evolven.com](https://customers.evolven.com)
- Evolven Software: [https://www.evolven.com](https://www.evolven.com) 

## Installation

To install from pip:
```
pip install evolven
```

To install from source:
```
python setup.py install
```


## Evolven API

The library provides a Python wrapper around the Evolven API and the Evolven data model. The library utilizes models to represent API calls to various objects:

- `api.Host`
- `api.Environment`
- `api.CI`
- `api.Change`
- `api.Agent`

The results are returned either as python `objects`, `json`, `string` or Pandas `DataFrame`. Fields for particular model match specified fields in Evolven API documentation.


The API is exposed via the ```api.EvolvenAPI``` class. To create an instance of the ```api.EvolvenAPI``` with login credentials:

```python
import evolven

api = evolven.EvolvenAPI("my-server.evolven.com", port=443, username="...", password="...")
api.Host.search("US3ALSQL004")

print(d.Next.Environment[0].name)
>>> US3ALSQL004

print(d.Next.Environment[0].env_id)
>>> 128439
```



## Usage

Below are examples of common tasks.

#### Authenticate with session id
API authentication can be achieved using `SecurityKey` parameter as follows:
```python
import evolven

api = evolven.EvolvenAPI("my-server.evolven.com", port=443, session="1870b4b....")
```

#### Define return type
You can define object return type on class initialization as follows:
```python
api = evolven.EvolvenAPI("my-server.evolven.com", port=443, session="1870b4b....", return_type="DataFrame")
```
All options are:

- `"DataFrame"` - returns data in normalized form as Pandas DataFrame object
- `"object"` - returns data as python object, fields are accesible as class properties
- `"JSON"` - returns data in JSON format
- `"string"` - returns string representation as returned by HTTP API



#### List all hosts

```python
hosts = api.Host.list()
hosts
```

Output:
```
| Host        | HostType | EnvId | Os                     | ... |
|-------------|----------|-------|------------------------|-----|
| NYUATOLD002 | Prod     | 847   | Windows 7              | ... |
| US3ALENG005 | Prod     | 512   | Windows Server 2008 R2 | ... |
| ...         | ...      | ...   | ...                    | ... |
```


#### Query Evolven Search

```python
hosts = api.Search.search("Host where cpu-count > 8 | Hotfixes")
hosts
```

Output:
```
| CIName    | Host         | EnvId | Os                     | ... |
|-----------|--------------|-------|------------------------|-----|
| KB4580325 | NYUATOLD002  | 847   | Windows 7              | ... |
| KB4580325 | US3ALENG005  | 512   | Windows Server 2008 R2 | ... |
| ...       | ...          | ...   | ...                    | ... |
```

#### Additional examples

Additional examples are shown in [Jupter notebooks here](https://github.com/evolven-software/evolven-api-python/tree/master/examples).


