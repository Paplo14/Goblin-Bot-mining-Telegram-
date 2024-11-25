#pylint:disable=W0127
import requests
import json
from colorama import Fore, init
from datetime import datetime
import time
import random
# تهيئة colorama
init(autoreset=True)
from time import sleep
from rich.console import Console
from rich.progress import Spinner

console = Console()
import subprocess
import sys
import importlib.util

# قائمة المكتبات المطلوبة
libraries = ["requests", "colorama", "rich"]

def is_library_installed(library_name):
    """تحقق إذا كانت المكتبة مثبتة."""
    return importlib.util.find_spec(library_name) is not None

def install_libraries():
    for library in libraries:
        if is_library_installed(library):
            print(f"✅ {library} is already installed.")
        else:
            try:
                print(f"🔄 Installing {library}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", library])
                print(f"✅ {library} installed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {library}. Error: {e}")




    
def wait_with_random_delay(message: str = "Processing your request..."):
    """
    دالة انتظار احترافية بوقت عشوائي بين 40 و60 ثانية.
    
    Args:
    message (str): الرسالة التي تظهر أثناء الانتظار.
    """
    # اختيار وقت عشوائي بين 40 و60 ثانية
    delay = random.randint(120, 200)
    
    with console.status(f"[bold cyan]{message}", spinner="dots") as status:
        for i in range(delay):
            sleep(1)  # انتظار لمدة ثانية واحدة
            status.update(f"[bold green]{message} ({i+1}/{delay} seconds)")
    
    console.print(f"[bold magenta]Done! Total wait time: {delay} seconds.[/bold magenta]")

# استخدام الدالة






def get_user_agent():
    return "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36 Telegram-Android/11.2.2 (Xiaomi M1908C3JGG; Android 12; SDK 31; AVERAGE)"

def read_init_data(file_path='data.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()

# دالة تسجيل الدخول

def login(intdata):
    # القيم الافتراضية للمحاولات والتأخير
    max_retries = 20
    delay = 10

    url = "https://api.goblinmine.game/graphql"
    payload = {
        "operationName": "login",
        "variables": {
            "input": {
                "initData": intdata
            }
        },
        "query": "mutation login($input: LoginInput!) {\n  login(input: $input) {\n    status\n    token\n    user {\n      id\n      first_name\n    }\n  }\n}"
    }
    headers = {
        'User-Agent': f"{get_user_agent()}",
        'Content-Type': "application/json",
        'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
        'accept-language': "en",
        'sec-ch-ua-mobile': "?1",  
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://game.goblinmine.game",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://game.goblinmine.game/"
    }
    
    retries = 0  # عدد المحاولات
    while retries < max_retries:
        print(Fore.BLUE + f"Attempting login... Attempt {retries + 1}/{max_retries}")
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "login" in data["data"]:
                token = data["data"]["login"]["token"]
                first_name = data["data"]["login"]["user"]["first_name"]
                print(Fore.GREEN + f"Login Successful! Token: {token} | User: {first_name}")
                return token, first_name
        # إذا فشلت المحاولة
        print(Fore.RED + f"Login failed. Retrying... ({retries + 1}/{max_retries})")
        retries += 1
        time.sleep(delay)  # الانتظار لمدة delay ثانية قبل المحاولة التالية
    
    # إذا لم يتم العثور على التوكين بعد المحاولات
    print(Fore.RED + "Login failed after multiple attempts.")
    return None, None

# اختبار الدالة مع بيانات تمثيلية

# استدعاء الدالة مباشرة مع بيانات المستخدم




def init_game_request(token):
    """
    ترسل طلب initGame إلى API وتتحقق من حالة الرد.
    """
    # تعريف الرابط
    url = "https://api.goblinmine.game/graphql"
    
    # إعداد الـ payload
    payload = {
        "operationName": "initGame",
        "variables": {
            "input": {
                "worldId": 1,
                "amount": 10000,
                "bombAmount": 2
            }
        },
        "query": "mutation initGame($input: StartGameInput) {\n  initGame(input: $input) {\n    active\n    amount\n    balance\n    bombs\n    gameFields\n    max\n    maxBomb\n    message\n    min\n    minBomb\n    resultFields\n    status\n    coefficients {\n      bombs\n      coefficients\n      __typename\n    }\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    }
    
    # إعداد الترويسة
    headers = {
        'User-Agent': f"{get_user_agent}",
        'Content-Type': "application/json",
        'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
        'accept-language': "en",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://game.goblinmine.game",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://game.goblinmine.game/"
    }
    
    try:
        # إرسال الطلب
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response_data = response.json()  # تحويل الرد إلى JSON
        
        # استخراج الحالة
        status = response_data.get("data", {}).get("initGame", {}).get("status")
        
        if status == "ok":
            print(Fore.GREEN +"Done Created Game")
        else:
            print(Fore.RED +f"Game creation failed with status: {status}")
    except Exception as e:
        print(f"Error: {e}")

# مثال لاستدعاء الدالة
# token = "ضع التوكن الخاص بك هنا"
# init_game_request(token)






def send_requests_with_delay(token):
    """
    ترسل طلبات إلى URL معين بفاصل زمني محدد مع التحقق من الحالة.
    """
    # تعريف الرابط والترويسة
    url = "https://api.goblinmine.game/graphql"
    headers = {
        'User-Agent': f"{get_user_agent}",
        'Content-Type': "application/json",
        'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
        'accept-language': "en",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://game.goblinmine.game",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://game.goblinmine.game/"
    }
    
    # إعداد عدد الطلبات والفاصل الزمني
    total_requests = 1
    delay = 20

    # متغير لتخزين حالة الفوز
    won = False

    # قائمة لتخزين الأرقام العشوائية المستخدمة
    used_numbers_list = []

    for i in range(total_requests):
        # توليد رقم عشوائي بين 1 و 22 وتجنب التكرار
        while True:
            random_index = random.randint(1, 22)
            if random_index not in used_numbers_list:
                used_numbers_list.append(random_index)
                break
        
        # إعداد الـ payload مع الرقم العشوائي
        payload = {
            "operationName": "select",
            "variables": {
                "input": {
                    "index": random_index,
                    "worldId": 1
                }
            },
            "query": "mutation select($input: SelectGameInput) {\n  select(input: $input) {\n    fields\n    message\n    resultSector\n    status\n    __typename\n  }\n}"
        }
        
        try:
            # إرسال الطلب
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response_data = response.json()  # تحويل الرد إلى JSON
            
            # استخراج الحالة
            status = response_data.get("data", {}).get("select", {}).get("status")
            
            if status == "win":
                won = True  # تعيين الحالة إلى فوز إذا كانت النتيجة "win"
                print(Fore.GREEN +"You win")
            else:
                print(Fore.RED +"You lose")
                break  # التوقف عن إرسال الطلبات إذا كانت النتيجة "lose"
        
        except Exception as e:
            print(f"Error: {e}")
            break  # إيقاف الحلقة في حالة وجود خطأ
        
        # الانتظار إذا لم يكن آخر طلب
        if i < total_requests - 1:
            time.sleep(delay)

    # إرسال cashOut فقط إذا كانت النتيجة "win" بعد انتهاء الحلقة
    if won:
        print("Win Bom")
        # إرسال طلب CashOut بعد انتهاء الحلقة إذا كانت النتيجة فوز
        cash_out_response = cashOut(token)
        print(f"CashOut Response: {cash_out_response}")

def cashOut(token):
    """
    إرسال طلب cashOut بعد انتهاء الطلبات السابقة.
    """
    url = "https://api.goblinmine.game/graphql"
    headers = {
        'User-Agent': f"{get_user_agent}",
        'Content-Type': "application/json",
        'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
        'accept-language': "en",
        'sec-ch-ua-mobile': "?1",
        'authorization': f"Bearer {token}",
        'sec-ch-ua-platform': "\"Android\"",
        'origin': "https://game.goblinmine.game",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://game.goblinmine.game/"
    }

    payload = {
        "operationName": "cashOut",
        "variables": {
            "worldId": 1
        },
        "query": "mutation cashOut($worldId: Int!) {\n  cashOut(worldId: $worldId) {\n    amount\n    balance\n    fields\n    message\n    resultSector\n    status\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # تحويل الرد إلى JSON لاستخراج amount
    response_data = response.json()
    
    # استخراج amount
    amount = response_data.get('data', {}).get('cashOut', {}).get('amount', 'No amount found')
    
    # طباعة amount أو اتخاذ إجراء بناءً عليها
    #print(f"CashOut Amount: {amount}")
    
    # إرجاع amount في حال الحاجة لاستخدامه لاحقًا
    return amount



def get_bronze_world_balance(token):
    url = "https://api.goblinmine.game/graphql"

    # بيانات الطلب
    payload = json.dumps({
        "operationName": "worlds",
        "variables": {},
        "query": """
        query worlds {
          worlds {
            active
            icon
            income_day
            name
            id
            currency {
              ...CURRENCY_FRAGMENT
              __typename
            }
            __typename
          }
        }

        fragment CURRENCY_FRAGMENT on Currency {
          id
          amount
          coefficient
          icon
          name
          __typename
        }
        """
    })

    # الرؤوس (Headers)
    headers = {
  'User-Agent': f"{get_user_agent}",
  'Content-Type': "application/json",
  #'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    try:
        # إرسال الطلب
        response = requests.post(url, data=payload, headers=headers)

        # التحقق من الاستجابة
        if response.status_code == 200:
            data = response.json()
            worlds = data.get('data', {}).get('worlds', [])

            # المتغير لتخزين رصيد العالم البرونزي
            bronze_world_balance = None

            # تصفية العالم البرونزي حسب الاسم
            for world in worlds:
                name = world.get('name', "").lower()  # التأكد من أن الاسم موجود وتحويله إلى أحرف صغيرة
                currency = world.get('currency', {})
                amount = currency.get('amount')

                # إذا كان اسم العالم هو "Bronze world" وكان الرصيد موجودًا
                if name == "bronze world" and amount is not None:
                    bronze_world_balance = int(amount)
                    break  # الخروج بعد العثور على العالم البرونزي

            # إذا لم يتم العثور على الرصيد
            if bronze_world_balance is None:
                print("Bronze world not found or no amount available.")
                return 0  # قيمة افتراضية

            return bronze_world_balance  # إعادة الرصيد إذا تم العثور عليه

        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            print("Response Text:", response.text)
            return 0  # قيمة افتراضية عند فشل الطلب

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0  # قيمة افتراضية عند حدوث خطأ

# مثال على كيفية استدعاء الدالة


# استدعاء الدالة مع التوكن

def welcome_user(name, token):
    
    today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(Fore.CYAN + "===============================")
    print(Fore.GREEN + f"Welcome {name}!")
    
    print(Fore.YELLOW + f"Current Date and Time: {today}")
    print(Fore.YELLOW + f"Your access token is: {token}")
    print(Fore.YELLOW + "This script Made By Mr : Karim ")
    print(Fore.YELLOW + "Telegram channel 🔥 : https://t.me/YOU742 ")
    
    print(Fore.CYAN + "===============================")

set = 0
clm = ""

def set_mine_level():
    global set, clm  # استخدام المتغيرات العالمية
    # طلب مستوى المنجم من المستخدم
    set = int(input(Fore.BLUE + "Set Your Mine Level Goblin: "))

    # التحقق إذا كانت القيمة 5
    if set == 5:
        set = 13
    elif set == 6:
        set = 14
    elif set == 7:
        set = 15  
    elif set == 8:
        set = 16    
    else:
        set = set  # إذا لم تكن 5، ستبقى القيمة كما هي

    # طباعة القيمة النهائية
    print(Fore.GREEN + f"Final Mine Level Goblin: {set}")

    # طلب من المستخدم إذا كان يريد المطالبة
    clm = str(input(Fore.BLUE + "Claming Blance Only [y or n]: "))
    #bom = str(input(Fore.BLUE + " Playing Bom Game Risk  [y or n]: "))



# استدعاء الدالة لتحديث المتغيرات


# استدعاء دالة أخرى للوصول إلى المتغيرات

#set buy
def buy_mine(token):
    url = "https://api.goblinmine.game/graphql"
    payload = {
        "operationName": "buyMine",
        "variables": {
            "input": {
                "mineId": set
            }
        },
        "query": "mutation buyMine($input: BuyMineInput!) {\n  buyMine(input: $input) {\n    message\n    status\n  }\n}"
    }
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json",
    }

    # إرسال الطلب
    response = requests.post(url, json=payload, headers=headers)

    # معالجة الاستجابة
    try:
        data = response.json()
        if "data" in data and data["data"].get("buyMine") is not None:
            message = data["data"]["buyMine"]["message"]
            print(Fore.GREEN + f"BuyMine message: {message}")
        else:
            error_message = data.get("errors", [{"message": "Unknown error"}])[0]["message"]
            print(Fore.RED + f"Don Buy Mine")
    except ValueError:
        print(Fore.RED + "Error: Failed to parse JSON response.")
        print(Fore.RED + f"Response: {response.text}")






def CatchWork(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "mineAndMiners",
        "variables": {
            "mineId": set
        },
        "query": "query mineAndMiners($mineId: Int!) {\n  mine(mineId: $mineId) {\n    ...MINE_FRAGMENT\n    __typename\n  }\n  miners(mineId: $mineId) {\n    ...MINERS_FRAGMENT\n    __typename\n  }\n}\n\nfragment MINE_FRAGMENT on MineFool {\n  deposit_day\n  goblin_image\n  id\n  image\n  income_per_day\n  level\n  miner_amount\n  name\n  price\n  user_miners_count\n  volume\n  userMine {\n    auto\n    cart_level\n    deposit_day\n    deposit_day_default\n    extracted_amount\n    extracted_percent\n    id\n    income_hour\n    next_volume\n    updateIn\n    volume\n    updated_at\n    total_day\n    __typename\n  }\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  miningCurrency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  __typename\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}\n\nfragment MINERS_FRAGMENT on Miners {\n  available\n  id\n  level\n  name\n  price\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  minerLevel {\n    available\n    disabled\n    existInventoryLevel\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventoryLevel {\n      level\n      name\n      __typename\n    }\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
    })

    headers = {
  'User-Agent': f"{get_user_agent}",
  'Content-Type': "application/json",
  #'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # استخراج بيانات miners
        miners = data.get('data', {}).get('miners', [])
        
        # استخراج العناصر التي يكون فيها available = False داخل minerLevel
        unavailable_miners = []
        for miner in miners:
            miner_levels = miner.get('minerLevel', [])
            for level in miner_levels:
                if level.get('available') == False:
                    unavailable_miners.append(level)

        # كتابة IDs الخاصة بالـ miners غير المتاحين إلى ملف
        with open('firstbuy.txt', 'w') as file:
            for miner in unavailable_miners:
                file.write(f"{miner.get('id')}\n")

        print(f"تم استخراج وكتابة {len(unavailable_miners)} من miners غير المتاحين إلى الملف firstbuy.txt.txt'")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response")
    except KeyError:
        print("Unexpected data structure in response")




def get_user_mine_id(token):
    url = "https://api.goblinmine.game/graphql"
    
    payload = json.dumps({
        "operationName": "minesAndCheckTasksCompleted",
        "variables": {
            "worldId": 1
        },
        "query": "query minesAndCheckTasksCompleted($worldId: Int!) {\n  mines(worldId: $worldId) {\n    ...MINE_FRAGMENT\n    __typename\n  }\n  check_tasks_completed(worldId: $worldId)\n}\n\nfragment MINE_FRAGMENT on MineFool {\n  deposit_day\n  goblin_image\n  id\n  image\n  income_per_day\n  level\n  miner_amount\n  name\n  price\n  user_miners_count\n  volume\n  userMine {\n    auto\n    cart_level\n    deposit_day\n    deposit_day_default\n    extracted_amount\n    extracted_percent\n    id\n    income_hour\n    next_volume\n    updateIn\n    volume\n    updated_at\n    total_day\n    __typename\n  }\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  miningCurrency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  
