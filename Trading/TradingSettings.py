

# Class to set up settings for trading

class TradeSettings:
    def __init__(self, BaselineToken, BaselinePercentageHold, PercentageTrade):
        self.BaselineToken = BaselineToken
        self.BaselinePercentageHold = BaselinePercentageHold
        self.PercentageTrade = PercentageTrade
        print(f'Trade settings as follows: BaselineToken = {self.BaselineToken}, BaselinePercentageHold = {self.BaselinePercentageHold}, PercentageTrade = {self.PercentageTrade}')

    # Method to change the baseline token
    def changebaselinetoken(self, NewToken):
        self.BaselineToken = NewToken
        print(f'Baseline Token changed to {self.BaselineToken}')
        # Notify user of new Trade Settings
        print(f'New Trade settings are: BaselineToken = {self.BaselineToken}, BaselinePercentageHold = {self.BaselinePercentageHold}, PercentageTrade = {self.PercentageTrade}')

    # Method to change BaselinePercentageHold
    def changebaselinepercentagehold(self, NewPercentageHold):
        self.BaselinePercentageHold = NewPercentageHold
        print(f'Baseline Percentage Hold changed to {self.BaselinePercentageHold}')
        # Notify user of new trade settings
        print(f'New Trade settings are: BaselineToken = {self.BaselineToken}, BaselinePercentageHold = {self.BaselinePercentageHold}, PercentageTrade = {self.PercentageTrade}')

    # Method to change Percentage Trade amount
    def changepercentagetrade(self, NewPercentageTrade):
        self.PercentageTrade = NewPercentageTrade
        print(f'Baseline Percentage Trade changed to {self.PercentageTrade}')
        # Notify user of new Trade Settings
        print(
            f'New Trade settings are: BaselineToken = {self.BaselineToken}, BaselinePercentageHold = {self.BaselinePercentageHold}, PercentageTrade = {self.PercentageTrade}')

    # Method to change all settings
    def changeallsettings(self, NewToken, NewPercentageHold, NewPercentTrade):
        self.BaselineToken = NewToken
        self.BaselinePercentageHold = NewPercentageHold
        self.PercentageTrade = NewPercentTrade
        # Notify user of the changes
        print(
            f'New Trade settings are: BaselineToken = {self.BaselineToken}, BaselinePercentageHold = {self.BaselinePercentageHold}, PercentageTrade = {self.PercentageTrade}')

    # Method to confirm and save trade settings
    def confirm(self):
        # Get input from user if they are happy with settings
        outcome = input("Please confirm with 'Y' or 'y' if happy with new settings")
        if outcome == "Y":
            print("Settings accepted, updating database")
        elif outcome == "y":
            print("Settings accepted, updating database")
        else:
            newsetting = input("Select which option to change: "
                               "1. All "
                               "2. Baseline Token "
                               "3. Baseline Percentage Hold "
                               "4. Percentage Trade ")
            print(newsetting)
            print(type(newsetting))
            if newsetting == "1":
                settings = []
                result = input("Input new baselinetoken symbol")
                settings.append(result)
                result = input("Input new baseline percentage hold")
                result = int(result)
                settings.append(result)
                result = input("Input new percentage trade amount")
                result = int(result)
                settings.append(result)
                self.changeallsettings(settings[0], settings[1], settings[2])
            elif newsetting == "2":
                settings = input("Input new baselinetoken symbol")
                self.changebaselinetoken(settings)
            elif newsetting == "3":
                settings = input("Input new baseline percentage hold")
                settings = int(settings)
                self.changebaselinepercentagehold(settings)
            elif newsetting == "4":
                settings = input("Input new percentage trade amount")
                settings = int(settings)
                self.changepercentagetrade(settings)
            else:
                "Wrong selection made, try again"

