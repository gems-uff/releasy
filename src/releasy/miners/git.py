from datetime import datetime, timedelta, timezone

import pygit2

from releasy.models.contributor import Contributor
from releasy.models.project import ProjectGraph
from releasy.models.release import Release
from releasy.miners.miner import Configuration, MinerPlugin


class GitMiner(MinerPlugin):
    def __init__(self, path: str, mine_commits: bool = True):
        self.path = path
        self.git = pygit2.Repository(self.path) 
        self.mine_commits = mine_commits

    def mine(self, project: ProjectGraph, config: Configuration):
        self.fetch_tags(project, config)
        self.fetch_commits(project, config)
        return project

    def fetch_tags(self, project: ProjectGraph, config: Configuration) -> None:
        tag_refs = [
            ref 
            for ref in self.git.references.objects 
            if ref.name.startswith('refs/tags/')
        ]
        version_parser = config.parser

        for tag_ref in tag_refs:
            tag = self.git.get(tag_ref.target)
            release_name = tag_ref.shorthand

            version = version_parser.parse(release_name)
            if not version:
                continue

            # Simple Tag
            if tag.type == pygit2.GIT_OBJECT_COMMIT:
                head = self.git.get(tag.id) #TODO Convert to commit
                author = None
                tagger_tzinfo = timezone(timedelta(minutes=tag.committer.offset))
                tagger_time = datetime.fromtimestamp(float(tag.committer.time), tagger_tzinfo)
                tagger = Contributor(tag.committer.name, tag.committer.email)
                release = Release(
                    version=version,
                    timestamp=tagger_time,
                    head=head,
                    author=tagger
                )
                project.releases.add(release)

            # Annotatted Tag
            elif tag.type == pygit2.GIT_OBJECT_TAG:
                peel = tag_ref.peel()
                # A tag may point to other objects in the repository
                # but we are only looking for tags that reference a commit
                if peel.type == pygit2.GIT_OBJECT_COMMIT:
                    head = self.git.get(peel.id)
                    try:
                        message = tag.message
                    except:
                        message = ''

                    if tag.tagger:
                        tagger = Contributor(tag.tagger.name, tag.tagger.email)
                        tagger_time_tzinfo = timezone(timedelta(minutes=tag.tagger.offset))
                        tagger_time = datetime.fromtimestamp(float(tag.tagger.time), tagger_time_tzinfo)
                    else:
                        tagger = Contributor(tag.committer.name, tag.committer.email)
                        tagger_time_tzinfo = timezone(timedelta(minutes=tag.committer.offset))
                        tagger_time = datetime.fromtimestamp(float(tag.committer.time), tagger_time_tzinfo)

                    release = Release(
                        version=version,
                        timestamp=tagger_time,
                        head=head,
                        author=tagger
                    )
                    project.releases.add(release)

    def fetch_commits(self, project: ProjectGraph, config: Configuration) -> None:
        pass
