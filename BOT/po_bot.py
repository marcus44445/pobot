# import base64
# import json
# import random
# import time
# from datetime import datetime, timedelta

# import numpy as np
# from selenium.webdriver.common.by import By
# from utils import companies, get_driver

# BASE_URL = 'https://pocketoption.com'
# LENGTH_STACK_MIN = 460
# LENGTH_STACK_MAX = 1000
# PERIOD = 5
# TIME = 1
# SMA_LONG = 50
# SMA_SHORT = 8
# PERCENTAGE = 0.91
# STACK = {}
# ACTIONS = {}
# MAX_ACTIONS = 1
# ACTIONS_SECONDS = PERIOD - 1
# LAST_REFRESH = datetime.now()
# CURRENCY = None
# CURRENCY_CHANGE = False
# CURRENCY_CHANGE_DATE = datetime.now()
# HISTORY_TAKEN = False
# CLOSED_TRADES_LENGTH = 3
# MODEL = None
# SCALER = None
# PREVIOUS = 1200
# MAX_DEPOSIT = 0
# MIN_DEPOSIT = 0
# INIT_DEPOSIT = None

# NUMBERS = {
#     '0': '11',
#     '1': '7',
#     '2': '8',
#     '3': '9',
#     '4': '4',
#     '5': '5',
#     '6': '6',
#     '7': '1',
#     '8': '2',
#     '9': '3',
# }
# IS_AMOUNT_SET = True
# AMOUNTS = []
# EARNINGS = 15
# MARTINGALE_COEFFICIENT = 2.5

# # Define Ichimoku settings
# tenkanPeriod = 1
# kijunPeriod = 1
# senkouPeriod = 3

# driver = get_driver()

# def load_web_driver():
#     url = f'{BASE_URL}/en/cabinet/demo-quick-high-low/'
#     driver.get(url)

# def calculate_sma(data, period):
#     if len(data) < period:
#         return [np.nan] * len(data)  # Return NaNs if not enough data
#     return np.convolve(data, np.ones((period,)) / period, mode='valid')

# def get_ichimoku_values(stack):
#     values = list(stack.values())
#     hl2 = [(high + low) / 2 for high, low in zip(values, values)]  # Mocking high and low with same value, should be replaced with actual high-low data

#     if len(hl2) < max(tenkanPeriod, kijunPeriod, senkouPeriod):
#         return None

#     tenkan_sen = calculate_sma(hl2, tenkanPeriod)[-1]
#     kijun_sen = calculate_sma(hl2, kijunPeriod)[-1]
#     senkou_span_a = calculate_sma(hl2, (tenkanPeriod + kijunPeriod) // 2)[-1]
#     senkou_span_b = calculate_sma(hl2, senkouPeriod)[-1]
#     chikou_span = values[-1]

#     return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span

# # def change_currency():
# #     current_symbol = driver.find_element(by=By.CLASS_NAME, value='current-symbol')
# #     current_symbol.click()
# #     currencies = driver.find_elements(By.XPATH, "//li[contains(., '92%')]")
# #     if currencies:
# #         while True:
# #             currency = random.choice(currencies)
# #             if CURRENCY not in currency.text:
# #                 break
# #         currency.click()

# def do_action(signal):
#     action = True
#     try:
#         last_value = list(STACK.values())[-1]
#     except:
#         return
#     global ACTIONS, IS_AMOUNT_SET
#     for dat in list(ACTIONS.keys()):
#         if dat < datetime.now() - timedelta(seconds=ACTIONS_SECONDS):
#             del ACTIONS[dat]

#     if action:
#         if len(ACTIONS) >= MAX_ACTIONS:
#             action = False

#     if action:
#         if ACTIONS:
#             if signal == 'call' and last_value >= min(list(ACTIONS.values())):
#                 action = False
#             elif signal == 'put' and last_value <= max(list(ACTIONS.values())):
#                 action = False

#     if action:
#         try:
#             print(f"FinalResult:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {signal.upper()}, currency: {CURRENCY} last_value: {last_value}")
#             driver.find_element(by=By.CLASS_NAME, value=f'btn-{signal}').click()
#             ACTIONS[datetime.now()] = last_value
#             IS_AMOUNT_SET = False
#         except Exception as e:
#             print(e)

# def hand_delay():
#     time.sleep(random.choice([0.2, 0.3, 0.4, 0.5, 0.6]))

# def get_amounts(amount):
#     if amount > 1999:
#         amount = 1999
#     amounts = []
#     while True:
#         amount = int(amount / MARTINGALE_COEFFICIENT)
#         amounts.insert(0, amount)
#         if amounts[0] <= 1:
#             amounts[0] = 1
#             return amounts

# def check_values(stack):
#     try:
#         deposit = driver.find_element(by=By.CSS_SELECTOR, value='body > div.wrapper > div.wrapper__top > header > div.right-block > div.right-block__item.js-drop-down-modal-open > div > div.balance-info-block__data > div.balance-info-block__balance > span')
#     except Exception as e:
#         print(e)

#     global IS_AMOUNT_SET, AMOUNTS, INIT_DEPOSIT

#     if not INIT_DEPOSIT:
#         INIT_DEPOSIT = float(deposit.text)

#     if not AMOUNTS:
#         AMOUNTS = get_amounts(float(deposit.text))

#     if not IS_AMOUNT_SET:
#         if ACTIONS and list(ACTIONS.keys())[-1] + timedelta(seconds=PERIOD) > datetime.now():
#             return

#         try:
#             closed_tab = driver.find_element(by=By.CSS_SELECTOR, value='#bar-chart > div > div > div.right-widget-container > div > div.widget-slot__header > div.divider > ul > li:nth-child(2) > a')
#             closed_tab_parent = closed_tab.find_element(by=By.XPATH, value='..')
#             if closed_tab_parent.get_attribute('class') == '':
#                 closed_tab_parent.click()
#         except:
#             pass

#         closed_trades_currencies = driver.find_elements(by=By.CLASS_NAME, value='deals-list__item')
#         if closed_trades_currencies:
#             last_split = closed_trades_currencies[0].text.split('\n')
#             print("last_split:",last_split)
#             try:
#                 amount = driver.find_element(by=By.CSS_SELECTOR, value='#put-call-buttons-chart-1 > div > div.blocks-wrap > div.block.block--bet-amount > div.block__control.control > div.control__value.value.value--several-items > div > input[type=text]')
#                 # amount = 100
#                 amount_value = int(amount.get_attribute('value')[1:])
#                 base = '#modal-root > div > div > div > div > div.trading-panel-modal__in > div.virtual-keyboard.js-virtual-keyboard > div > div:nth-child(%s) > div'
#                 if '0.00' not in last_split[4]:  # win
#                     print("I am wining")
#                     if amount_value > 1:
#                         amount.click()
#                         hand_delay()
#                         driver.find_element(by=By.CSS_SELECTOR, value=base % NUMBERS['1']).click()
#                         AMOUNTS = get_amounts(float(deposit.text))  # refresh amounts
#                 elif '0.00' not in last_split[3]:  # draw
#                     print("I am drawing")
#                     pass
#                 else:  # lose
#                     amount.click()
#                     print("I am losing")
#                     time.sleep(random.choice([0.6, 0.7, 0.8, 0.9, 1.0, 1.1]))
#                     if amount_value in AMOUNTS and AMOUNTS.index(amount_value) + 1 < len(AMOUNTS):
#                         next_amount = AMOUNTS[AMOUNTS.index(amount_value) + 1]
#                         print("next_amount:",next_amount)
#                         for number in str(next_amount):
#                             driver.find_element(by=By.CSS_SELECTOR, value=base % NUMBERS[number]).click()
#                             hand_delay()
#                     else:  # reset to 1
#                         driver.find_element(by=By.CSS_SELECTOR, value=base % NUMBERS['1']).click()
#                         hand_delay()
#                 closed_tab_parent.click()
#             except Exception as e:
#                 print(e)
#         IS_AMOUNT_SET = True

#     if IS_AMOUNT_SET and datetime.now().second % PERIOD == 0:
#         ichimoku_values = get_ichimoku_values(stack)
#         if not ichimoku_values:
#             return

#         tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span = ichimoku_values

#         if chikou_span > tenkan_sen:
#             do_action('call')
#         elif chikou_span <= tenkan_sen:
#             do_action('put')

# def websocket_log(stack):
#     global CURRENCY, CURRENCY_CHANGE, CURRENCY_CHANGE_DATE, LAST_REFRESH, HISTORY_TAKEN, MODEL, INIT_DEPOSIT
#     try:
#         current_symbol = driver.find_element(by=By.CLASS_NAME, value='current-symbol').text
#         if current_symbol != CURRENCY:
#             CURRENCY = current_symbol
#             CURRENCY_CHANGE = True
#             CURRENCY_CHANGE_DATE = datetime.now()
#     except:
#         pass

#     if CURRENCY_CHANGE and CURRENCY_CHANGE_DATE < datetime.now() - timedelta(seconds=5):
#         stack = {}  # drop stack when currency changed
#         HISTORY_TAKEN = False  # take history again
#         driver.refresh()
#         CURRENCY_CHANGE = False
#         MODEL = None
#         INIT_DEPOSIT = None

#     for wsData in driver.get_log('performance'):
#         message = json.loads(wsData['message'])['message']
#         response = message.get('params', {}).get('response', {})
#         if response.get('opcode', 0) == 2 and not CURRENCY_CHANGE:
#             payload_str = base64.b64decode(response['payloadData']).decode('utf-8')
#             data = json.loads(payload_str)
#             if not HISTORY_TAKEN:
#                 if 'history' in data:
#                     stack = {int(d[0]): d[1] for d in data['history']}
#                     print(f"History taken for asset: {data['asset']}, period: {data['period']}, len_history: {len(data['history'])}, len_stack: {len(stack)}")
#             try:
#                 current_symbol = driver.find_element(by=By.CLASS_NAME, value='current-symbol').text
#                 symbol, timestamp, value = data[0]
#             except:
#                 continue
#             try:
#                 if current_symbol.replace('/', '').replace(' ', '') != symbol.replace('_', '').upper() and companies.get(current_symbol) != symbol:
#                     continue
#             except:
#                 pass

#             if len(stack) == LENGTH_STACK_MAX:
#                 first_element = next(iter(stack))
#                 del stack[first_element]
#             if len(stack) < LENGTH_STACK_MAX:
#                 if int(timestamp) in stack:
#                     return stack
#                 else:
#                     stack[int(timestamp)] = value
#             elif len(stack) > LENGTH_STACK_MAX:
#                 print(f"Len > {LENGTH_STACK_MAX}!!")
#                 stack = {}
#             if len(stack) >= LENGTH_STACK_MIN:
#                 check_values(stack)
#     return stack

# load_web_driver()
# while True:
#     STACK = websocket_log(STACK)



import base64
import json
import random
import time
from datetime import datetime, timedelta

import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import companies, get_driver

BASE_URL = 'https://pocketoption.com'
LENGTH_STACK_MIN = 460
LENGTH_STACK_MAX = 1000
PERIOD = 10
TIME = 1
SMA_LONG = 50
SMA_SHORT = 8
PERCENTAGE = 0.91
STACK = {}
ACTIONS = {}
MAX_ACTIONS = 1
ACTIONS_SECONDS = PERIOD - 1
LAST_REFRESH = datetime.now()
CURRENCY = None
CURRENCY_CHANGE = False
CURRENCY_CHANGE_DATE = datetime.now()
HISTORY_TAKEN = False
CLOSED_TRADES_LENGTH = 3
MODEL = None
SCALER = None
PREVIOUS = 1200
MAX_DEPOSIT = 0
MIN_DEPOSIT = 0
INIT_DEPOSIT = None
INIT_AMOUNT = 10
INIT_TIME_FRAME = "00:00:10"

NUMBERS = {
    '0': '11',
    '1': '7',
    '2': '8',
    '3': '9',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '1',
    '8': '2',
    '9': '3',
}
IS_AMOUNT_SET = True
AMOUNTS = []
EARNINGS = 15
MARTINGALE_COEFFICIENT = 2.5

# Defined periods for Ichimoku elements
TENKAN_PERIOD = 9
KIJUN_PERIOD = 26
SENKOU_B_PERIOD = 52

driver = get_driver()

def load_web_driver():
    url = f'{BASE_URL}/en/cabinet/demo-quick-high-low/'
    driver.get(url)

def calculate_ichimoku_elements(highs, lows, closes):
    if len(closes) < max(TENKAN_PERIOD, KIJUN_PERIOD, SENKOU_B_PERIOD):
        return None, None, None, None, None
    
    # Calculate Tenkan-sen (Conversion Line)
    tenkan_sen = (max(highs[-TENKAN_PERIOD:]) + min(lows[-TENKAN_PERIOD:])) / 2
    
    # Calculate Kijun-sen (Base Line)
    kijun_sen = (max(highs[-KIJUN_PERIOD:]) + min(lows[-KIJUN_PERIOD:])) / 2
    
    # Calculate Senkou Span A (Leading Span A)
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2)
    
    # Calculate Senkou Span B (Leading Span B)
    senkou_span_b = (max(highs[-SENKOU_B_PERIOD:]) + min(lows[-SENKOU_B_PERIOD:])) / 2
    
    # Calculate Chikou Span (Lagging Span)
    chikou_span = closes[-1]
    
    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span

def wait_for_element(css_selector, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
    except Exception as e:
        print(f"Element not found: {css_selector}, Exception: {e}")
        return None

def do_action(signal):
    action = True
    try:
        last_value = list(STACK.values())[-1]
    except:
        return
    global ACTIONS, IS_AMOUNT_SET
    for dat in list(ACTIONS.keys()):
        if dat < datetime.now() - timedelta(seconds=ACTIONS_SECONDS):
            del ACTIONS[dat]

    if action:
        if len(ACTIONS) >= MAX_ACTIONS:
            action = False

    if action:
        if ACTIONS:
            if signal == 'call' and last_value >= min(list(ACTIONS.values())):
                action = False
            elif signal == 'put' and last_value <= max(list(ACTIONS.values())):
                action = False

    if action:
        try:
            print(f"FinalResult:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {signal.upper()}, currency: {CURRENCY} last_value: {last_value}")
            action_button = wait_for_element(f'.btn-{signal}')
            if action_button:
                action_button.click()
                ACTIONS[datetime.now()] = last_value
                IS_AMOUNT_SET = False
        except Exception as e:
            print(e)

def hand_delay():
    time.sleep(random.choice([0.2, 0.3, 0.4, 0.5, 0.6]))

def get_amounts(amount):
    if amount > 1999:
        amount = 1999
    amounts = []
    index = 0
    while True:
        if not INIT_AMOUNT:            
            amount = int(amount / MARTINGALE_COEFFICIENT)
            amounts.insert(0, amount)
            if amounts[0] <= 1:
                amounts[0] = 1
                return amounts
        else:
            if (INIT_AMOUNT * MARTINGALE_COEFFICIENT**index) < amount: 
                amounts.append(int(INIT_AMOUNT * MARTINGALE_COEFFICIENT**index))
                index = index + 1
            else: return amounts            

def init_amount():
    try:
        closed_tab = wait_for_element('#bar-chart > div > div > div.right-widget-container > div > div.widget-slot__header > div.divider > ul > li:nth-child(2) > a')
        if closed_tab is None:
            return
        closed_tab_parent = closed_tab.find_element(by=By.XPATH, value='..')
        if closed_tab_parent.get_attribute('class') == '':
            closed_tab_parent.click()
    except:
        pass

    try:
        amount = wait_for_element('#put-call-buttons-chart-1 > div > div.blocks-wrap > div.block.block--bet-amount > div.block__control.control > div.control__value.value.value--several-items > div > input[type=text]')
        if amount is None:
            return
        base = '#modal-root > div > div > div > div > div.trading-panel-modal__in > div.virtual-keyboard.js-virtual-keyboard > div > div:nth-child(%s) > div'

        amount.click()
        hand_delay()

        for number in str(INIT_AMOUNT):
            numeric_button = wait_for_element(base % NUMBERS[number])

            if numeric_button:
                numeric_button.click()
                hand_delay()
        
        closed_tab_parent.click()
        
    except Exception as e:
        print(e)

    time.sleep(1.0)

def init_timeframe():
    try:
        timeDiv = wait_for_element('#put-call-buttons-chart-1 > div > div.blocks-wrap > div.block.block--expiration-inputs > div.block__control.control > div.control__value.value.value--several-items > div')

        if timeDiv is None:
            return
        
        timeDiv.click()
        hand_delay()

        plus_base = '#modal-root > div > div > div > div.trading-panel-modal__in > div:nth-child(%s) > a.btn-plus'
        minus_base = '#modal-root > div > div > div > div.trading-panel-modal__in > div:nth-child(%s) > a.btn-minus'
        
        current = timeDiv.text.split(":")
        target = INIT_TIME_FRAME.split(":")
        print(f"Current : {current}, Target : {target}")

        for i in range(3):
            plus_button = wait_for_element(plus_base % (i + 1))
            minus_button = wait_for_element(minus_base % (i + 1))

            diff = int(target[i]) - int(current[i])

            if i == 2 and target[0] == 0 and target[1] == 0: diff -= 5
            for j in range(abs(diff)):
                if diff < 0 : 
                    minus_button.click()
                    hand_delay()
                else:
                    plus_button.click()
                    hand_delay()
        
    except Exception as e:
        print(e)    

    time.sleep(1.0)

def check_values(stack):
    try:
        deposit = wait_for_element('body > div.wrapper > div.wrapper__top > header > div.right-block > div.right-block__item.js-drop-down-modal-open > div > div.balance-info-block__data > div.balance-info-block__balance > span')
        if deposit is None:
            return
    except Exception as e:
        print(e)

    global IS_AMOUNT_SET, AMOUNTS, INIT_DEPOSIT

    if not INIT_DEPOSIT:
        INIT_DEPOSIT = float(deposit.text)

    if not AMOUNTS:
        AMOUNTS = get_amounts(float(deposit.text))

    if not IS_AMOUNT_SET:
        if ACTIONS and list(ACTIONS.keys())[-1] + timedelta(seconds=PERIOD) > datetime.now():
            return

        try:
            closed_tab = wait_for_element('#bar-chart > div > div > div.right-widget-container > div > div.widget-slot__header > div.divider > ul > li:nth-child(2) > a')
            if closed_tab is None:
                return
            closed_tab_parent = closed_tab.find_element(by=By.XPATH, value='..')
            if closed_tab_parent.get_attribute('class') == '':
                closed_tab_parent.click()
        except:
            pass

        closed_trades_currencies = driver.find_elements(by=By.CLASS_NAME, value='deals-list__item')
        if closed_trades_currencies:
            last_split = closed_trades_currencies[0].text.split('\n')
            if len(last_split) < 5:  # Ensure last_split has expected elements
                print(f"Unexpected format for last_split: {last_split}")
                return
            print("last_split:", last_split)
            try:
                amount = wait_for_element('#put-call-buttons-chart-1 > div > div.blocks-wrap > div.block.block--bet-amount > div.block__control.control > div.control__value.value.value--several-items > div > input[type=text]')
                if amount is None:
                    return
                amount_value = int(amount.get_attribute('value')[1:])
                base = '#modal-root > div > div > div > div > div.trading-panel-modal__in > div.virtual-keyboard.js-virtual-keyboard > div > div:nth-child(%s) > div'
                if '0.00' not in last_split[4]:  # win
                    print("I am winning")
                    if amount_value > 1:
                        print("amount_value:", amount_value)
                        print("I am winning")
                        amount.click()
                        hand_delay()
                        if not INIT_AMOUNT:
                            numeric_button = wait_for_element(base % NUMBERS["1"])
                            if numeric_button:
                                numeric_button.click()    
                        else:
                            for number in str(INIT_AMOUNT):
                                numeric_button = wait_for_element(base % NUMBERS[number])
                                if numeric_button:
                                    numeric_button.click()
                                    hand_delay()
                        AMOUNTS = get_amounts(float(deposit.text))  # refresh amounts
                elif '0.00' not in last_split[3]:  # draw
                    print("I am drawing")
                    pass
                else:  # lose
                    amount.click()
                    print("I am losing")
                    time.sleep(random.choice([0.6, 0.7, 0.8, 0.9, 1.0, 1.1]))
                    if amount_value in AMOUNTS and AMOUNTS.index(amount_value) + 1 < len(AMOUNTS):
                        next_amount = AMOUNTS[AMOUNTS.index(amount_value) + 1]
                        print("next_amount:", next_amount)
                        for number in str(next_amount):
                            numeric_button = wait_for_element(base % NUMBERS[number])
                            if numeric_button:
                                numeric_button.click()
                                hand_delay()
                    else:  # reset to 1
                        # numeric_button = wait_for_element(base % NUMBERS['1'])
                        # if numeric_button:
                        #     numeric_button.click()
                        # hand_delay()
                        for number in str(INIT_AMOUNT):
                            numeric_button = wait_for_element(base % NUMBERS[number])
                            if numeric_button:
                                numeric_button.click()
                                hand_delay()
                closed_tab_parent.click()
            except Exception as e:
                print(e)
        IS_AMOUNT_SET = True

    if IS_AMOUNT_SET and (datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second) % PERIOD == 0:
        closes = list(stack.values())
        highs = [close + 0.5 for close in closes] # Mock highs with a small offset
        lows = [close - 0.5 for close in closes]  # Mock lows with a small offset

        ichimoku_values = calculate_ichimoku_elements(highs, lows, closes)
        if not ichimoku_values:
            return

        tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span = ichimoku_values

        if chikou_span > tenkan_sen:
            do_action('call')
        elif chikou_span <= tenkan_sen:
            do_action('put')

def websocket_log(stack):
    global CURRENCY, CURRENCY_CHANGE, CURRENCY_CHANGE_DATE, LAST_REFRESH, HISTORY_TAKEN, MODEL, INIT_DEPOSIT
    try:
        current_symbol = driver.find_element(by=By.CLASS_NAME, value='current-symbol').text
        if current_symbol != CURRENCY:
            CURRENCY = current_symbol
            CURRENCY_CHANGE = True
            CURRENCY_CHANGE_DATE = datetime.now()
    except:
        pass

    if CURRENCY_CHANGE and CURRENCY_CHANGE_DATE < datetime.now() - timedelta(seconds=5):
        if INIT_AMOUNT:  # Initialize with init_amount
            init_amount()

        if INIT_TIME_FRAME:  # Initialize with init_time_frame
            init_timeframe()
            
        stack = {}  # drop stack when currency changed
        HISTORY_TAKEN = False  # take history again
        driver.refresh()        
        CURRENCY_CHANGE = False
        MODEL = None
        INIT_DEPOSIT = None

    for wsData in driver.get_log('performance'):
        message = json.loads(wsData['message'])['message']
        response = message.get('params', {}).get('response', {})
        if response.get('opcode', 0) == 2 and not CURRENCY_CHANGE:
            payload_str = base64.b64decode(response['payloadData']).decode('utf-8')
            data = json.loads(payload_str)
            if not HISTORY_TAKEN:
                if 'history' in data:
                    stack = {int(d[0]): d[1] for d in data['history']}
                    print(f"History taken for asset: {data['asset']}, period: {data['period']}, len_history: {len(data['history'])}, len_stack: {len(stack)}")
            try:
                current_symbol = driver.find_element(by=By.CLASS_NAME, value='current-symbol').text
                symbol, timestamp, value = data[0]
            except:
                continue
            try:
                if current_symbol.replace('/', '').replace(' ', '') != symbol.replace('_', '').upper() and companies.get(current_symbol) != symbol:
                    continue
            except:
                pass

            if len(stack) == LENGTH_STACK_MAX:
                first_element = next(iter(stack))
                del stack[first_element]
            if len(stack) < LENGTH_STACK_MAX:
                if int(timestamp) in stack:
                    return stack
                else:
                    stack[int(timestamp)] = value
            elif len(stack) > LENGTH_STACK_MAX:
                print(f"Len > {LENGTH_STACK_MAX}!!")
                stack = {}
            if len(stack) >= LENGTH_STACK_MIN:
                check_values(stack)
    return stack

load_web_driver()
while True:
    STACK = websocket_log(STACK)
