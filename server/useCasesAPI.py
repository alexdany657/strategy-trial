from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.storage import storage
from server.tester import tournament, testStrategies
from server.tester import loadProblemDownloads as TesterLPD
from server.commonFunctions import stringTime
import json

def addSubmission(userId, problemId, code):
    user = storage.getUser(userId)
    newSubmission = Submission(-1, userId, problemId, code, StrategyState.NonMain)
    idOfNewSubmission = storage.saveSubmission(newSubmission)
    if (problemId not in user.submissions):
        user.submissions[problemId] = []
    user.submissions[problemId].append(idOfNewSubmission)
    storage.saveUser(user)
    return idOfNewSubmission

def changeMainSubmission(userId, subId):
    newMainSubmission = storage.getSubmission(subId)
    user = storage.getUser(userId)
    probId = newMainSubmission.probId
    problem = storage.getProblem(probId)
    for anotherSubmissionId in user.submissions[probId]:
        anotherSubmission = storage.getSubmission(anotherSubmissionId)
        if (anotherSubmission.type == StrategyState.Main):
            anotherSubmission.type = StrategyState.NonMain
            storage.saveSubmission(anotherSubmission)
            problem.submissions.remove(anotherSubmissionId)
    newMainSubmission.type = StrategyState.Main
    storage.saveSubmission(newMainSubmission)
    problem.submissions.add(subId)
    storage.saveProblem(problem)

def addUser(username, password):
    newUser = User(-1, username, password, UserType.Default, dict())
    idOfNewUser = storage.saveUser(newUser)
    return idOfNewUser

def getProblemset():
    return storage.getProblemset()

def getSubmissionsU(userId):
    return storage.getSubmissionListU(userId)

def getSubmissionsUP(userId, probId):
    return storage.getSubmissionListUP(userId, probId)

def makeTornament(probId):
    return tournament(probId)

def judge(id1, id2):
    return testStrategies(id1, id2, saveLogs = True)

def getSubmissionCode(subId):
    submission = storage.getSubmission(subId)
    if (submission is None):
        return ""
    else:
        return submission.code

def getProbTournaments(probId):
    lst = json.loads(storage.getCertainField('problems', probId, 'tournaments'))
    res = [
        {
            'id' : i + 1, 
            'tour_id' : lst[i], 
            'time' : stringTime(storage.getCertainField('tournaments', lst[i], 'time'))
        }
        for i in range(len(lst))
    ]
    return res

def getTournament(tourId):
    tournament = storage.getTournament(tourId)
    if (tournament is None):
        return None
    lst = []
    for i in range(len(tournament.standings)):
        position = tournament.standings[i]
        lst.append([i + 1, position[0],
            storage.getCertainField('users', position[1], 'username')])
    return {'time' : tournament.time, 'list' : lst}
