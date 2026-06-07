import telebot
import random
import threading
import time
import os

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

quiz_data = {
    "Bio": [
        {"q": "Functional unit of inheritance?", "opts": ["Gene", "DNA", "Cell", "RNA"], "ans": 0},
        {"q": "Powerhouse of the cell?", "opts": ["Nucleus", "Mitochondria", "Ribosome", "Golgi"], "ans": 1},
        {"q": "Which is a fat-soluble vitamin?", "opts": ["Vit C", "Vit B", "Vit A", "Vit B12"], "ans": 2},
        {"q": "Normal human blood pH?", "opts": ["6.4", "7.4", "8.4", "5.4"], "ans": 1},
        {"q": "Largest organ in human body?", "opts": ["Liver", "Skin", "Heart", "Brain"], "ans": 1},
        {"q": "Who proposed evolution theory?", "opts": ["Darwin", "Mendel", "Newton", "Einstein"], "ans": 0},
        {"q": "Basic structural unit of life?", "opts": ["Tissue", "Organ", "Cell", "System"], "ans": 2},
        {"q": "Insulin is produced in?", "opts": ["Liver", "Pancreas", "Kidney", "Stomach"], "ans": 1},
        {"q": "Number of chambers in heart?", "opts": ["2", "3", "4", "1"], "ans": 2},
        {"q": "Vitamin C source?", "opts": ["Meat", "Citrus fruit", "Milk", "Egg"], "ans": 1}
    ],
    "Phy": [
        {"q": "Unit of Force?", "opts": ["Joule", "Newton", "Watt", "Pascal"], "ans": 1},
        {"q": "Speed of light in vacuum?", "opts": ["3x10^8 m/s", "2x10^8 m/s", "3x10^6 m/s", "None"], "ans": 0},
        {"q": "Ohm's law relates?", "opts": ["I, R, V", "F, M, A", "W, F, D", "P, V, T"], "ans": 0},
        {"q": "Kinetic Energy formula?", "opts": ["mgh", "1/2mv^2", "mv", "ma"], "ans": 1},
        {"q": "Value of 'g' on earth?", "opts": ["9.8 m/s^2", "8.9 m/s^2", "10 m/s^2", "9 m/s^2"], "ans": 0},
        {"q": "Work is?", "opts": ["Vector", "Scalar", "Tensor", "None"], "ans": 1},
        {"q": "Frequency unit?", "opts": ["Hertz", "Joule", "Watt", "Second"], "ans": 0},
        {"q": "Heat unit?", "opts": ["Calorie", "Newton", "Watt", "Joule"], "ans": 0},
        {"q": "Power unit?", "opts": ["Joule", "Watt", "Newton", "Pascal"], "ans": 1},
        {"q": "Pressure unit?", "opts": ["Newton", "Pascal", "Joule", "Watt"], "ans": 1}
    ],
    "Chem": [
        {"q": "pH of neutral solution?", "opts": ["0", "7", "14", "1"], "ans": 1},
        {"q": "Water formula?", "opts": ["HO2", "H2O", "H2O2", "OH"], "ans": 1},
        {"q": "Atomic number of Carbon?", "opts": ["5", "6", "7", "8"], "ans": 1},
        {"q": "Metal liquid at room temp?", "opts": ["Gallium", "Mercury", "Sodium", "Gold"], "ans": 1},
        {"q": "Noble gas?", "opts": ["Nitrogen", "Oxygen", "Helium", "Hydrogen"], "ans": 2},
        {"q": "Proton charge?", "opts": ["+1", "-1", "0", "+2"], "ans": 0},
        {"q": "Electron mass is?", "opts": ["High", "Negligible", "Zero", "Same as proton"], "ans": 1},
        {"q": "Symbol for Gold?", "opts": ["Ag", "Au", "Fe", "Cu"], "ans": 1},
        {"q": "Most reactive metal?", "opts": ["Iron", "Gold", "Cesium", "Copper"], "ans": 2},
        {"q": "Valency of Oxygen?", "opts": ["1", "2", "3", "4"], "ans": 1}
    ]
}

active_groups = set()

@bot.message_handler(commands=['startquiz'])
def start_quiz(message):
    active_groups.add(message.chat.id)
    bot.reply_to(message, "✅ NEET Quiz started! You will receive a poll every 10 minutes.")

def quiz_loop():
    while True:
        time.sleep(600)
        if active_groups:
            subject = random.choice(list(quiz_data.keys()))
            question_data = random.choice(quiz_data[subject])
            for gid in list(active_groups):
                try:
                    bot.send_poll(gid, f"NEET Quiz: {subject}\n{question_data['q']}", question_data['opts'], type='quiz', correct_option_id=question_data['ans'], is_anonymous=False)
                except:
                    active_groups.discard(gid)

threading.Thread(target=quiz_loop, daemon=True).start()
bot.polling(none_stop=True)
