from releasy.models.contributor import Contributor


class DescribeContributor:
    def it_has_name(self, alice: Contributor):
        assert alice.name == "Alice"

