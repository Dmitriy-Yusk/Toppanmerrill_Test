from collections import namedtuple

DrinkType = namedtuple('DrinkType', 'BEER WINE WATER')
SUPPORTED_DRINKS = DrinkType(BEER='Beer', WINE='Wine', WATER='Water')


class BaseBottledDrink:
    def __init__(self, drink_type, name):
        self._drink_type = drink_type
        self._name = name

    def get_drink_type(self):
        return self._drink_type

    def get_name(self):
        return self._name

    def __repr__(self):
        return f'Bottle of {self._drink_type}: "{self._name}"'


class BottledBeer(BaseBottledDrink):
    def __init__(self, name):
        super().__init__(SUPPORTED_DRINKS.BEER, name)


class BottledWine(BaseBottledDrink):
    def __init__(self, name):
        super().__init__(SUPPORTED_DRINKS.WINE, name)


class BottledWater(BaseBottledDrink):
    def __init__(self, name):
        super().__init__(SUPPORTED_DRINKS.WATER, name)


class SingletonMeta(type):
    """Not Thread Safe"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DrinkFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._drink_types = {}

    def register_drink_type(self, drink_type, drink_type_class):
        if drink_type not in SUPPORTED_DRINKS:
            return False

        self._drink_types[drink_type] = drink_type_class

        return True

    def create_drink(self, drink_type, name):
        if drink_type not in self._drink_types:
            return None

        drink_type_class = self._drink_types[drink_type]

        return drink_type_class(name)


class Fridge:
    def __init__(self, name, *args):
        if len(args) < 1:
            raise Exception('')

        self._name = name
        self._supported_drink_types = args[0]

        for drink_type in self._supported_drink_types:
            self.__setattr__(drink_type, [])

    def get_drink_types(self):
        return self._supported_drink_types

    def add_drink(self, drink_obj: BaseBottledDrink):
        drink_type = drink_obj.get_drink_type()
        if drink_type not in self._supported_drink_types:
            return False

        self.__dict__[drink_type].append(drink_obj)

        return True

    def get_drink(self, drink_type, drink_name: str = ''):
        """Find by Drink name is not implemented"""
        if drink_type not in self._supported_drink_types:
            return None

        drinks = self.__dict__[drink_type]
        if len(drinks) < 1:
            return None

        drink = drinks.pop()

        return drink

    def __repr__(self):
        return str(self.__dict__)


class StorageFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._storages = {}

    def register_storage(self, storage_obj: Fridge):
        drink_types = storage_obj.get_drink_types()

        for drink_type in drink_types:
            if drink_type not in self._storages:
                self._storages[drink_type] = storage_obj

    def get_storage_by_drink_type(self, drink_type) -> Fridge:
        if drink_type in self._storages:
            return self._storages[drink_type]

        return None


class BottledDrinkServe:
    @staticmethod
    def _open_bottle(drink_obj: BaseBottledDrink):
        print(f'Open the bottle of "{drink_obj.get_name()}"')

    @staticmethod
    def _put_on_table(drink_obj: BaseBottledDrink):
        print(f'Put the bottle of "{drink_obj.get_name()}" to a table')

    @classmethod
    def serve(cls, drink_obj: BaseBottledDrink, *args):
        cls._open_bottle(drink_obj)
        cls._put_on_table(drink_obj)


class BottledBeerServe(BottledDrinkServe):
    pass


class BottledWineServe(BottledDrinkServe):
    @staticmethod
    def _give_sniff_at_the_cork(drink_obj: BaseBottledDrink, client):
        if client is None:
            return
        print(f'Give a client a sniff at the cork of bottle of wine "{drink_obj.get_name()}"')

    @staticmethod
    def _pour_wine_into_glasses(drink_obj: BaseBottledDrink, clients: []):
        if clients is None or len(clients) < 1:
            return
        print(f'Pour "{drink_obj.get_name()}" onto the glasses')

    @classmethod
    def serve(cls, drink_obj: BaseBottledDrink, *args):
        if len(args) < 1:
            return

        clients: [] = args[0]
        if len(clients) < 1:
            return

        main_client = clients[0]

        cls._open_bottle(drink_obj)
        cls._give_sniff_at_the_cork(drink_obj, main_client)
        cls._pour_wine_into_glasses(drink_obj, clients)
        cls._put_on_table(drink_obj)


class BottledWaterServe(BottledDrinkServe):
    @staticmethod
    def _pour_water_into_glass(drink_obj: BaseBottledDrink, client):
        if client is None:
            return
        print(f'Pour "{drink_obj.get_name()}" onto the glass')

    @classmethod
    def serve(cls, drink_obj: BaseBottledDrink, *args):
        if len(args) < 1:
            return

        clients: [] = args[0]
        if len(clients) < 1:
            return

        client = clients[0]

        cls._open_bottle(drink_obj)
        cls._pour_water_into_glass(drink_obj, client)
        cls._put_on_table(drink_obj)


class ServeInstructions(metaclass=SingletonMeta):
    def __init__(self):
        self._instructions = {
            SUPPORTED_DRINKS.BEER: BottledBeerServe,
            SUPPORTED_DRINKS.WINE: BottledWineServe,
            SUPPORTED_DRINKS.WATER: BottledWaterServe,
        }

    def get_instruction_by_drink_type(self, drink_type) -> BottledDrinkServe:
        if drink_type in self._instructions:
            return self._instructions[drink_type]
        return None

    def get_instruction_by_drink(self, drink_obj: BaseBottledDrink) -> BottledDrinkServe:
        drink_type = drink_obj.get_drink_type()
        if drink_type in self._instructions:
            return self._instructions[drink_type]
        return None


class Waiter:
    def __init__(self, name):
        self._name = name

    @staticmethod
    def bring_drink(drink_type, drink_name: str = '') -> BaseBottledDrink:
        no_drink = f'We do not have {drink_type}'
        if drink_type not in SUPPORTED_DRINKS:
            print(no_drink)
            return None

        storage = storage_factory.get_storage_by_drink_type(drink_type)
        if storage is None:
            print(no_drink)
            return None

        drink_obj = storage.get_drink(drink_type)

        if drink_obj is not None:
            print(f'Bring "{drink_obj.get_name()}"')

        return drink_obj

    @staticmethod
    def serve_drink(drink_obj: BaseBottledDrink, clients: []) -> bool:
        if drink_obj is None:
            return False

        serve_instruct = serve_instructions_factory.get_instruction_by_drink(drink_obj)
        if serve_instruct is None:
            return False

        serve_instruct.serve(drink_obj, clients)

        return True


drink_factory = DrinkFactory()
drink_factory.register_drink_type(SUPPORTED_DRINKS.BEER, BottledBeer)
drink_factory.register_drink_type(SUPPORTED_DRINKS.WINE, BottledWine)
drink_factory.register_drink_type(SUPPORTED_DRINKS.WATER, BottledWater)

main_cooler = Fridge('cooler', [SUPPORTED_DRINKS.BEER, SUPPORTED_DRINKS.WATER])
wine_cooler = Fridge('wine_cooler', [SUPPORTED_DRINKS.WINE])

storage_factory = StorageFactory()
storage_factory.register_storage(main_cooler)
storage_factory.register_storage(wine_cooler)

serve_instructions_factory = ServeInstructions()

