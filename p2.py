from p2_game import Game, State
from collections import defaultdict

rounds = 100
wins = defaultdict(lambda: 0)


def runSim(redBot, blueBot):

  # instead of manully importing file name, use command line option to choose bots to play
  # however, this part can not be placed into a subfunction because importing files in a local function  
  # doesn't not update red_bot, blue_bot.
  # There might be a way to create red_bot and blue_bot as global variables, then this decision part can be placed in a sub fucntion.
  validBot = [ "first_bot", "rollout_bot", "uniform_bot", "greedy_bot", "uct_bot", "fast_bot"];
 
  a, chosenBotB =  blueBot 
  b, chosenBotR = redBot
  if chosenBotB not in validBot :
    sys.exit(chosenBotB + " is not an valid bot");
  if chosenBotR not in validBot:
    sys.exit(chosenBotR + " is not an valid bot");
    
  if chosenBotB == validBot[0]:
    import first_bot as blue_bot
  elif chosenBotB == validBot[1]:
    import rollout_bot as blue_bot
  elif chosenBotB == validBot[2]:
    import uniform_bot as blue_bot
  elif chosenBotB == validBot[3]:
    import greedy_bot as blue_bot
  elif chosenBotB == validBot[4]:
    import uct_bot as blue_bot
  elif chosenBotB == validBot[5]:
    import fast_bot as blue_bot
 
  if chosenBotR == validBot[0]:
    import first_bot as red_bot
  elif chosenBotR == validBot[1]:
    import rollout_bot as red_bot
  elif chosenBotR == validBot[2]:
    import uniform_bot as red_bot
  elif chosenBotR == validBot[3]:
    import greedy_bot as red_bot
  elif chosenBotR == validBot[4]:
    import uct_bot as red_bot
  elif chosenBotR == validBot[5]:
    import fast_bot as red_bot

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

  runSim(("red", options.red), ("blue", options.blue) )
 

