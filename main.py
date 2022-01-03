from warehouse import Daryl
from multi_backtest import MultiVariableBackTest
if __name__ == "__main__":
    btc = Daryl("BTC")
    back_test = MultiVariableBackTest(btc.coin, btc.worked_data, btc.matrix, None, None, 10000, None)
    back_test.multi_variable_test()