import datetime as dt


class Record:
    DATE_FORMAT = '%d.%m.%Y'
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()

#Родительский класс.
class Calculator: 
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    #Расчёт остатка.
    def day_remainder(self):
        remainder_day = self.limit - self.get_today_stats()
        return remainder_day
    
    #Сохраняет новую запись в списке.
    def add_record(self, record):
        self.records.append(record)
    
    #Количество потраченных денег за сегодня.
    def get_today_stats(self):
        date_today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == date_today)
    
    #Расчет денег\калорий за последние 7 дней.
    def get_week_stats(self):
        date_today = dt.date.today()
        week_delta = date_today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if date_today >= record.date >= week_delta)

#Калькулятор калорий.
class CaloriesCalculator(Calculator):  
    TEXT_CALORIES = ("Сегодня можно съесть что-нибудь ещё, "
                 "но с общей калорийностью не более {value} кКал") 
    TEXT_2_CALORIES = "Хватит есть!"

    #Вывод количества калорий.
    def get_calories_remained(self):
        remainder_day = self.day_remainder()
        if remainder_day > 0:
            return self.TEXT_CALORIES.format(value=remainder_day)                
        else:
            return self.TEXT_2_CALORIES

#Калькулятор денег.
class CashCalculator(Calculator):
    RUB_RATE = float(1.0)
    USD_RATE = float(60.0)
    EURO_RATE = float(70.0)
    
    CURRENCIES = {
        'rub': (RUB_RATE, 'руб'),
        'usd': (USD_RATE, 'USD'),
        'eur': (EURO_RATE, 'Euro')
    }
    TEXT_CASH_REMAINS = ("На сегодня осталось {spent}"
                "{currency_name}")
    TEXT_DEBT_CASH = ("Денег нет, держись: твой долг - "
                    "{spent} {currency_name}")
    TEX_NO_CASH = ("Денег нет, держись")
    TEXT_NO_CURRENCY = ("Данная валюта {no_currency} не поддерживается")
    
    #Конвертация валюты и условия вывода.
    def get_today_cash_remained(self, currency='rub'):
        #Обработка исключений.
        if currency not in self.CURRENCIES: 
            raise ValueError(self.TEXT_NO_CURRENCY.format(
            	no_currency=currency
            	))

        remainder_day = self.day_remainder()
        
        if remainder_day == 0:
            return self.TEX_NO_CASH
        
        #Распаковываем словарь и округляем валюту до сотых.
        rate, currency_name = self.CURRENCIES[currency]
        spent_by_currency = round(remainder_day/ rate, 2)
        
        if remainder_day > 0:
            return self.TEXT_CASH_REMAINS.format(
            	spent=spent_by_currency,
            	currency_name=currency_name
            	)
        else:
             return self.TEXT_DEBT_CASH.format(
             	spent=spent_by_currency,
            	currency_name=currency_name
            	)

if __name__ == '__main__':
    pass
      