
from releasy.model import Release, ReleaseType, SemanticVersioningFormat

class describe_release:
    def it_has_name(self):
        release = Release()
        release.name = "1.0.0"
        assert release.name == "1.0.0"

        release = Release("1.1.0")
        assert release.name == "1.1.0"


    def it_has_version(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        release = Release(version=version)
        assert release.version.parts == [1,0,0] 
        assert release.version.type == ReleaseType.MAJOR 
        assert release.version.format.name == "Semantic Versioning"
    

    def it_has_type(self):
        release = Release()
        pass
        

class describe_release_version:
    def it_has_parts(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        release = Release(version=version)
        assert release.version.parts == [1,0,0] 

    def it_has_type(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        release = Release(version=version)
        assert release.version.type == ReleaseType.MAJOR

    def it_has_format(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        release = Release(version=version)
        assert release.version.format == releaseFormat


class describe_semantic_versioning_format:
    def it_has_version_number(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        release = Release(version=version)
        assert release.version.parts == [1, 0, 0]
        
    def it_parse_major_release(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        release = Release(version=version)
        assert release.version.type == ReleaseType.MAJOR

    def it_parse_minor_release(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.1.0")
        release = Release(version=version)
        assert release.version.type == ReleaseType.MINOR

    def it_parse_patch(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.1")
        release = Release(version=version)
        assert release.version.type == ReleaseType.PATCH

