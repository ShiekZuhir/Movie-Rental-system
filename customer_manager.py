class CustomerManager:
    def __init__(self):
        self.customers = []

    def has_customers(self):
        return len(self.customers) > 0