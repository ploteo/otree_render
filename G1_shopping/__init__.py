from otree.api import *


doc = """
TODO: I would give 5 seconds to both
TODO: Do you give feedback on the correct answer?
TODO: What are the incentives to report the number?
"""
import random


class C(BaseConstants):
    NAME_IN_URL = 'G1_shopping'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 11
    LONG = [random.randint(1000000, 9999999) for _ in range(10)]
    SHORT = [random.randint(100, 999) for _ in range(10)]
    TIMEOUT_SECONDS = 5
    PRICES = [1240, 105, 75, 900, 70, 970, 60, 230]


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
 #first randomization layer (stress game/no stress game)
    for p in subsession.get_players():
        if p.id_in_subsession % 2 == 0:
            p.condition = "stress"
        else:
            p.condition = "no_stress"
    #second randomization layer (priming/no priming)
    c_1=0
    c_2=0
    for p in subsession.get_players():
        if p.condition == "stress":
            c_1+=1
            if c_1 % 2 == 0:
                p.priming = "yes"
            else:
                p.priming = "no"
        else:
            c_2+=1
            if c_2 % 2 == 0:
                p.priming = "yes"
            else:
                p.priming = "no"


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #treatment variables
    priming = models.StringField()
    condition = models.StringField()
    # mood variables
    mood_1 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5], label='How stressed do you feel at this moment?')
    mood_2 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5], label='How sad do you feel right now?')
    mood_3 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5], label='How energetic do you feel right now?')
    mood_4 = models.IntegerField(widget=widgets.RadioSelect, choices=[1, 2, 3, 4, 5], label='How anxious do you feel right now?')
    # report variable
    report = models.IntegerField()
    correct = models.BooleanField()
    TOT_correct = models.IntegerField()
    # shopping variables
    shoe1 = models.BooleanField(initial=False, blank=True )
    shoe2 = models.BooleanField(initial=False, blank=True)
    shoe3 = models.BooleanField(initial=False, blank=True)
    shoe4 = models.BooleanField(initial=False, blank=True)
    shoe5 = models.BooleanField(initial=False, blank=True)
    shoe6 = models.BooleanField(initial=False, blank=True)
    shoe7 = models.BooleanField(initial=False, blank=True)
    shoe8 = models.BooleanField(initial=False, blank=True)



# PAGES
class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Mood(Page):
    form_model = 'player'
    form_fields = ['mood_1', 'mood_2', 'mood_3', 'mood_4']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Mood_2(Page):
    form_model = 'player'
    form_fields = ['mood_1', 'mood_2', 'mood_3', 'mood_4']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10

class Mood_3(Page):
    form_model = 'player'
    form_fields = ['mood_1', 'mood_2', 'mood_3', 'mood_4']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 11

class Display(Page): # Display the number
    @staticmethod
    def get_timeout_seconds(player: Player):
        return C.TIMEOUT_SECONDS
    
    
    def vars_for_template(player: Player):
        if player.condition == "stress":
            number = C.LONG[player.round_number - 1]
        else:
            number = C.SHORT[player.round_number - 1]

        html_code = ''.join(f'<span style="background-color: #000; color: #fff; padding: 10px; margin: 2px; font-size: 36px;">{digit}</span>' for digit in str(number))
        
        return dict(
                tab = html_code
            )
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= 10


class Report(Page):
    form_model = 'player'
    form_fields = ['report']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.condition == "stress":
            number = C.LONG[player.round_number - 1]
        else:
            number = C.SHORT[player.round_number - 1]

        if player.report == number:
            player.correct = True
        else:
            player.correct = False
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= 10
        

class ShopInfo(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10


class DisplayShoes(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.priming == "yes" and player.round_number == 10
    
    @staticmethod
    def get_timeout_seconds(player: Player):
        return C.TIMEOUT_SECONDS
    

class Shopping(Page):
    form_model = 'player'
    form_fields = ['shoe1', 'shoe2', 'shoe3', 'shoe4', 'shoe5', 'shoe6', 'shoe7', 'shoe8']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                prices_1 = C.PRICES[0],
                prices_2 = C.PRICES[1],
                prices_3 = C.PRICES[2],
                prices_4 = C.PRICES[3],
                prices_5 = C.PRICES[4],
                prices_6 = C.PRICES[5],
                prices_7 = C.PRICES[6],
                prices_8 = C.PRICES[7]
            )
    @staticmethod
    def get_timeout_seconds(player: Player):
        return 300
    @staticmethod
    # an error message will be displayed if the participant spends too much
    def error_message(player: Player, values):
        total_spent = sum([values['shoe1'] * C.PRICES[0], values['shoe2'] * C.PRICES[1], values['shoe3'] * C.PRICES[2], values['shoe4'] * C.PRICES[3], values['shoe5'] * C.PRICES[4], values['shoe6'] * C.PRICES[5], values['shoe7'] * C.PRICES[6], values['shoe8'] * C.PRICES[7]])
        if total_spent > 2000:
            return 'You have spent more than $2000. Please adjust your choices.'

class ResultsWaitPage(WaitPage):
    pass

class Results(Page): # not diplayed
    @staticmethod # to compute total correct answers
    def vars_for_template(player: Player):
        hist = player.in_all_rounds()
        player.TOT_correct = sum([g.correct for g in hist])
        return dict(
                TOT_correct = player.TOT_correct
            )

class End(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 11


page_sequence = [Welcome, Mood, Display, Report, Mood_2, ShopInfo, DisplayShoes, Shopping, Mood_3, End]
