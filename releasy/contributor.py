from typing import List, Set, Tuple
from releasy.repository import CommitSet

class ContributorSet():
    def __init__(self, 
            commits: CommitSet = None, 
            previous_contributors: Set[str] = None) -> None:
        self._commits = CommitSet()
        self.committers = set[str]()
        self.authors = set[str]()
        self.contributors = set[str]()
        self.newcomers = set[str]()
  
        if commits:
            self._commits = commits
            self.committers = set[str](commit.committer for commit in commits)
            self.authors = set[str](commit.author for commit in commits)
            self.contributors = self.committers | self.authors

            if previous_contributors:
                self.newcomers = self.contributors - previous_contributors

    def __len__(self):
        return len(self.contributors)

    def frequency(self):
        contributors_frequency = dict[str,int]()
        total_contributions = 0
        for author, committer in zip(
                [commit.author for commit in self._commits],
                [commit.committer for commit in self._commits]):

            contributors_frequency[author] \
                = contributors_frequency.get(author, 0) +1
            total_contributions += 1
            if author != committer:
                contributors_frequency[committer] \
                    = contributors_frequency.get(committer, 0) +1
                total_contributions += 1

        for contributor, contributions in contributors_frequency.items():
            contributors_frequency[contributor] \
                = int(contributors_frequency[contributor] \
                    * 100 \
                    / total_contributions)
        
        return contributors_frequency

    def top(self, top: int = None, percent: int = None) -> Tuple[str, int]:
        if top and percent:
            raise ValueError("must use top or percent argument")

        contributors = sorted(
            self.frequency().items(), 
            key=lambda t: (-t[1], t[0]))

        if top == None and percent == None:
            return contributors
        
        if top:
            return contributors[0:top]

        contributions = 0
        for pos, (contributor, frequency) in enumerate(contributors):
            contributions += frequency
            if contributions >= percent:
                return contributors[0:pos+1] 
            
        return []

    @property
    def all(self):
        return self.contributors
    
    def commits(self, contributors: List[str]) -> CommitSet:
        contributors = set(contributors)
        commits = [commit for commit in self._commits
            if commit.author in contributors 
                or commit.committer in contributors]
        commits = CommitSet(commits)
        return commits
