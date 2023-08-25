from django.test import TestCase
from Bingo.models import Countries

class CountriesModelTest(TestCase):

    def test_string_representation(self):
        country = Countries.objects.create(name="Testland", country_code="TL")
        self.assertEqual(str(country), "Testland")

    def test_name_unique(self):
        country = Countries.objects.create(name="UniqueLand", country_code="UL")
        with self.assertRaises(Exception):
            # Trying to create another country with the same name should raise an exception
            another_country = Countries.objects.create(name="UniqueLand", country_code="UQ")

    def test_country_code_unique(self):
        country = Countries.objects.create(name="CodeLand", country_code="CD")
        with self.assertRaises(Exception):
            # Trying to create another country with the same country code should raise an exception
            another_country = Countries.objects.create(name="AnotherCodeLand", country_code="CD")

    def test_verbose_name_plural(self):
        self.assertEqual(Countries._meta.verbose_name_plural, "Countries")

    def test_create_and_retrieve_country(self):
        country = Countries.objects.create(name="SampleLand", country_code="SL")
        saved_country = Countries.objects.get(id=country.id)
        self.assertEqual(saved_country.name, "SampleLand")
        self.assertEqual(saved_country.country_code, "SL")
