*Disclaimer: The following README is under construction and show desire outputs, some not yet implemented*

Releasy
=======

Releasy is a tool that collects provenance data from releases 
by parsing the software version control and issue tracking
systems.

Usage
-----

```
$ releasy [release-name] [option]
```

### E.g.:

Show information about the actual release
``` 
$ releasy
```

Show information about the release 1.0.0
``` 
$ releasy 1.0.0
```

List the commits of the release 1.0.0
```
$ releasy 1.0.0 ls commit
```

List the issues of the release 1.0.0
```
$ releasy 1.0.0 ls issue
```
