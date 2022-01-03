from matplotlib import pyplot as plt
import seaborn as sns


class MultiBase:

    def __init__(self, coin, data, matrix, start, end, amount, max_loss):
        self.coin = coin
        self.data = data
        self.matrix = matrix
        self.start = start
        self.end = end
        self.amount = amount
        self.max_loss = max_loss
        self.trade_costs = .005
        self.initial_balance = amount
        self.current_balance = amount
        self.units = 0
        self.trades = 0
        self.position = 0
        self.own = 0
        self.purchase_price = None
        self.hold_time = []
        self.ret_tracker = []

    def set_commission(self, amount):
        """
        Sets commission as a percent
        :param amount: float
        """
        self.trade_costs = amount

    def plot_data(self):
        """
        Graphs periods of holding over price movement in lineplot
        :return: lineplot
        """
        temp = self.data.copy()
        temp = temp.reset_index()
        sns.set(rc={'figure.figsize': (60, 45)})
        ax = sns.lineplot(x=temp.index, y=temp.Price, data=temp)
        marker = self.hold_time
        fm = 0
        lm = 1
        for i in range(len(marker) - 1):
            try:
                plt.axvspan(marker[fm], marker[lm], color="gray")
            except IndexError:
                pass
            fm += 2
            lm += 2
        plt.title("Time of exposure | {0}".format(self.coin), fontsize=110, y=1.05)
        ax.set_xlabel("Time", fontsize=80)
        ax.set_ylabel("Price", fontsize=80)
        plt.show()
        plt.clf()

    def get_values(self, bar):
        date = str(self.data.index[bar].date())
        price = round(self.data.Price.iloc[bar], 5)
        return date, price

    def print_current_balance(self, bar):
        date, price = self.get_values(bar)
        print("{0} | Current Balance: {1}".format(date, round(self.current_balance, 2)))

    def buy(self, bar):
        if self.own == -1:
            pass
        else:
            date, price = self.get_values(bar)
            units = float(self.current_balance / price)
            self.current_balance -= units * price
            self.units += units
            self.current_balance -= price * units * self.trade_costs
            self.trades += 1
            self.hold_time.append(bar)
            self.own = 1
            self.purchase_price = price
            print("{0} | Buying {1} for {2}".format(date, units, round(price, 5)))

    def sell(self, bar):
        if self.own == 0:
            pass
        else:
            date, price = self.get_values(bar)
            units = self.units
            self.current_balance += units * price
            self.current_balance -= price * units * self.trade_costs
            self.units = 0
            self.trades += 1
            self.own = 0
            self.hold_time.append(bar)
            self.purchase_price = None
            print("{0} | Selling {1} for {2}".format(date, units, round(price, 5)))

    def print_current_nav(self, bar):
        date, price = self.get_values(bar)
        nav = self.current_balance + self.units * price
        print("{0} | Net Asset Value = {1}".format(date, round(nav, 2)))

    def close_pos(self, bar):
        if self.own == -1:
            date, price = self.get_values(bar)
            print("-" * 75)
            print("{0} | +++ CLOSING FINAL POSITION +++".format(date))
            self.current_balance += self.units * price
            self.current_balance -= (abs(self.units * price * .005))
            print("{0} | closing position of {1} for {2}".format(date, self.units, price))
            self.units = 0
            self.trades += 1
            perf = (self.current_balance - self.initial_balance) / self.initial_balance * 100
            self.print_current_balance(bar)
            print("{0} | net performance (%) = {1}".format(date, round(perf, 2)))
            print("{0} | number of trades executed = {1}".format(date, self.trades))
            print("-" * 75)
        else:
            date, price = self.get_values(bar)
            print("-" * 75)
            print("{0} | +++ CLOSING FINAL POSITION +++".format(date))
            perf = (self.current_balance - self.initial_balance) / self.initial_balance * 100
            self.print_current_balance(bar)
            print("{0} | net performance (%) = {1}".format(date, round(perf, 2)))
            print("{0} | number of trades executed = {1}".format(date, self.trades))
            print("-" * 75)
        self.ret_tracker.append(round(perf, 2))


class MultiVariableBackTest(MultiBase):

    def multi_variable_test(self, parama=None):
        print(parama)
        stm = "Testing Multi-Variable Strategy for | {0}".format(self.coin)
        print("-" * 75)
        print(stm)
        print("-" * 75)

        # reset
        self.position = 0
        self.trades = 0
        self.current_balance = self.initial_balance

        for slug in self.matrix:
            base_points = list(slug)
            low = float(base_points[0])
            high = float(base_points[1])
            # first = self.matrix[slug][0]
            # second = self.matrix[slug][1]
            # third = self.matrix[slug][2]
            # fourth = self.matrix[slug][3]
            for bar in range(len(self.data) - 1):

                if self.data["price_z"].iloc[bar] < -1:
                    if self.position in [0, -1]:
                        if low < self.data["price_z"].iloc[bar] > high:
                            self.buy(bar)
                            self.position = 1
                        else:
                            pass
                elif self.data["vol_z"].iloc[bar] < .5:
                    if self.position in [-0, 1]:
                        self.sell(bar)
                        self.position = -1
            self.close_pos(bar + 1)
            if self.current_balance > self.initial_balance:
                self.plot_data()
            else:
                pass
