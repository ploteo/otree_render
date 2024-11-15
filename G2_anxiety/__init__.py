from otree.api import *


doc = """
NOTE: to compute the final grade and payoffs
NOTE: understand the grading system
"""


class C(BaseConstants):
    NAME_IN_URL = 'G2_anxiety'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 15
    TIMEOUT = 60*.1
    CORRECT_ANSWERS = [1, 4, 3, 1, 6, 1, 8, 7, 6, 2, 1, 6, 7, 2, 3]
    TIMEOUT_PRESSURE = 10
    TIMEOUT_NO_PRESSURE = 100

    # IMAGE CODING
    # 1 = EASY A1
    # 2 = EASY A4
    # 3 = EASY A3
    # 4 = EASY A1
    # 5 = EASY A6
    # 6 = EASY A1
    # 7 = EASY A8
    # 8 = MED A7
    # 9 = MED A6
    # 10 = MED A2
    # 11 = MED A1
    # 12 = MED A6
    # 13 = MED A7
    # 14 = DIFF A2
    # 15 = DIFF A3


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        if p.id_in_subsession % 2 == 0:
            p.condition = "pressure"
        else:
            p.condition = "no_pressure"

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    condition = models.StringField()
    confidence = models.IntegerField(min=0, max=5)
    overestimate = models.StringField()
    gender_influence = models.StringField()
    gender_overconfident = models.StringField(blank=True)
    grade = models.IntegerField(min=18, max=30, initial=0)
    points = models.IntegerField()
    response = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], widget=widgets.RadioSelectHorizontal)
    correct = models.BooleanField()
    accept = models.BooleanField(initial=0) # 1 = accept, 0 = reject



# PAGES
class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Overconfidence(Page):
    form_model = 'player'
    form_fields = ['confidence', 'overestimate','gender_influence','gender_overconfident', 'grade']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Raven_instr(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time

        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + C.TIMEOUT

class Raven(Page):
    form_model = 'player'
    form_fields = ['response']

    timer_text = 'Time left to complete the tasks:'
    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant
        import time
        return participant.expiry - time.time()
    @staticmethod
    def vars_for_template(player):
        return dict(
            image_path='{}.png'.format(player.round_number)
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.response = -99
        player.correct = player.response == C.CORRECT_ANSWERS[player.round_number - 1]
        player.points = 3 if player.correct else 0

        # Retrieve grade from the previous round
        if player.round_number > 1:
            previous_round = player.in_round(player.round_number - 1)
            player.grade = previous_round.grade + player.points
        else:
            player.grade = player.points

class Info(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

class Choice(Page):
    form_model = 'player'
    form_fields = ['accept']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    #add a timer
    timer_text = 'Time left to choose:'
    @staticmethod
    def get_timeout_seconds(player):
        if player.condition == "pressure":
            return C.TIMEOUT_PRESSURE
        else:
            return C.TIMEOUT_NO_PRESSURE

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Welcome, Overconfidence, Raven_instr,Raven,Info,Choice]
