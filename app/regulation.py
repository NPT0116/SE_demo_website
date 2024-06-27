class Regulation:
    def __init__(self):
        self.period = ["no period", "3 months", "6 months"]
        self.minimum_deposit_money = 100000  # Số tiền gửi tối thiểu
        self.minimum_withdraw_day = 15
        self.interest_rate = {
            "no period": 0.015,
            "3 months": 0.05,
            "6 months": 0.055
        }

    def add_period(self, new_period, interest_rate):
        if new_period not in self.period:
            self.period.append(new_period)
            self.interest_rate[new_period] = interest_rate

    def set_minimum_deposit_money(self, amount):
        self.minimum_deposit_money = amount

    def get_periods(self):
        return self.period

    def get_minimum_deposit_money(self):
        return int(self.minimum_deposit_money)

    def set_interest_rate(self, period, rate):
        if period in self.period:
            self.interest_rate[period] = rate
        else:
            raise ValueError(f"Period '{period}' not found in periods")

    def get_interest_rate(self, period):
        return self.interest_rate.get(period, None)
    
    def set_minimum_withdraw_day (self, day):
        self.minimum_withdraw_day = day

    def get_minimum_withdraw_day (self):
        return self.minimum_withdraw_day
# Khởi tạo đối tượng Regulation toàn cục
regulation = Regulation()
