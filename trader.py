import json
import pprint


class Trader():
    def __init__(self, client, strategy, money_to_trade=100, leverage=5, symbol="XBTUSD"):
        self.client = client
        self.strategy = strategy

        self.money_to_trade = money_to_trade
        self.leverage = leverage

        self.open_position = False
        self.size = 500
        self.symbol = symbol
        self.position = self.client.Position.Position_get(filter=json.dumps({"symbol": self.symbol})).result()[0][0]
        self.open_position = self.position["isOpen"]
        self.exposure = self.position["currentQty"]

    def execute_trade(self):
        
        prediction = self.strategy.predict()
        try:
            self.position = self.client.Position.Position_get(filter=json.dumps({"symbol": self.symbol})).result()[0][0]
        except:
            pass
        self.open_position = self.position["isOpen"]
        self.exposure = self.position["currentQty"]

        if self.open_position: 
            print ("{:<20} | {:<15}".format('Param','Value'))
            print ("-"*38)
            for k, v in self.get_postion().items():
                print ("{:<20}   {:<15}".format(k, v))

            
            # Check to hack
            
            # Check trade exit

            if prediction == -1:
                if self.exposure > 0: # already long
                    self.close_position() # exit position
                # else hold as already short
            if prediction == 1:
                if self.exposure < 0:
                    self.close_position() # exit position
                # else hold as already long
        
        else:
            print("NO POSITIONS OPEN")

            if prediction == -1: # go short
                self.exec_trade(side="Sell")
            if prediction == 1: # go long
                self.exec_trade(side="Buy")
            
        

        return

    def get_postion(self):
        satosh = 100000000

        positions = self.position

        processed_position = {}
        timestamp_minute = str(positions["openingTimestamp"]).split(':')[0] + ":" + \
                        str(positions["openingTimestamp"]).split(':')[1] + ":00"

        processed_position["openTimestamp"] = timestamp_minute
        processed_position["isOpen"] = positions["isOpen"]
        processed_position["currentQty"] = positions["currentQty"]
        processed_position["leverage"] = positions["leverage"]
        processed_position["liquidationPrice"] = positions["liquidationPrice"]
        processed_position["entryPrice"] = positions["avgEntryPrice"]
        processed_position["entryValue"] = 1/ positions["avgEntryPrice"] * positions["currentQty"]
        processed_position["breakEvenPrice"] = positions["breakEvenPrice"]
        processed_position["lastPrice"] = positions["lastPrice"]
        processed_position["marked_price"] = positions["markPrice"]
        processed_position["margin"] = (positions["posMargin"] /satosh)
        processed_position["posValue"] = positions["homeNotional"]
        processed_position["futPNL"] = ((1 / positions["avgEntryPrice"])-(1 / positions["markPrice"])) * positions["currentQty"]
        processed_position["futROE"] = str(positions["unrealisedRoePcnt"] * 100) + "%"
        processed_position["markPNL"] = ((1 / positions["avgEntryPrice"])-(1 / self.strategy.close)) * positions["currentQty"]
        processed_position["markROE"] = str((processed_position["markPNL"] / processed_position["margin"])*100) + "%"
        return processed_position

    
    def close_position(self):
        res = self.client.Order.Order_closePosition(symbol=self.symbol).result()
        self.open_position = False
        # TODO CHECK position is closed

    def exec_trade(self, side):
        # check max size
        lotsize = 500
        print(f"Submitting {side} Order of {lotsize}!")
        try:
            response = self.client.Order.Order_new(
                        symbol=self.symbol,
                        side=side,
                        orderQty=self.size,
                    ).result()
            self.open_position = True
        except Exception:
                    print("Order error!")

    def get_open_orders(self):
        pass
    
    def pull_orders(self):
        pass

    def update_leverage(self, leverage):
        self.leverage = leverage
        res = self.client.Position.Position_updateLeverage(symbol=self.symbol, leverage=leverage).result()

    def account_position(self):
        # account balance
        # account margin
        # realised PNL
        # unrealised PNL
        pass
