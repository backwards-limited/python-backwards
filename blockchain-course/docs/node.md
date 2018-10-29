# Node

## Setup

We'll follow the easy way.
However, as mentioned before, an environment can be setup with [Anaconda](https://anaconda.org/anaconda/anaconda-navigator) or other alternatives.

Nodes will work (together) by exposing their services via [Flask](http://flask.pocoo.org/).

```bash
pip install flask
```

though in may case I just upgraded:

```bash
pip install --upgrade pip
```

and added an optional/missing dependency, just to keep Pip happy:

```bash
pip install PyHamcrest
```

And some more Flask installation, though again you may already have this:

```bash
pip install Flask-Cors
```

## Run Node

Within **src** of this module:

```bash
$ python node.py
 * Serving Flask app "node" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

and check the **node's** health:

```bash
$ curl http://localhost:5000/healthz
Good to go!
```

## API

Call the API via:

- Browser (limited usage)
- HTTP Client such as [Insomnia](https://insomnia.rest/)
- HTTP command line client such as OS built in **curl**, or better [httpie](https://httpie.org) which we'll see examples below

### Chain

View current chain (note responses use "..." for brevity):

```bash
$ http localhost:5000/chain
HTTP/1.0 200 OK
...
[
  {
    "index": 0,
    "previous_hash": "",
    "proof": 100,
    "timestamp": 0,
    "transactions": []
  },
...
```

### Wallet

Create new wallet including new keys:

```bash
$ http POST localhost:5000/wallet
HTTP/1.0 201 CREATED
...
{
  "data": {
    "private-key": ...
    "public-key": ...
...
```

Get wallet's keys:

```bash
$ http localhost:5000/wallet
HTTP/1.0 200 OK
...
{
  "data": {
    "private-key": ...
    "public-key": ...
...
```

Wallet funds:

```bash
$ http localhost:5000/balance
HTTP/1.0 200 OK
...
{
  "data": {
    "funds": 0,
    "message": "Fetched balance successfully"
...
```

### Transaction

Add/Create a transaction:

```bash
$ http POST localhost:5000/transaction recipient=blah amount:=4.5
HTTP/1.0 201 CREATED
...
{
  "data": {
    "funds": 51.5,
    "message": "Transaction added successfully",
    "transaction": {
      "amount": 4.5,
      "recipient": "blah"
...
```

### Mine

Mine a new block:

```bash
$ http POST localhost:5000/mine
HTTP/1.0 201 CREATED
...
{
  "data": {
    "block": {
      "index": 10,
      "previous_hash":
...
```