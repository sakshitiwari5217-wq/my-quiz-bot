import os
import random
import telebot
import time
import threading

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

active_groups = set()

quiz_data = {
    "Physics": [
        "Q1: Unit of force?\n(A) Joule (B) Newton (C) Watt (D) Pascal\nAns: (B)",
        "Q2: Light year is unit of?\n(A) Time (B) Distance (C) Speed (D) Light\nAns: (B)",
        "Q3: Dimensional formula for Energy?\n(A) MLT^-2 (B) ML^2T^-2 (C) MLT^-1 (D) ML^2T^-1\nAns: (B)",
        "Q4: Speed of light in vacuum?\n(A) 3x10^8 m/s (B) 3x10^6 m/s (C) 2x10^8 m/s (D) 3x10^5 m/s\nAns: (A)",
        "Q5: Ohm's law relates?\n(A) I, R, Q (B) V, I, R (C) V, I, t (D) P, V, I\nAns: (B)",
        "Q6: Kinetic Energy formula?\n(A) mgh (B) 1/2mv^2 (C) ma (D) Fd\nAns: (B)",
        "Q7: Value of 'g' on earth?\n(A) 9.8 m/s^2 (B) 8.9 m/s^2 (C) 10.5 m/s^2 (D) 9.0 m/s^2\nAns: (A)",
        "Q8: Work is?\n(A) Vector (B) Scalar (C) Tensor (D) None\nAns: (B)",
        "Q9: Frequency unit?\n(A) Hertz (B) Second (C) Meter (D) Newton\nAns: (A)",
        "Q10: Heat unit?\n(A) Calorie (B) Watt (C) Volt (D) Ampere\nAns: (A)",
        "Q11: Power unit?\n(A) Joule (B) Watt (C) Newton (D) Pascal\nAns: (B)",
        "Q12: Pressure unit?\n(A) Newton (B) Joule (C) Pascal (D) Watt\nAns: (C)",
        "Q13: Density formula?\n(A) Mass/Vol (B) Vol/Mass (C) F/A (D) Work/t\nAns: (A)",
        "Q14: 1 HP = ?\n(A) 746 W (B) 700 W (C) 1000 W (D) 500 W\nAns: (A)",
        "Q15: Newton's 1st law defines?\n(A) Force (B) Inertia (C) Energy (D) Momentum\nAns: (B)",
        "Q16: Impulse is?\n(A) Force x time (B) Force/time (C) mass x acc (D) Work x time\nAns: (A)",
        "Q17: Surface tension unit?\n(A) N/m (B) N/m^2 (C) Joule (D) Watt\nAns: (A)",
        "Q18: Which is vector?\n(A) Mass (B) Velocity (C) Time (D) Distance\nAns: (B)",
        "Q19: Centrifugal force acts?\n(A) Inward (B) Outward (C) Tangent (D) None\nAns: (B)",
        "Q20: Escape velocity on earth?\n(A) 11.2 km/s (B) 9.8 km/s (C) 5 km/s (D) 3 km/s\nAns: (A)"
    ],
    "Chemistry": [
        "Q1: Water formula?\n(A) HO2 (B) H2O (C) H2O2 (D) OH\nAns: (B)",
        "Q2: Atomic number of Carbon?\n(A) 5 (B) 6 (C) 7 (D) 8\nAns: (B)",
        "Q3: pH of neutral solution?\n(A) 0 (B) 7 (C) 14 (D) 1\nAns: (B)",
        "Q4: Metal liquid at room temp?\n(A) Gold (B) Silver (C) Mercury (D) Iron\nAns: (C)",
        "Q5: Noble gas?\n(A) Nitrogen (B) Oxygen (C) Helium (D) Hydrogen\nAns: (C)",
        "Q6: Proton charge?\n(A) +1 (B) -1 (C) 0 (D) +2\nAns: (A)",
        "Q7: Electron mass is?\n(A) High (B) Negligible (C) Zero (D) Infinity\nAns: (B)",
        "Q8: Symbol of Gold?\n(A) Ag (B) Au (C) Fe (D) Cu\nAns: (B)",
        "Q9: Rusting of iron is?\n(A) Reduction (B) Oxidation (C) Neutral (D) None\nAns: (B)",
        "Q10: Strongest acid?\n(A) HCl (B) HF (C) HI (D) HBr\nAns: (C)",
        "Q11: Atomic number of Oxygen?\n(A) 6 (B) 7 (C) 8 (D) 9\nAns: (C)",
        "Q12: Isotope of Hydrogen?\n(A) Deuterium (B) Carbon (C) Nitrogen (D) Oxygen\nAns: (A)",
        "Q13: Common Salt?\n(A) KCl (B) NaCl (C) MgCl (D) CaCl\nAns: (B)",
        "Q14: Valence shell?\n(A) 1st (B) Inner (C) Outer (D) Middle\nAns: (C)",
        "Q15: CO2 is?\n(A) Acidic (B) Basic (C) Neutral (D) None\nAns: (A)",
        "Q16: Catalyst?\n(A) Speeds up reaction (B) Stops it (C) Neutral (D) None\nAns: (A)",
        "Q17: Avogadro number?\n(A) 6.022x10^23 (B) 6.022x10^10 (C) 3x10^8 (D) 9.1x10^-31\nAns: (A)",
        "Q18: Hardest substance?\n(A) Iron (B) Diamond (C) Gold (D) Graphite\nAns: (B)",
        "Q19: Chemical name of baking soda?\n(A) Sodium Carbonate (B) Sodium Bicarbonate (C) NaCl (D) NaOH\nAns: (B)",
        "Q20: Nitrogen valency?\n(A) 1 (B) 2 (C) 3 (D) 4\nAns: (C)"
    ],
    "Biology": [
        "Q1: Powerhouse of cell?\n(A) Nucleus (B) Mitochondria (C) Ribosome (D) Lysosome\nAns: (B)",
        "Q2: DNA shape?\n(A) Helix (B) Round (C) Square (D) Flat\nAns: (A)",
        "Q3: RBC life?\n(A) 120 days (B) 50 days (C) 200 days (D) 10 days\nAns: (A)",
        "Q4: Plant cell wall made of?\n(A) Chitin (B) Cellulose (C) Protein (D) Lipid\nAns: (B)",
        "Q5: Master gland?\n(A) Thyroid (B) Pituitary (C) Adrenal (D) Pancreas\nAns: (B)",
        "Q6: Blood clotting vitamin?\n(A) A (B) B (C) C (D) K\nAns: (D)",
        "Q7: Normal human pulse rate?\n(A) 72/min (B) 100/min (C) 50/min (D) 120/min\nAns: (A)",
        "Q8: Chlorophyll contains?\n(A) Iron (B) Magnesium (C) Calcium (D) Zinc\nAns: (B)",
        "Q9: Largest organ?\n(A) Skin (B) Heart (C) Liver (D) Lungs\nAns: (A)",
        "Q10: Basic unit of life?\n(A) Tissue (B) Cell (C) Organ (D) Bone\nAns: (B)",
        "Q11: Insulin is produced in?\n(A) Liver (B) Pancreas (C) Kidney (D) Stomach\nAns: (B)",
        "Q12: Number of chambers in human heart?\n(A) 2 (B) 3 (C) 4 (D) 1\nAns: (C)",
        "Q13: Vitamin C source?\n(A) Meat (B) Citrus fruit (C) Milk (D) Grain\nAns: (B)",
        "Q14: Who discovered cells?\n(A) Hooke (B) Darwin (C) Mendel (D) Einstein\nAns: (A)",
        "Q15: Father of Genetics?\n(A) Darwin (B) Mendel (C) Hooke (D) Watson\nAns: (B)",
        "Q16: Human chromosomes?\n(A) 46 (B) 23 (C) 48 (D) 50\nAns: (A)",
        "Q17: Protein building block?\n(A) Amino acid (B) Fat (C) Sugar (D) Vitamin\nAns: (A)",
        "Q18: Which blood group is universal donor?\n(A) A (B) B (C) AB (D) O\nAns: (D)",
        "Q19: Lungs functional unit?\n(A) Alveoli (B) Bronchi (C) Trachea (D) Neuron\nAns: (A)",
        "Q20: Process of making food in plants?\n(A) Respiration (B) Photosynthesis (C) Digestion (D) None\nAns: (B)"
    ]
}

@bot.message_handler(commands=['startquiz'])
def start_quiz(message):
    active_groups.add(message.chat.id)
    bot.reply_to(message, "NEET Quiz started! You will get a question every 10 minutes.")

def send_quiz():
    while True:
        if active_groups:
            subject = random.choice(list(quiz_data.keys()))
            question = random.choice(quiz_data[subject])
            for gid in list(active_groups):
                try:
                    bot.send_message(gid, f"NEET Quiz: {subject}\n\n{question}")
                except:
                    active_groups.discard(gid)
        time.sleep(600)

threading.Thread(target=send_quiz, daemon=True).start()
bot.polling()
              
