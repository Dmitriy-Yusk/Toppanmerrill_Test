class Car:
    def __init__(self, model, right_steering_wheel=False):
        self._name = model
        self._right_steering = right_steering_wheel

    def is_right_steering(self) -> bool:
        return self._right_steering


class Address:
    def __init__(self, country, city) -> bool:
        self.country = country
        self.city = city


class User:
    def __init__(self, name, address: Address):
        self.name = name
        self.address = address
        self.cars = []

    def add_car(self, car):
        if car not in self.cars:
            self.cars.append(car)


RIGHT_STEERING_COUNTRIES = ('UK', 'AU', 'IN')


class UserCarsHelper:
    """Any weird behavior should be out of the main classes like Car, Address, User"""

    @staticmethod
    def user_has_right_steering_wheel_car(user) -> bool:
        """We force to return True for users who live in the countries"""
        """where cars have steering wheel at right in common, like UK"""
        """and the user has a car at all."""
        if len(user.cars) > 0 and user.address.country in RIGHT_STEERING_COUNTRIES:
            return True

        for car in user.cars:
            if car.is_right_steering():
                return True

        return False
