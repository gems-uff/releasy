Releasy
=======

Releasy is a tool that collects provenance data from releases 
by parsing the software version control and issue tracking
systems.

Papers
======

[Curty, F., Kohwalter, T., Braganholo, V., Murta, L., 2018. An Infrastructure for Software Release Analysis through Provenance Graphs. Presented at the VI Workshop on Software Visualization, Evolution and Maintenance.](https://goo.gl/9u8rzc)

How to use
==========

Basic Usage
-----------

```
$ python -m releasy [release-name] <command> [options]
```

**E.g.:**

Show information about the release 1.0.0
```
$ python -m releasy project download https://api.github.com/repos/gems-uff/releasy/issues
$ python -m releasy 1.0.0 show
```

Installation
------------

```
pip install releasy-uff
```

Available Commands
------------------

Show project information
```
$ python -m releasy project overview
```

Download project issues
```
$ python -m releasy project download https://api.github.com/repos/gems-uff/releasy/issues
```

Show release information
```
$ python -m releasy 1.0.0 show
```

Export prov-n from a release
```
$ python -m releasy 1.0.0 prov
```

