from django.core.management.base import BaseCommand
from details.models import Test

class Command(BaseCommand):
    help = 'Add data to Test model'

    def handle(self, *args, **kwargs):
        # Sample data to be added
        test_data = [
            {'test_id':1,'test_name': 'GLYCOSYLATED HEMOGLOBIN (HBA1c) ', 'collection_status': 'no', 'price': 500},
            {'test_id':2,'test_name': 'BLOOD UREA NITROGEN - BUN ', 'collection_status': 'no', 'price': 250},
            {'test_id':3,'test_name': 'COMPLETE URINE EXAMINATION', 'collection_status': 'no', 'price': 150},
            {'test_id':4,'test_name': 'COTININE', 'collection_status': 'no', 'price': 500},
            {'test_id':5,'test_name': 'ERYTHROCYTE SEDIMENTATION RATE( ESR)', 'collection_status': 'no', 'price': 100},
            {'test_id':6,'test_name': 'HAEMOGRAM', 'collection_status': 'no', 'price': 250},
            {'test_id':7,'test_name': 'HBsAg - Hepatitis B surface Antigen', 'collection_status': 'no', 'price': 300},
            {'test_id':8,'test_name': 'HIV I & II Elisa', 'collection_status': 'no', 'price': 400},
            {'test_id':9,'test_name': 'LIPID PROFILE', 'collection_status': 'no', 'price': 550},
            {'test_id':10,'test_name': 'LIVER FUNCTION TEST', 'collection_status': 'no', 'price': 550},
            {'test_id':11,'test_name': 'RANDOM BLOOD SUGAR', 'collection_status': 'no', 'price': 50},
            {'test_id':12,'test_name': 'RFT/KFT', 'collection_status': 'no', 'price': 800},
            {'test_id':13,'test_name': 'Test', 'collection_status': 'no', 'price': 150},
        ]

        # Add the data to the Test model
        for data in test_data:
            test, created = Test.objects.get_or_create(
                test_name=data['test_name'],
                defaults={'collection_status': data['collection_status'], 'price': data['price']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added test: {test.test_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Test {test.test_name} already exists"))
