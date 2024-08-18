import pytest
from releasy.model import ReleaseFormat, ReleaseType, ReleaseVersion, SemanticVersioningFormat


class DescribeReleaseVersion:
    def it_has_name(self, version: ReleaseVersion):
        assert version.name == "1.0.0"

    def it_has_version_str(self, version: ReleaseVersion):
        assert version.str == ["1", "0", "0"]

    def it_has_version_number(self, version: ReleaseVersion):
        assert version.number == [1,0,0] 

    def it_has_type(self, version: ReleaseVersion):
        assert version.type == ReleaseType.MAJOR

    def it_has_format(self, version: ReleaseVersion):
        assert isinstance(version.format, SemanticVersioningFormat)

    def it_is_comparable(self, 
            version: ReleaseVersion, 
            version_a: ReleaseVersion, 
            version_b: ReleaseVersion, 
            version_c: ReleaseVersion):
        
        assert version == version_a
        assert version != version_b
        
        assert version_a < version_b
        assert version_a <= version_b
        assert version_b > version_a 
        assert version_b >= version_a 
        
        assert not (version < version_a)
        assert not (version > version_a)
    
    def it_is_sortable(self,
            version_a: ReleaseVersion, 
            version_b: ReleaseVersion, 
            version_c: ReleaseVersion):
        versions = [version_c, version_a, version_b]
        sorted_versions = sorted(versions)
        assert sorted_versions == [version_a, version_b, version_c] 

    def it_fetch_number(self, version_c: ReleaseVersion):
        assert version_c.number[0] == 1
        assert version_c.number[1] == 2
        assert version_c.number[2] == 3
    

class DescribeSemanticVersioningFormat:
    def it_has_version_number(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        assert version.number == [1, 0, 0]
        
    def it_parse_major_release(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.0")
        assert version.type == ReleaseType.MAJOR

    def it_parse_minor_release(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.1.0")
        assert version.type == ReleaseType.MINOR

    def it_parse_patch(self):
        releaseFormat = SemanticVersioningFormat()
        version = releaseFormat.parse("1.0.1")
        assert version.type == ReleaseType.PATCH


