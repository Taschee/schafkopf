## Documentation

This python code was written for my masters thesis, developing an AI for the bavarian card game Schafkopf. 

#### The game rules
The "schafkopf" module firstly contains a number of files providing the implementation of the game rules. 

Cards are encoded as tuples (x, y) with x corresponding to the rank and y corresponding to the suit of the card, with ranks x encoded by the numbers 0 to 7 in ascending order. Suits are encoded as numbers as well, with 0 = "Bells", 1 = "Hearts", 2="Leaves" and 3="Acorns". This way, determining which card is higher can always easily be accomplished by simple comparisons of the appropriate values. These encodings are saved in ranks.py and suits.py.
In payouts.py, the tariff used in the game is fixed.
Game modes are encoded as tuples _(type, suit)_. The types are encoded as numbers as well, with 0 = "No Game", 1 = "Partner Mode", 2 = "Wenz" and 3 = "Solo". 

The class **CardDeck** takes care of shuffeling and dealing cards.
The class **Trick** provides some functionality for a trick during trick play, like determining its winner. The classes **BiddingGame** and **TrickGame** incapsulate all functionality during the two phases of a game. Both are combined in the class **Game**, which adds all methods to compute final rewards, after a game is finished.
A game has to be instantiated with a game state and a list of four players. A game state is just a dictionary containing the player hands, the index of the starting player, the index of the current player, the declaring player, the game mode, all previous mode proposals, a list of previous tricks and the current trick.

#### Players
All developed players are collected in the players submodule.
Each player is a subclass of the **Player** class, which provides some general functionality like picking up cards. Each such player in the player list has to at least provide two methods that takes the public info provided by the game and the possible options for the next action as input: 
A _choose_game_mode_ method that returns one possible game mode from the options and a _play_card_ method that returns one card from the players current hand.

The **RandomPlayer** chooses all cards by random, while always passing during the bidding phase. The **FullyRandomPlayer** makes random announcements during the bidding phase as well.
The **UCTPlayer** uses Monte Carlo Tree Search on a fixed number of determinizations for each of his decisions, with the UCT formula as a tree policy. The number of determinizations and the number of simulations can be set as well as the exploration constant. On default, it uses a random policy for playouts during simulation, but it can be provided with a list of different players for performing these simulations.
The **ISUCTPlayer** use Information Set Monte Carlo Tree Search for his decisions instead of determinizations. The number of simulations and the exploitation constant can again be varied, as well as a simulation player list provided if the random policy shall be replaced.
The **DummyPlayer** will always play his provided favorite cards first if possible, and declare his favorite game mode. He is used mainly for testing.
The **HeuristicPlayer** finally just uses some typical rules of thumb for his play, defaulting to random play whenever a adequate heuristic is missing.
The **HumanConsolePlayer** can be used to play via the console without a user interface. It is still using and providing only information encoded in the way described above though. Hopefully this will be improved soon.
A **NNPlayer** uses pretrained neural networks to make each decision. It has to be instantiated with the trained model for game mode classification during the bidding phase, and models for prediction of the next card for each of the three game modes for trick play.
##### Data
This module provides scripts for downloading and preprocessing all data for the training of the neural networks, and the already downloaded and prepared datasets.
##### Models
Here, the scripts for training the different models are located. Also there are a number of scripts for evaluating and analyzing the performance of trained models, as well as the already trained models for bidding, trick play and inference.

#### Tournaments
This submodule only contains some scripts that have been used for experiments with different players.

#### GUI
A little bit of work was put into the development of a simple graphical user interface using kivy and the kivy language. This work is still unfinished though. 

### Monte Carlo Tree Analyzing
This provides only a few simple scripts which were used for the analysis and visualization of the partial game trees built during Monte Carlo Tree Search.




