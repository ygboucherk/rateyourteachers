import json, flask, eth_abi
from web3 import Web3, HTTPProvider
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["debug"] = False
w3 = Web3(HTTPProvider("https://rpc.raptorchain.io/"))
CORS(app)

class Grade(object):
    def __init__(self, infoDict=None, rater="", score=0):
        (self.score, self.rater, self.comment) = ((int(infoDict.get("score", 0)), infoDict.get("rater", "")) if self.infoDict else (score, rater), self.comment)

    def JSONSerializable(self):
        return {"score": self.score, "rater": self.rater, "comment": self.comment}

class Teacher(object):
    def __init__(self, file, initData=None):
        self.file = file
        if initData:
            self._load(initData)
        else:
            f = open(self.file, "r")
            self._load(json.load(file))
            f.close()
            
    def _load(self, initData):
        (self.name, self.grades) = (initData.get("name", ""), [Grade(infoDict=d) for d in initData.get("grades", [])])
        self.updateAverage()
        
    def updateAverage(self):
        gradesn = [g.score for g in self.grades]
        self.average = sum(gradesn) / len(gradesn)
    
    def save(self):
        serialized = json.dumps({"name": self.name, "grades": [g.JSONSerializable() for g in self.grades]})
        f = open(self.file, "w")
        f.write(serialized)
        f.close()
        
    def rate(self, rater, score):
        self.grades.append(Grade(rater=rater, score=score))
        self.updateAverage()
        self.save()
        
class Account(object):
    def __init__(self, file, initData=None):
        self.file = file
        if initData:
            self._load(initData)
        else:
            f = open(self.file, "r")
            self._load(json.load(file))
            f.close()

    def __init__(self, address):
        self.address = address
        self.ratedTeachers = []
        

class Core(object):
    class WriteRequest(object):
        def __init__(self, methodType, content, sig):
            self.content = content
            self.sig = sig
            self.hash = w3.keccak(self.content)
            self.signer = w3.eth.account.recoverHash(self.hash, signature=self.sig)
            
    class ReadRequest(object)
        self.content = content
        
    self.teachers = {}
    self.accounts = {}
    self.addrsListLocation = "addrs.dat"
    
    
    def load(self):
        f = open(self.addrsListLocation, "r")
        self.teachers = [Teacher(a) for a in f.read().splitlines()]
        f.close()
        
    
    def getAccount(self, address):
        _addr = w3.toChecksumAddress(address)
        if not self.accounts.get(_addr):
            self.accounts[]
    
@app.route("/write/grade")
def writeGrade():
    grade = flask.request.args.get("grade")
    teacher = flask.request.args.get("teacher")
    encoded = eth_abi.encode_abi(["string", "string", "uint256"], ["newGrade", teacher, int(grade)])
    sig = flask.request.args.get("sig")
    WriteRequest("newGrade", encoded, sig)
