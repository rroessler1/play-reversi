import random
from agent.base import Agent
from board import Move
from board import GameState
from reversi_types import Point, Player


class AlphaBetaBot(Agent):
    search_depth = 5

    def select_move(self, game_state):
        alpha = float('-inf')
        beta = float('inf')
        best_score = alpha if game_state.next_player == Player.white else beta
        best_moves = []
        for point in game_state.board._possibly_valid_points:
            move = Move.play(point)
            if game_state.is_valid_move_for_player(Move.play(point), game_state.next_player):
                next_state = game_state.apply_move(move)
                our_score = self.alpha_beta_search(next_state, next_state.next_player, alpha, beta, self.search_depth)
                if game_state.next_player == Player.white:
                    if our_score > best_score:
                        best_score = our_score
                        best_moves = [move]
                        alpha = best_score
                    elif our_score == best_score:
                        best_moves.append(move)
                else:
                    if our_score < best_score:
                        best_score = our_score
                        best_moves = [move]
                        beta = best_score
                    elif our_score == best_score:
                        best_moves.append(move)
        if not best_moves:
            return Move.pass_turn()
        print("Best score was %s" % best_score)
        return random.choice(best_moves)

    def alpha_beta_search(self, game_state, current_player, alpha, beta, depth):
        if game_state.is_over():
            winner = game_state.get_winner()
            if winner == Player.white:
                return float('inf')
            if winner == Player.black:
                return float('-inf')
            return 0

        if depth == 0:
            return GameState.corner_evaluation_function(game_state)

        if current_player == Player.white:
            best_score = float('-inf')
            for point in game_state.board._possibly_valid_points:
                move = Move.play(point)
                if game_state.is_valid_move_for_player(Move.play(point), current_player):
                    next_state = game_state.apply_move(move)
                    score = self.alpha_beta_search(next_state, next_state.next_player, alpha, beta, depth-1)
                    best_score = max(score, best_score)
                    alpha = max(score, alpha)
                    if beta <= alpha:
                        return best_score
            return best_score

        if current_player == Player.black:
            best_score = float('inf')
            for point in game_state.board._possibly_valid_points:
                move = Move.play(point)
                if game_state.is_valid_move_for_player(Move.play(point), current_player):
                    next_state = game_state.apply_move(move)
                    score = self.alpha_beta_search(next_state, next_state.next_player, alpha, beta, depth-1)
                    best_score = min(score, best_score)
                    beta = min(score, beta)
                    if beta <= alpha:
                        return best_score
            return best_score
