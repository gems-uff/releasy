# Module responsible to parse code repositories and mine releases and related
# information
#

import os.path
import re

from .model import Project, Release


class Miner():
    """ Mine a single repository """

    def __init__(self, path, vcs=None):
        self.path = path
        name = os.path.basename(path)
        self._vcs = vcs
        self._project = Project(name)

    def mine_releases(self):
        releases = []
        for tag in self._vcs.tags():
            (is_release, release_type, prefix, major, minor, patch) = self._match_release(tag.name)
            if is_release:
                release = Release(tag.name,
                                  prefix=prefix,
                                  major=major,
                                  minor=minor,
                                  patch=patch)

                releases.append(release)
        releases = sorted(releases, key=lambda release: release.name)
        self._project._releases = releases
        return self._project

    def _match_release(self, tagname):
        pattern = re.compile(r'^(?P<prefix>(?:.*?[^0-9\.]))?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)$')
        re_match = pattern.search(tagname)
        if re_match:
            prefix = re_match.group('prefix')
            major = re_match.group('major')
            minor = re_match.group('minor')
            patch = re_match.group('patch')

            if patch and patch != '0':
                release_type = 'PATCH'
            elif minor and minor != '0':
                release_type = 'MINOR'
            elif major:
                release_type = 'MAJOR'
            else:
                release_type = 'UNKNOWN'
            return True, release_type, prefix, major, minor, patch
        else:        
            return False


class Vcs:
    """
    Version Control Repository

    Attributes:
        __commit_dict: internal dictionary of commits
    """

    def __init__(self):
        self._commit_cache = {}
        self._tag_cache = {}
        self.developer_db = None

    def tags(self):
        """ Return repository tags """
        pass

    def load_tag(self):
        """ load tag from version control """
        pass

    def load_commit(self):
        """ load commit from version control """
        pass
