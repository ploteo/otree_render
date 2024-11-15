import random
from otree.api import *


doc = """
rounds 1-4 treated with different info; rounds 5-10 the make an investment choice

TODO: when does the news happen? before the investment choice or after?
TODO: The values of the two stocks are not realistic, same expected 
TODO: Work on feedback and computation of the payoff

"""


class C(BaseConstants):
    NAME_IN_URL = 'G4_confirmation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10
    #------------------------------------------------
    # the return and standard deviation of the two assets
    A_value = [22, 24, 27, 29, 28, 30, 29, 31, 32, 30]
    B_value = [22, 25, 29, 31, 27, 34, 29, 35, 31, 30 ]
    #------------------------------------------------
    # INFO GIVEN TO THE GROUPS (should be the same after round 5)
    info_risky = [["Analysts are impressed by Option B’s rapid growth potential, noting it has recently delivered impressive returns. This option attracts investors looking for strong, short-term gains.","According to financial reports, Option B is an exciting choice for high-reward seekers. With its dynamic performance, it’s positioned to provide excellent returns for those willing to embrace its higher risk."],
                  ["Economic forecasts show Option B as a top choice for growth, with analysts pointing to its potential for sizable gains. Investors seeking an edge in a dynamic market find Option B very appealing.","Market observers highlight Option B’s capacity for rapid value increase, making it ideal for investors aiming for substantial profit. Though it fluctuates, the potential for high returns draws interest."],
                  ["Investment specialists note Option B as a favored choice for high returns, even with its market swings. Those with a bold approach to investing may find it especially rewarding.","According to recent analysis, Option B is set to provide strong returns in growth-driven sectors. Investors who prioritize profits over stability are likely to benefit from its aggressive potential."],
                  ["Recent studies underscore Option B as a leading option for those open to higher risk, showing great promise in fast-growing markets. The payoff potential makes it highly attractive to growth-focused investors.""Reports suggest that Option B could be a prime choice for substantial gains in the near term, despite its fluctuations. It’s ideal for investors who are prepared to accept risk for the chance of higher returns."]              
                  ]
    info_safe = [
            ["Analysts describe Option A as a safe and stable investment, providing peace of mind to cautious investors. Its steady returns make it a strong choice for those who avoid market turbulence.","According to experts, Option A’s low-risk profile suits investors who prioritize financial security. With its consistent performance, Option A is favored by those who prefer gradual, reliable growth."], 
            ["Economic forecasts highlight Option A as a resilient choice, ideal for those seeking to minimize risk exposure. Its stability makes it an excellent option for conservative investors.","Market evaluations show that Option A stands out for its dependability, offering investors protection against major market changes. This option suits those looking to secure their investments long-term."],
            ["Reports indicate Option A’s steady growth trajectory, which reassures investors aiming for predictable, long-term returns. Those cautious of volatility will appreciate its low-risk approach.","Financial experts emphasize Option A’s consistency in value, making it a favorite for those who avoid high-risk assets. Its reliability in uncertain markets appeals to security-focused investors."],
            ["Analysis confirms Option A as a stable choice, with minimal fluctuations and steady returns, appealing to investors who prioritize low-risk growth over high returns.","Recent reviews underscore Option A’s reputation for stability, making it the preferred choice for those seeking a safe investment. It’s particularly suitable for individuals who value protection over rapid growth."]
                    ]
    info_ctrl = [
        ["Analysts commend Option A for its stability, showing steady growth with minimal risk, appealing to cautious investors. In comparison, Option B has had significant fluctuations.","Experts predict that Option B could bring high returns, offering exciting growth potential. However, Option A provides only stable returns, which may not satisfy investors seeking higher gains."],
        ["Recent reports confirm Option A as a safe, reliable choice for investors who prioritize steady returns. Meanwhile, Option B’s high volatility could lead to losses during downturns.","Market analysts highlight Option B as a strong choice for growth-focused investors. By contrast, Option A offers security but lacks the high-reward potential that some investors look for."],
        ["Economic advisors point to Option A as a dependable option that performs consistently without major swings. In contrast, Option B has shown unpredictable changes, which might deter those seeking stability.", "Reports highlight Option B as an option for those looking to maximize returns through a higher-risk approach as can be seen from the recent explosion of price. Option A offers stability, but its growth is slower, appealing mainly to those focused on safety over rapid profit."],
        ["Analysts recommend Option A for its resilience and low-risk profile, fitting for investors aiming for stable, secure returns. Conversely, Option B has shown considerable volatility, which may be challenging for those who prefer predictable outcomes.","Forecasts suggest that Option B may deliver higher returns for investors who accept more risk despite recent drops. Meanwhile, Option A remains a relatively stable choice, but it may not provide the substantial profits that investors desire."],
        ["Current studies show Option A as a secure choice for avoiding market risk, ideal for investors looking to protect their assets. However, Option B remains highly volatile, posing a risk of loss for the more cautious.","Market predictions favor Option B for its potential to yield significant profits in favorable conditions. On the other hand, Option A may limit growth potential for those seeking substantial gains."],
        ["Experts confirm Option A as a steady choice for conservative investors, offering predictable returns without large fluctuations. Meanwhile, Option B carries substantial risk with its frequent market swings, which may not suit those preferring a safer approach.","Analysts suggest Option B could achieve strong growth for investors open to risk, making it an appealing option for high returns despite recent decreases. In contrast, Option A’s growth remains steady but limited, catering to those focused on low-risk investments."]
        ]
    #------------------------------------------------
    


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    condition = models.CharField() # in which condition the player is
    investment_A = models.IntegerField() # if the player chooses A
    ret_A = models.FloatField() # return of asset A
    ret_B = models.FloatField() # return of asset B
    confidence = models.IntegerField(choices=range(1,8,1),widget=widgets.RadioSelectHorizontal) # how confident the player is
    returns = models.FloatField() # the returns of the player

# FUNCTIONS

def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        if p.id_in_subsession % 3 == 0:
            p.condition = "risky"
        elif p.id_in_subsession % 3 == 1:
            p.condition = "safe"
        else:
            p.condition = "ctrl"

# compute the payoffs
def compute_payoffs(player: Player):
    player.payoff = player.investment_A*100

# PAGES
class Welcome(Page):
    pass

class Investment_info(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class News(Page):
    pass

class Choice(Page):
    form_model = 'player'
    form_fields = ['investment_A']
    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number < 5:
            if player.condition == "risky":
                return dict(
                    news_1 = C.info_risky[player.round_number-1][0],
                    news_2 = C.info_risky[player.round_number-1][1]
                )
            elif player.condition == "safe":
                return dict(
                    news_1 = C.info_safe[player.round_number-1][0],
                    news_2 = C.info_safe[player.round_number-1][1]
                )
            else:
                return dict(
                    news_1 = "",
                    news_2 = ""
                )
        else:
            return dict(
                news = C.info_ctrl[player.round_number-5] # the same for all players
            )
            
    def before_next_page(player: Player, timeout_happened):
        compute_payoffs(player)
        print(player.payoff)
        #player.payoff=player.investment_A*(1+player.ret_A)+(100-player.investment_A)*(1+player.ret_B)

class Confidence(Page):
    form_model = 'player'
    form_fields = ['confidence']
    def vars_for_template(player: Player):
        inv_A = player.investment_A
        inv_B = 100 - player.investment_A
        return dict(
            inv_A = inv_A,
            inv_B = inv_B
        )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        inv_A = player.investment_A
        inv_B = 100 - player.investment_A
        return dict(
            inv_A = inv_A,
            inv_B = inv_B,
            value_A = C.A_value[player.round_number-1],
            value_B = C.A_value[player.round_number-1],
            payoff = player.payoff
        )


page_sequence = [Welcome, Investment_info, Choice, Confidence, Results]
