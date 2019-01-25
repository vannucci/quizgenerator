import json
from random import randrange
from string import Template
import datetime
import click



def shuffle_gen(n):
  state = dict()
  for remaining in range(n, 0, -1):
    i  = randrange(remaining)
    yield state.get(i,i)
    state[i] = state.get(remaining - 1, remaining - 1)
    state.pop(remaining - 1, None)

@click.command()
@click.option('--length', default=3, help='Length of quiz in number of questions')
@click.option('--title', default='Untitled', help='Title of quiz')
@click.option('--subtitle', default='', help='Subtitle of quiz')
def quizgenerator(length = 3,title = 'Untitled',subtitle = ''):

  questionbank,topics = [],''
  questionlist = []
  nowdate = datetime.datetime.now()
  formattedquestionlist = None
  sources = [{'book': 'TADM', 'chapterNo': '3'},{'book': 'TADM', 'chapterNo': '2'}]


  with open('questionbank.json') as json_file:
    data = json.load(json_file)
    for source in sources:
      questionbank.extend(data[source['book']]['chapters'][source['chapterNo']]['questions'])
      topics += ' '.join(data[source['book']]['chapters'][source['chapterNo']]['topics'])

  if(length <= len(questionbank)):
    gen = shuffle_gen(len(questionbank))
    for _ in range(length):
      print()
      questionlist.append(questionbank[next(gen)])
      formattedquestionlist = '\n\n1. ' + '\n\n1. '.join(questionlist)
  else:
    print(f'Number of questions requested exceeds size of question bank, requested: {length}, available: {len(questionbank)}')

  quizobject = { 'title':title, 'subtitle': subtitle, 'topics': topics, 'questionlist': formattedquestionlist }

  with open( 'quiztemplate.md' ) as quizfile:
    src = Template( quizfile.read() )

  finalresult = src.substitute(quizobject)

  try:
    with open(f'{quizobject["title"]} {nowdate.month}-{nowdate.day}.md', 'x') as destinationfile:
      destinationfile.write(finalresult)
  except FileExistsError:
      print(f'File \'{quizobject["title"]} {nowdate.month}-{nowdate.day}.md\' already exists. Please remove it and try again')

if __name__ == '__main__':
  quizgenerator()