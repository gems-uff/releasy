from releasy.release2 import MainRelease, MajorRelease, MinorRelease, Patch, ReleaseBuilder, SemanticVersioningSchema


class TestReleaseBuilder:
    class WithSimpleRelease:
        def it_build_releases(self):
            builder = ReleaseBuilder()
            builder.name("1.0.1")
            release = builder.build()

            assert release.name == "1.0.1"
            assert isinstance(release, MainRelease)
            

    class WithSemanticVersioning:
        def it_build_major_releases(self):
            builder = ReleaseBuilder(SemanticVersioningSchema())
            builder.name("1.0.0")
            release = builder.build()
            
            assert release.name == "1.0.0"
            assert isinstance(release, MajorRelease)


        def it_build_minor_releases(self):
            builder = ReleaseBuilder(SemanticVersioningSchema())
            builder.name("1.1.0")
            release = builder.build()
            
            assert release.name == "1.1.0"
            assert isinstance(release, MinorRelease)


        def it_build_patches(self):
            builder = ReleaseBuilder(SemanticVersioningSchema())
            builder.name("1.1.1")
            release = builder.build()
            
            assert release.name == "1.1.1"
            assert isinstance(release, Patch)
