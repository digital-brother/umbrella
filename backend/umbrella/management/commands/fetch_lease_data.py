import sys

from django.core.management.base import BaseCommand
from django.utils import timezone

from backend.umbrella.models import Lease


class Command(BaseCommand):
    help = 'Copy data from old database to new database'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("Starting data transfer at:  %s" % time)

        # remove data from destination db before copying
        # to avoid primary key conflicts or mismatches
        # if Lease.objects.using('default').exists():
        #      Lease.objects.using('default').all().delete()

        # get data form the source database
        prodLeaseCount = Lease.objects.using('prod_db').count()

        print("Total : %s Lease in old database" % (prodLeaseCount))
        start = 0
        # count = prodLeaseCount
        count = 2
        size = 1

        for i in range(start, count, size):
            print("Tranfering data :  %s" % i)
            sys.stdout.flush()
            original_data = Lease.objects.using('prod_db').all()[i:i + size]
            print(original_data)
            Lease.objects.using('default').bulk_create(original_data)
