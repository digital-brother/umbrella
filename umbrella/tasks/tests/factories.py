import factory
from factory.django import DjangoModelFactory

from umbrella.contracts.tests.factories import ContractFactory
from umbrella.tasks.models import Task, Comment
from umbrella.users.tests.factories import UserFactory


class TaskFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Task {n}")
    contract = factory.SubFactory(ContractFactory)
    contract_clause_type = factory.Sequence(lambda n: f"Test Clause {n}")
    contract_business_intelligence_type = factory.Sequence(lambda n: f"BI Type {n}")
    link_to_contract_text = factory.Sequence(lambda n: f"text_link_{n}")

    class Meta:
        model = Task

    @factory.post_generation
    def assignees(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of assignee were passed in, use them
            for extracted_assignee in extracted:
                self.assignees.add(extracted_assignee)


class CommentFactory(DjangoModelFactory):
    message = factory.Sequence(lambda n: f"Comment {n}")
    task = factory.SubFactory(TaskFactory)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Comment
