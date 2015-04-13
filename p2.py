from p2_game import Game, State
from collections import defaultdict

rounds = 10
wins = defaultdict(lambda: 0)


def runSim(redBot, blueBot):

  red_bot = __import__(redBot)
  blue_bot = __import__ (blueBot)

  BOTS = {'red': red_bot, 'blue': blue_bot}

  ################### End importing bot ##############################

  for i in range(rounds):

    print ""
    print "Round %d, fight!" % i

    game = Game(4)
    state = State(game)
    
    def make_quipper(who):
      def quip(what):
        print who, ">>", what
      return quip
    
    while not state.is_terminal():
      move = BOTS[state.whos_turn].think(state.copy(), make_quipper(state.whos_turn))
      state.apply_move(move)

    final_score = state.get_score()
    winner = max(['red','blue'],key=final_score.get)
    print "The %s bot wins this round! (%s)" % (winner, str(final_score))
    wins[winner] = 1 + wins[winner]

  print ""
  print "Final win counts:", dict(wins)

def default(str):
  return str + ' [Default: %default]'

if __name__ ==  '__main__':
  import sys

  # Use command line options
  from optparse import OptionParser
  usageStr = """
  USAGE:      python p2.py <options>
  EXAMPLES:   (1) python p2.py
                  - starts a game with two first_bot agents
              (2) python p2.py -r first_bot -b rollout_bot
                  - starts a fully automated game where the red agent uses first_bot and blue agent uses rollout_bot
  """
  parser = OptionParser(usageStr)

  parser.add_option('-r', '--red', help=default('Red agent'),
                    default='first_bot')
  parser.add_option('-b', '--blue', help=default('Blue agent'),
                    default='first_bot')

  (options, args) = parser.parse_args()

 
  if len(args) != 0:  sys.exit( "Invalid argument(s): " + str(args) );

 

  runSim(options.blue, options.red )
 

