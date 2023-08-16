from django.test import TestCase
from seizures.models import Seizure


class SeizureTestCase(TestCase):

    def __all__(self):
        self.delete()

    def create(self):
        Seizure.objects.create(
            address=__name__, device='test', ssid='django',
            latitude=39.952583, longitude=-75.165222,
            altitude=100, battery=100, brightness=0.5, volume=0.5
        )
        self.assertIsNotNone(Seizure.objects.all(), 'Cannot get seizures.')
        self.assertIsNotNone(Seizure.objects.first(), 'Cannot get seizure.')
        self.assertEqual(Seizure.objects.count(), 1, 'Bad count after create.')

    def delete(self):
        self.create()
        created = Seizure.objects.first()
        created.delete()
        self.assertIsNone(Seizure.objects.all(), 'Exists after delete.')
        self.assertIsNone(Seizure.objects.first(), 'Exists after delete.')
        self.assertEqual(Seizure.objects.count(), 0, 'Bad count after delete.')
