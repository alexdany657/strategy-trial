from enum import Enum

class ProblemState(Enum):
    Running = 0
    Upsolving = 1
    Testing = 2

class StrategyState(Enum):
    Main = 0
    NonMain = 1

class StratrgyVerdict(Enum):
	Ok = 0
	IncorrectTurn = 1
	TimeLimitExceeded = 2
	Failed = 3

# definition of user

class User:
    def __init__(self, Id: int, username: str, password: str, submissions: list, results: dict):
        self.id = Id # id of user
        self.username = username # username of user
        self.password = password # password of user
        self.submissions = submissions # list of user's ids of submissions
        self.results = results # dict prob_id into result of user's strategies

# definition of problem

class Problem:
    def __init__(self, Id: int, name: str, rules: Rules, ttype: ProblemState, StartTime: int, EndTime: int, submissions: list, standings: list):
        self.id = Id # id of problem
        self.name = name # name of problem
        self.rules = rules # description of rules, interaction with strategy
        self.type = ttype # type (running/upsolving/testing)
        self.startTime = StartTime # time when users can send strategies
        self.endTime = EndTime # time when users stop sending strategies, time in milliseconds from 01.01.1970
        self.submissions = submissions #list of strategies' ids (startegies that will play with each other, selected by user)
        self.standings = standings # standings: sortedby score list of results of all strategies

class Rules:
    def __init__(self, ProbId: int, GamePath, text: str):
        self.probId = ProbId # id of problem
        self.gamePath = GamePath # path on server to the class game that discribes interacting user's strategy with judge(TODO may be not needed)
        self.text = text # text needed to be published

class Result:
    def __init__(self, SubId: int, Verdict: StratrgyVerdict, Score: int):
        self.verdict = Verdict # is this strategy working correct, or it gets TL, WA or RE?
        self.score = Score # points, which the strategy has got

# defination of submission

class Submission:
    def __init__(self, Id: int, UserId: int, ProbId: int, path: str, ttype: StrategyState, result: Result):
        self.id = Id # id of submission
        self.userId = UserId # id of owner
        self.probId = ProbId # id of problem that it solves
        self.type = ttype # type of strategy (e.g. main or nonmain)
        self.result = result # result of strategy

