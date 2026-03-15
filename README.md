Releasy
=======

[![Build Status](https://github.com/gems-uff/releasy/actions/workflows/pytest.yml/badge.svg)](https://github.com/gems-uff/releasy/actions/workflows/pytest.yml)

Releasy is a tool that collects provenance data from releases 
by parsing the software version control and issue tracking
systems.

Papers
======

[Curty, F., Kohwalter, T., Braganholo, V., Murta, L., 2018. An Infrastructure for Software Release Analysis through Provenance Graphs. Presented at the VI Workshop on Software Visualization, Evolution and Maintenance.](https://goo.gl/9u8rzc)

Overview
========

```text
Git ----> Releases + Commits ----> Data
      |                        |
    Miner                  Inspector
```

1. The miner creates release and commit collections based on Git
2. The inspector reads these collections to extract data


