mongo-admin
===========

MongoDB Administration made simple. The tool is written in Python and has been tested in Python 2.7

##Installation

Running fab files require Fabric to be installed on Python:

```bash
$ pip install fabric
```

Clone this repo:

```bash
$ git clone https://github.com/mongoh/mongo-admin.git
```

##Deploying MongoDB to a remote server

```bash
$ cd mongoadmin/deploy
$ fab deploy -H <host>
```

E.g.
```bash
$ fab deploy -H rishi@mongoh.com
```