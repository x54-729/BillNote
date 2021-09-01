class Bill:

    def __init__(self, id, date, type_, method, description, amount, is_income=False):

        self.id = id
        self.date = date
        self.amount = amount
        self.type = type_
        self.description = description
        self.method = method
        self.is_income = is_income

        self.data_tuple = (self.id, self.date, self.type, self.method, self.description, self.amount)

    def __getitem__(self, index):

        return self.data_tuple[index]

    def __iter__(self):

        return iter(self.data_tuple)