
from releasy.model import Release, ReleaseType, SemanticVersioningFormat

class DescribeRelease:
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
        assert release.version.number == [1,0,0] 
        assert release.version.type == ReleaseType.MAJOR 
        assert release.version.format.name == "Semantic Versioning"

    def it_has_type(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        release = Release(version=version)
        assert release.type == ReleaseType.MAJOR
        

class DescribeReleaseVersion:
    def it_has_name(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        assert version.name == "1.0.0"

    def it_has_version_str(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        assert version.str == ["1", "0", "0"]

    def it_has_version_number(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        assert version.number == [1,0,0] 

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

    def it_is_comparable(self):
        releaseFormat = SemanticVersioningFormat()
        release_a = Release(version=releaseFormat.parse("1.0.0"))
        release_a2 = Release(version=releaseFormat.parse("1.0.0"))
        release_b = Release(version=releaseFormat.parse("1.0.1"))
        
        assert release_a.version == release_a2.version 
        assert release_a.version != release_b.version 
        
        assert release_a.version < release_b.version 
        assert release_a.version <= release_b.version 
        assert release_b.version > release_a.version 
        assert release_b.version >= release_a.version 
        
        assert not (release_a.version < release_a2.version)
        assert not (release_a.version > release_a2.version)
    
    def it_is_sortable(self):
        releaseFormat = SemanticVersioningFormat()
        version_a = releaseFormat.parse("1.0.0")
        version_b = releaseFormat.parse("1.0.1")
        version_c = releaseFormat.parse("1.1.0")
        versions = [version_c, version_a, version_b]
        sorted_versions = sorted(versions)
        assert sorted_versions == [version_a, version_b, version_c] 

    def it_fetch_number(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.2.3")
        assert version.number[0] == 1
        assert version.number[1] == 2
        assert version.number[2] == 3
    

class DescribeSemanticVersioningFormat:
    def it_has_version_number(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        release = Release(version=version)
        assert release.version.number == [1, 0, 0]
        
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


