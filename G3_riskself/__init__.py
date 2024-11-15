from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'G3_riskself'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 5
    #f each group has multiple roles, such as buyer/seller, principal/agent, etc., you can define them in constants. Make their names end with _ROLE:
    TRUSTOR_ROLE = 'Trustor'
    TRUSTEE_ROLE = 'Trustee'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def set_payoffs(group: Group):
    trustor = group.get_player_by_role("Trustor")
    trustee = group.get_player_by_role("Trustee")
    sent = trustor.send
    returned = [0,trustee.r_1, trustee.r_2, trustee.r_3, trustee.r_4, trustee.r_5, trustee.r_6, trustee.r_7, trustee.r_8, trustee.r_9, trustee.r_10][sent]
    trustor.payoff = 10 - sent + returned
    trustee.payoff = sent*3 - returned
    print(sent)
    print(returned)

class Player(BasePlayer):
    cards_flipped = models.IntegerField(min=0, max=32)
    bomb_position = models.IntegerField()
    bomb_found = models.BooleanField()
    TOT_payoff = models.CurrencyField()
    # trustor
    send = models.IntegerField(choices = range(0, 11, 1))
    # return
    r_1 = models.IntegerField()
    r_2 = models.IntegerField()
    r_3 = models.IntegerField()
    r_4 = models.IntegerField()
    r_5 = models.IntegerField()
    r_6 = models.IntegerField()
    r_7 = models.IntegerField()
    r_8 = models.IntegerField()
    r_9 = models.IntegerField()
    r_10 = models.IntegerField()


# PAGES

class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
class Welcome2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

class Cards(Page):
    form_model = 'player'
    form_fields = ['cards_flipped']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # check if they found a bomb and set the payoff (position the bomb randomly between 1 and 32) 
        player.bomb_position = random.randint(1, 32)
        if player.cards_flipped < player.bomb_position:
            player.bomb_found = False
            player.payoff = 5 + .25 * player.cards_flipped
        else:
            player.bomb_found = True
            player.payoff = 0

        if player.cards_flipped == 0:
            player.payoff = 0

class Cards_display(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
        cards_flipped=player.cards_flipped,
        bomb_position=player.bomb_position,
        bomb_found=player.bomb_found,
        payoff=player.payoff

    )
    @staticmethod
    def js_vars(player):
        return dict(
            cards_flipped=player.cards_flipped,
            bomb_position=player.bomb_position
        )

class Summary(Page):
    @staticmethod # to compute total correct answers
    def vars_for_template(player: Player):
        hist = player.in_all_rounds()
        player.TOT_payoff = sum([g.payoff for g in hist])
        return dict(
            TOT_payoff = player.TOT_payoff
            )
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

class ResultsWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

class Send(Page):
    form_model = 'player'
    form_fields = ['send']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
class Return(Page):
    form_model = 'player'
    form_fields = ['r_1','r_2','r_3','r_4','r_5','r_6','r_7','r_8','r_9','r_10']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):  
        amounts = [i * 3 for i in range(1, 11)]
        print(amounts)

        return dict(
            amounts=amounts
        )

class ResultsWaitPage2(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    @staticmethod # to compute total correct answers
    def vars_for_template(player: Player):
        trustor = player.group.get_player_by_role("Trustor")
        trustee = player.group.get_player_by_role("Trustee")
        sent = trustor.send
        returned = [0, trustee.r_1, trustee.r_2, trustee.r_3, trustee.r_4, trustee.r_5, trustee.r_6, trustee.r_7, trustee.r_8, trustee.r_9, trustee.r_10][sent]

        return dict(
            trustor_sent = sent,
            trustee_returned = returned,
            )
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    


page_sequence = [Welcome, Cards, Cards_display,Summary,ResultsWaitPage,Send,Return,ResultsWaitPage2, Results]
