from unittest import TestCase
from order_drink import SUPPORTED_DRINKS, drink_factory, storage_factory, Waiter


def init_data_for_testing():
    carlsberg_beer = drink_factory.create_drink(SUPPORTED_DRINKS.BEER, 'Carlsberg')
    hoegaarden_beer = drink_factory.create_drink(SUPPORTED_DRINKS.BEER, 'Hoegaarden')

    pg_wine = drink_factory.create_drink(SUPPORTED_DRINKS.WINE, 'Pinot Grigio')

    pepsi = drink_factory.create_drink(SUPPORTED_DRINKS.WATER, 'Pepsi')

    beer_storage = storage_factory.get_storage_by_drink_type(SUPPORTED_DRINKS.BEER)
    wine_storage = storage_factory.get_storage_by_drink_type(SUPPORTED_DRINKS.WINE)
    water_storage = storage_factory.get_storage_by_drink_type(SUPPORTED_DRINKS.WATER)

    beer_storage.add_drink(carlsberg_beer)
    beer_storage.add_drink(hoegaarden_beer)

    water_storage.add_drink(pepsi)

    wine_storage.add_drink(pg_wine)


class FunctionalTests(TestCase):
    def test_beer(self):
        init_data_for_testing()
        print('-------------------------------------------')

        waiter = Waiter('John')
        clients = ['Bill']
        drink = waiter.bring_drink(SUPPORTED_DRINKS.BEER)
        if drink is None:
            self.fail()
        if not waiter.serve_drink(drink, clients):
            self.fail()

    def test_wine(self):
        init_data_for_testing()
        print('-------------------------------------------')

        waiter = Waiter('John')
        clients = ['Bill']
        drink = waiter.bring_drink(SUPPORTED_DRINKS.WINE)
        if drink is None:
            self.fail()
        if not waiter.serve_drink(drink, clients):
            self.fail()

    def test_water(self):
        init_data_for_testing()
        print('-------------------------------------------')

        waiter = Waiter('John')
        clients = ['Bill']
        drink = waiter.bring_drink(SUPPORTED_DRINKS.WATER)
        if drink is None:
            self.fail()
        if not waiter.serve_drink(drink, clients):
            self.fail()
