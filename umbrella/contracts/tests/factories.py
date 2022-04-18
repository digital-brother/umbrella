import factory
from factory.django import DjangoModelFactory

from umbrella.contracts.models import Contract, Clause, KDP
from umbrella.users.tests.factories import UserFactory


class ContractFactory(DjangoModelFactory):
    file_name = factory.Sequence(lambda n: f"contract_{n}.pdf")
    created_by = factory.SubFactory(UserFactory)
    file_size = 1024
    file_hash = factory.Sequence(lambda n: f"file_hash_{n}")
    modified_file_name = factory.Sequence(lambda n: f"modified_file_name_{n}")

    class Meta:
        model = Contract

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for extracted_group in extracted:
                self.groups.add(extracted_group)


class TermClauseFactory(DjangoModelFactory):
    type = "term"
    contract = factory.SubFactory(ContractFactory)

    class Meta:
        model = Clause


class StartKDPFactory(DjangoModelFactory):
    type = 'start'
    clause = factory.SubFactory(TermClauseFactory)
    contract = factory.LazyAttribute(lambda kdp: kdp.clause.contract)

    class Meta:
        model = KDP
