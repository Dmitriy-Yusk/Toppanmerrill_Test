from unittest import TestCase
from right_steering_wheel import Car, Address, User, UserCarsHelper


class TestUserCarsHelper(TestCase):
    def test_user_has_right_steering_wheel_car(self):
        car_bmw_m5 = Car(model='BMW M5')
        addr_london = Address(country='UK', city='London')

        user_bill = User('Bill', addr_london)
        user_bill.add_car(car_bmw_m5)

        if not UserCarsHelper.user_has_right_steering_wheel_car(user_bill):
            self.fail()

        addr_munich = Address(country='DE', city='Munich')
        car_civic = Car(model='Honda Civic', right_steering_wheel=True)

        user_sholz = User('Sholz', addr_munich)
        user_sholz.add_car(car_civic)
        user_sholz.add_car(car_bmw_m5)

        if not UserCarsHelper.user_has_right_steering_wheel_car(user_sholz):
            self.fail()

    def test_user_has_left_steering_wheel_car(self):
        addr_ny = Address(country='US', city='New York')
        car_cadillac = Car(model='Cadillac Escalade')

        addr_john = User('John', addr_ny)
        addr_john.add_car(car_cadillac)

        if UserCarsHelper.user_has_right_steering_wheel_car(addr_john):
            self.fail()
