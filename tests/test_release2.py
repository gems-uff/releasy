import pytest

from releasy.release2 import (
    MainRelease,
    MajorRelease,
    MinorRelease,
    Patch,
    SemanticVersioningSchema,
    SimpleVersioningSchema
)


class TestSimpleVersioningSchema:
    def it_build_releases(self):
        release = SimpleVersioningSchema().apply("1.2.3")

        assert release.name == "1.2.3"
        assert isinstance(release, MainRelease)


    def it_match_prefix(self):
        release = SimpleVersioningSchema().apply("prefix1.2.3")

        assert release.name == "prefix1.2.3"
        assert release.version.prefix == "prefix"
        assert isinstance(release, MainRelease)


    def it_match_suffix(self):
        release = SimpleVersioningSchema().apply("1.2.3suffix")

        assert release.name == "1.2.3suffix"
        assert release.version.suffix == "suffix"
        assert isinstance(release, MainRelease)
        

    def it_skip_invalid_references(self):
        release = SimpleVersioningSchema().apply("invalid")
        
        assert not release


class TestSemanticVersioningSchema:
    def it_build_major_releases(self):
        release = SemanticVersioningSchema().apply("1.0.0")
        
        assert release.name == "1.0.0"
        assert release.version.major == 1
        assert release.version.minor == 0
        assert release.version.patch == 0
        assert isinstance(release, MajorRelease)


    def it_build_minor_releases(self):
        release = SemanticVersioningSchema().apply("1.1.0")
        
        assert release.name == "1.1.0"
        assert release.version.major == 1
        assert release.version.minor == 1
        assert release.version.patch == 0
        assert isinstance(release, MinorRelease)
                          

    def it_build_patches(self):
        release = SemanticVersioningSchema().apply("1.1.1")
        
        assert release.name == "1.1.1"
        assert release.version.major == 1
        assert release.version.minor == 1
        assert release.version.patch == 1
        assert isinstance(release, Patch)
