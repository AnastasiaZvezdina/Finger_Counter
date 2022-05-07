class Vehicle():
    def __init__(self, color, price, type):
        self.color = color
        self.price = price
        self.type = type
    
    def drive(self):
        print(self.color, self.type, "поехал")
    def stop(self):
        print(self.color, self.type, "остановился")

car1 = Vehicle("Красный", 10000, "легковой")
car2 = Vehicle("Зелёный", 100000, "грузовой")
print(car1.color, car1.price, car1.type)
car1.drive()
car2.drive()