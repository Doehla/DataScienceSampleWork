import numpy as np
import itertools
import logging


class Environment:
    row_cnt = 6
    col_cnt = 7
    max_turns = 6 * 7
    agents = {}
    forfit_move_on_invalid = True

    def __init__(self):
        self.logger = logging.getLogger('game.environment')
        self.logger.debug('Instanting environment class')
        self.grid = np.zeros((self.row_cnt, self.col_cnt))


    def add_player(self, name, model, key=None):
        """Add player to the game.
        Game expects 2 players which will be assigned to keys 1 and -1
        Expect a model to be provided to return the moves of the player through
            calls placed to get_move()
        """
        self.logger.debug('Adding player to environment class')
        if key is not None:
            self.agents[key] = (name, model)
        else:
            if 1 in self.agents.keys():
                self.agents[-1] = (name, model)
            else:
                self.agents[1] = (name, model)
        self.logger.info('Set up player: {name}'.format(name=name))


    def __repr__(self):
        """Provide a representation of the board. Will attempt to use a pretty representation.
        If it cannot, will default to displaying the numbers backing the grid.
        """
        ret_str = ''
        try:
            ret_str = self.print_special(1)
        except Exception as e:
            for row in self.grid[::-1]:
                ret_str += '|'
                for col in row:
                    ret_str += '{:>2.0f}'.format(col)
                ret_str += ' |\n'

        return ret_str


    def print_special(self, agent_num):
        """Provide a pretty printed representation of the board.
        """
        ret_str = ''
        for row in self.grid[::-1]:
            ret_str += '|'
            for col in row:
                if col == agent_num:
                    ret_str += '#'
                elif col == 0:
                    ret_str += ' '
                else:
                    ret_str += 'X'
            ret_str += '|\n'

        return ret_str


    def accept_move(self, slot, agent):
        """Update game state with the move provided.
        """
        try:
            i = int(next(idx for idx, x in enumerate(self.grid[:,slot]) if x == 0))
            self.grid[i, slot] = agent
            self.logger.info('Player move logged to: [{}, {}]'.format(i, slot))
        except Exception as e:
            self.logger.error('Move submitted to slot {}, with grid:\n{}'.format(slot, self.grid))
            if not self.forfit_move_on_invalid:
                raise ValueError('Invalid Move Submitted')
            self.logger.warning('Player move invalid for slot: {}'.format(slot))


    def _fetch_sets(self):
        """Provide all possible avenues for adjacency inspection.
        """
        for i in range(self.col_cnt):
            yield self.grid[:,i]
        for i in range(self.row_cnt):
            yield self.grid[i,:]
        for i in range(-self.row_cnt + 1, self.col_cnt):
            yield np.diag(self.grid, k=i)
        for i in range(-self.row_cnt + 1, self.col_cnt):
            yield np.diag(np.fliplr(self.grid), k=i)


    def determine_if_winner(self):
        """Examine adjacency to determine if wining criteria has been meet.
        """
        self.logger.debug('Checking win condition criteria')
        found_winner = False
        for test_set in self._fetch_sets():
            test_set = np.trim_zeros(test_set)

            # No need to consider if there are not at least 4 items in the set
            if test_set.size < 4:
                continue

            for k, g in itertools.groupby(test_set):
                # k = 0 is just empty cells, so skip these
                if k == 0:
                    continue
                cnt = int(sum(1 for _ in g))
                if cnt >= 4:
                    try:
                        name, model = self.agents.get(k, None)
                    except Exception as e:
                        self.logger.error('Failed examining winning condition for k = {}'.format(k))
                        raise Exception(e)

                    self.logger.info('Found wining condition met for: {}'.format(name))
                    found_winner = True
                    break

        if found_winner:
            self.logger.info('Board at end of game:\n{}'.format(self.print_special(k)))

        return found_winner

    def run_game(self):
        """Process game.
        Termination conditions:
            - winner found
            - maximum number of allowed turns has been meet
        """
        self.logger.info('Starting game')

        # Ensure we have a player for -1 and 1:
        agent_neg = self.agents.get(-1, None)
        agent_pos = self.agents.get(1, None)
        if agent_neg is None or agent_pos is None:
            raise Exception('Expecting two players for this game!')

        # set up loop variables
        player_state = 1
        win_condition = False
        turn_counter = 0

        # Run the game:
        while not win_condition:
            turn_counter += 1
            self.logger.debug('Executing turn: {}'.format(turn_counter))

            # get the agent and the move they make:
            name, agent = self.agents.get(player_state, None)
            token_slot = agent.get_move(self.grid*player_state)

            # Update game state with the move:
            self.accept_move(token_slot, player_state)
            self.logger.debug('Turn made by agent name: {}'.format(name))

            # Check if they won the game:
            win_condition = self.determine_if_winner()

            # If the game has exceeded the max number of turns, end it.
            if turn_counter > self.max_turns:
                self.logger.debug('Max turns limit reached. Terminating in stalemate.')
                break

            # Change player state to have the other player take a turn:
            player_state = player_state * -1




if __name__ == '__main__':
    game = Environment()
    game.add_player('rando', 'x')
    game.add_player('dumbo', 'hi')

    game.accept_move(3, 1)
    game.accept_move(3, 1)
    game.accept_move(3, 1)
    game.accept_move(3, 1)
    game.accept_move(2,-1)
    game.accept_move(2,-1)
    game.accept_move(2,-1)
    game.accept_move(2, 1)
    game.accept_move(0,-1)
    game.accept_move(1,-1)
    game.accept_move(1, 1)
    print(game)
    game.determine_if_winner()
