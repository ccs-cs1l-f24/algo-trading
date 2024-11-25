from strategies import *

traders = {}
traders["default"] = [scoreTrader(unitScore), scoreTrader(negativeUnitScore), scoreTrader(getDerivative), scoreTrader(dayTrade)]
traders["control_only"] = [scoreTrader(unitScore)]
traders["day_trader_vs_derivative_trader"] = [scoreTrader(getDerivative), scoreTrader(dayTrade)]