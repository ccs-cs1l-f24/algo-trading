from strategies import *

traders = {}
traders["default"] = [scoreTrader(unitScore), scoreTrader(negativeUnitScore), scoreTrader(getDerivative), scoreTrader(dayTrade), scoreTrader(biggestLosers)]
traders["control_only"] = [scoreTrader(unitScore)]
traders["day_trader_vs_derivative_trader"] = [scoreTrader(getDerivative), scoreTrader(dayTrade)]
traders["day_traders"] = [scoreTrader(unitScore), scoreTrader(lambda elt: dayTrade(elt, 2)), scoreTrader(lambda elt: dayTrade(elt, 3)), scoreTrader(lambda elt: dayTrade(elt, 4)), scoreTrader(lambda elt: dayTrade(elt, 5)), scoreTrader(lambda elt: dayTrade(elt, 10))]