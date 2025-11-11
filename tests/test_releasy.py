
from releasy import mine
from releasy.session import ReleasySession
from releasy.configuration import Configuration
from releasy.models.release import ReleaseList

class DescribeReleasySession:
    def it_works_without_configuration(self):
        with mine(".") as session:
            assert isinstance(session, ReleasySession)
            assert hasattr(session, "releases")
            assert isinstance(session.releases, ReleaseList)
            assert hasattr(session, "config")
            assert isinstance(session.config, Configuration)

    def it_works_with_configuration(self):
        config = Configuration(branch="main", log_level="debug")
        with mine(".", config) as session:
            assert isinstance(session, ReleasySession)
            assert hasattr(session, "releases")
            assert isinstance(session.releases, ReleaseList)
            assert hasattr(session, "config")
            assert isinstance(session.config, Configuration)
            assert session.config.branch == "main"
            assert session.config.log_level == "debug"
