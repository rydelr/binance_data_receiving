import csv
import json
import time
import os, os.path


trade_pair = "xmrusdt"
res = int(input("round to: "))
file_name = f"extracted_trades/{trade_pair}/extracted_trades_{trade_pair}_{res}.csv"
stream_file = f"datastream/{trade_pair}/recent_trades_{trade_pair}.txt"
config_name = f"config/{trade_pair}/{trade_pair}_config_{res}.json"
rnd = 2

header = [str('Time'), str('Price'), str('Amount Bought'), str('Amount Sold'), str('Delta'), str("Sum of Delta"),
          str("Volume")]

# Kod który od nowa nadpisuje cały plik:
overwrite = str(input("Czy nadpisać istniejący plik? (Tak/Nie [y/n]): "))
continous = str(input("Czy pozostawić program w trybie non stop analysis? (Tak/Nie [y/n]): "))

if str.lower(overwrite) == ('y' or 'yes' or 'tak' or 't'):

    while True:
        try:
            with open(file_name, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

        try:
            with open(config_name, 'w') as f:
                config = {
                        "Last_Row": 0,
                        "Sum_of_Delta": 0,
                        "previous_price": 0,
                        "previous_time": 0,
                        "amount_sold": 0,
                        "amount_bought": 0,
                        "volume": 0,
                        }
                json.dump(config, f)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(config_name), exist_ok=True)
        else:
            break

i = 1
while i == 1:
    with open(config_name, "r") as json_load:
        data = json.load(json_load)
        LastRow = data["Last_Row"]
        Sum_of_Delta = data["Sum_of_Delta"]
        previous_price = data["previous_price"]
        previous_time = data["previous_time"]
        amount_sold = data["amount_sold"]
        amount_bought = data["amount_bought"]
        volume = data["volume"]
        print(f"Last Row = {LastRow}")

    with open(stream_file, "r") as dataread:
        lines = dataread.readlines()[LastRow:]
        for line in lines:
            actual_time = int(line[0:13])
            actual_price = float(line[14:26])
            amount = float(line[27:37])
            is_sell = line[38:44]

            if is_sell == "True \n":
                is_sell = bool(True)
            else:
                is_sell = bool(False)

            amount = round(amount, rnd)
            if res <= 0:
                actual_price = round(actual_price, res)

            if (actual_price == previous_price) & (is_sell is True):
                amount_sold += amount
            elif (actual_price == previous_price) & (is_sell is False):
                amount_bought += amount

            elif (actual_price != previous_price) & (is_sell is True):
                save_buys = round(amount_bought, rnd)
                save_sells = round(amount_sold, rnd)

                volume = abs(round(save_buys + save_sells, rnd))
                difference = save_buys - save_sells
                delta = round(difference, rnd)
                Sum_of_Delta += delta
                Sum_of_Delta = round(Sum_of_Delta, (rnd - 2))

                timestamp = previous_time

                trade = [timestamp, previous_price, save_buys, save_sells, delta, Sum_of_Delta, volume]

                if previous_price > 0:
                    with open(file_name, 'a+', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(trade)

                amount_sold = amount
                amount_bought = 0

            elif (actual_price != previous_price) & (is_sell is False):
                save_buys = round(amount_bought, rnd)
                save_sells = round(amount_sold, rnd)

                volume = abs(round(save_buys + save_sells, rnd))
                difference = save_buys - save_sells
                delta = round(difference, rnd)
                Sum_of_Delta += delta
                Sum_of_Delta = round(Sum_of_Delta, (rnd - 2))

                timestamp = previous_time

                trade = [timestamp, previous_price, save_buys, save_sells, delta, Sum_of_Delta, volume]

                if previous_price > 0:
                    with open(file_name, 'a+', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(trade)

                amount_bought = amount
                amount_sold = 0

            else:
                print("something went wrong!")
            LastRow += 1
            previous_price = actual_price
            previous_time = actual_time
            volume = 0

    # zapisanie ostatniego wiersza:
    with open(config_name, 'w') as f:
        config = {
                "Last_Row": LastRow,
                "Sum_of_Delta": Sum_of_Delta,
                "previous_price": previous_price,
                "previous_time": previous_time,
                "amount_sold": amount_sold,
                "amount_bought": amount_bought,
                "volume": volume
                }
        json.dump(config, f)
    if str.lower(continous) != ('y' or 'yes' or 'tak' or 't'):
        i = -1
    time.sleep(30)
