import json
from random import randint
from string import Template
import datetime
import mistune

def quizgenerator(numberofquestions = 3,title = "Default",subtitle = "Default subtitle"):

  questionbank,topics = None,"None"
  questionlist = []
  nowdate = datetime.datetime.now()
  formattedquestionlist = None


  with open('questionbank.json') as json_file:
    data = json.load(json_file)
    questionbank = data["TADM"]["chapters"]["3"]["questions"]
    topics = ' '.join(data["TADM"]["chapters"]["3"]["topics"])

  if(numberofquestions <= len(questionbank)):
    for _ in range(numberofquestions):
      questionlist.append(questionbank[randint(0,len(questionbank)-1)])
      formattedquestionlist = '\n\n1. ' + '\n\n1. '.join(questionlist)
  else:
    print(f"Number of questions requested exceeds size of question bank, requested: {numberofquestions}, available: {len(questionbank)}")

  quizobject = { 'title':title, 'subtitle': subtitle, "topics": topics, "questionlist": formattedquestionlist }

  with open( 'quiztemplate.md' ) as quizfile:
    src = Template( quizfile.read() )

  finalresult = src.substitute(quizobject)

  with open(f'{quizobject["title"]} {nowdate.month}-{nowdate.day}.md', "x") as destinationfile:
    destinationfile.write(finalresult)

quizgenerator()