from model import (
    Location,
    Portal,
    Wizard,
    Goblin,
    Crystal,
    WizardMoves,
    GoblinMoves,
    GameAction,
    GameState,
)
from agents import ReasoningWizard
from dataclasses import dataclass


class WizardGreedy(ReasoningWizard):
    def evaluation(self, state: GameState) -> float:

        # Return -infinity evaluation if wizard is dead
        if len(state.get_all_entity_locations(Wizard)) == 0:
            return float('-inf')
        
        current_location = state.get_all_entity_locations(Wizard)[0]

        # Calculate portal distance
                
        goal_location = state.get_all_tile_locations(Portal)[0]

        goal_distance = abs(current_location.row - goal_location.row) + abs(current_location.col - goal_location.col)

        # Calculate goblin distance
        goblin_locations = state.get_all_entity_locations(Goblin)

        closest_goblin_distance = float('inf')
        for goblin in goblin_locations:
            current_distance = abs(current_location.row - goblin.row) + abs(current_location.col - goblin.col)
        
            closest_goblin_distance = min(closest_goblin_distance, current_distance)

        # Calculate crystal distance
        crystal_locations = state.get_all_entity_locations(Crystal)

        if len(crystal_locations) != 0:
            closest_crystal_distance = float('inf')
            for crystal in crystal_locations:
                current_distance = abs(current_location.row - crystal.row) + abs(current_location.col - crystal.col)
            
                closest_crystal_distance = min(closest_crystal_distance, current_distance)
        else:
            closest_crystal_distance = 0
            

        # Put heavy weight for collected crystals (state.score)
        # -1.5 * Goal dist + goblin dist + 10 *crystal score
        return (-1.5 * goal_distance + closest_goblin_distance - (2) * closest_crystal_distance + (10) * state.score)
        


class WizardMiniMax(ReasoningWizard):
    max_depth: int = 2

    def evaluation(self, state: GameState) -> float:

        # Return -infinity evaluation if wizard is dead
        if len(state.get_all_entity_locations(Wizard)) == 0:
            return float('-inf')
        
        current_location = state.get_all_entity_locations(Wizard)[0]

        # Calculate portal distance
                
        goal_location = state.get_all_tile_locations(Portal)[0]

        goal_distance = abs(current_location.row - goal_location.row) + abs(current_location.col - goal_location.col)

        # Calculate goblin distance
        goblin_locations = state.get_all_entity_locations(Goblin)

        closest_goblin_distance = float('inf')
        for goblin in goblin_locations:
            current_distance = abs(current_location.row - goblin.row) + abs(current_location.col - goblin.col)
        
            closest_goblin_distance = min(closest_goblin_distance, current_distance)

        # Calculate crystal distance
        crystal_locations = state.get_all_entity_locations(Crystal)

        if len(crystal_locations) != 0:
            closest_crystal_distance = float('inf')
            for crystal in crystal_locations:
                current_distance = abs(current_location.row - crystal.row) + abs(current_location.col - crystal.col)
            
                closest_crystal_distance = min(closest_crystal_distance, current_distance)
        else:
            closest_crystal_distance = 0
            

        # Put heavy weight for collected crystals (state.score)
        # -1.5 * Goal dist + goblin dist + 10 *crystal score
        return (-1.5 * goal_distance + closest_goblin_distance - (2) * closest_crystal_distance + (10) * state.score)

    def is_terminal(self, state: GameState) -> bool:
        if len(state.get_all_entity_locations(Wizard)) == 0:
            return True
        

        # Returns true if reached portal, otherwise reaches false
        return state.get_all_entity_locations(Wizard)[0] == state.get_all_tile_locations(Portal)[0]

    def react(self, state: GameState) -> WizardMoves:
        
        action = None
        optimal_outcome = float('-inf')

        for potential_action, successor in self.get_successors(state):
            outcome = self.minimax(successor, depth = self.max_depth - 1)

            # Compare to current optimal_outcome, overwrite if better
            # Choose action with best outcome
            if outcome > optimal_outcome:
                optimal_outcome = outcome
                action = potential_action
        
        return action
        


    def minimax(self, state: GameState, depth: int):
        
        # Check if terminal before every turn
        if self.is_terminal(state):
            return self.evaluation(state)
        
        # Check if the active entity is of type wizard, and maximize
        if type(state.get_active_entity()) == Wizard:
            
            if depth == 0:
                return self.evaluation(state)
            
            value = float('-inf')

            for action, successor in self.get_successors(state):
                value = max(value, self.minimax(successor, depth - 1))
            return value
        # Goblin's turn, minimizer
        else:

            value = float('inf')
            for action, successor in self.get_successors(state):
                value = min(value, self.minimax(successor, depth))
            return value



class WizardAlphaBeta(ReasoningWizard):
    max_depth: int = 2

    # evaluation() and is_terminal() are the same as minimax
    # react() and alpha_beta_minimax are same as in minimax, but
    # with added alpha & beta values <--- (obviously)


    def evaluation(self, state: GameState) -> float:

        # Return -infinity evaluation if wizard is dead
        if len(state.get_all_entity_locations(Wizard)) == 0:
            return float('-inf')
        
        current_location = state.get_all_entity_locations(Wizard)[0]

        # Calculate portal distance
                
        goal_location = state.get_all_tile_locations(Portal)[0]

        goal_distance = abs(current_location.row - goal_location.row) + abs(current_location.col - goal_location.col)

        # Calculate goblin distance
        goblin_locations = state.get_all_entity_locations(Goblin)

        closest_goblin_distance = float('inf')
        for goblin in goblin_locations:
            current_distance = abs(current_location.row - goblin.row) + abs(current_location.col - goblin.col)
        
            closest_goblin_distance = min(closest_goblin_distance, current_distance)

        # Calculate crystal distance
        crystal_locations = state.get_all_entity_locations(Crystal)

        if len(crystal_locations) != 0:
            closest_crystal_distance = float('inf')
            for crystal in crystal_locations:
                current_distance = abs(current_location.row - crystal.row) + abs(current_location.col - crystal.col)
            
                closest_crystal_distance = min(closest_crystal_distance, current_distance)
        else:
            closest_crystal_distance = 0
            

        # Put heavy weight for collected crystals (state.score)
        # -1.5 * Goal dist + goblin dist + 10 *crystal score
        return (-1.5 * goal_distance + closest_goblin_distance - (2) * closest_crystal_distance + (10) * state.score)

    def is_terminal(self, state: GameState) -> bool:
        if len(state.get_all_entity_locations(Wizard)) == 0:
            return True
        

        # Returns true if reached portal, otherwise reaches false
        return state.get_all_entity_locations(Wizard)[0] == state.get_all_tile_locations(Portal)[0]

    def react(self, state: GameState) -> WizardMoves:
        
        action = None
        optimal_outcome = float('-inf')

        alpha = float('-inf')
        beta = float('inf')

        for potential_action, successor in self.get_successors(state):
            outcome = self.alpha_beta_minimax(successor, depth = self.max_depth - 1, alpha=alpha, beta=beta)

            # Compare to current optimal_outcome, overwrite if better
            # Choose action with best outcome
            if outcome > optimal_outcome:
                optimal_outcome = outcome
                action = potential_action
                # Update alpha
                alpha = max(optimal_outcome, alpha)

        return action

    # ADDED ALPHA AND BETA as function parameters 
    def alpha_beta_minimax(self, state: GameState, depth: int, alpha: float, beta: float):
        
        # Check if terminal before every turn
        if self.is_terminal(state):
            return self.evaluation(state)
        
        # Check if the active entity is of type wizard, and maximize
        if type(state.get_active_entity()) == Wizard:
            
            if depth == 0:
                return self.evaluation(state)
            
            value = float('-inf')

            for action, successor in self.get_successors(state):
                value = max(value, self.alpha_beta_minimax(successor, depth - 1, alpha, beta))
                alpha = max(alpha, value)

                # PRUNE
                if alpha >= beta:
                    break

            return value
        # Goblin's turn, minimizer
        else:

            value = float('inf')
            for action, successor in self.get_successors(state):
                value = min(value, self.alpha_beta_minimax(successor, depth, alpha, beta))
                beta = min(beta, value)

                # PRUNE
                if alpha >= beta:
                    break

            return value




class WizardExpectimax(ReasoningWizard):
    max_depth: int = 2

    def evaluation(self, state: GameState) -> float:

        # Return -infinity evaluation if wizard is dead
        if len(state.get_all_entity_locations(Wizard)) == 0:
            return float('-inf')
        
        current_location = state.get_all_entity_locations(Wizard)[0]

        # Calculate portal distance
                
        goal_location = state.get_all_tile_locations(Portal)[0]

        goal_distance = abs(current_location.row - goal_location.row) + abs(current_location.col - goal_location.col)

        # Calculate goblin distance
        goblin_locations = state.get_all_entity_locations(Goblin)

        closest_goblin_distance = float('inf')
        for goblin in goblin_locations:
            current_distance = abs(current_location.row - goblin.row) + abs(current_location.col - goblin.col)
        
            closest_goblin_distance = min(closest_goblin_distance, current_distance)

        # Calculate crystal distance
        crystal_locations = state.get_all_entity_locations(Crystal)

        if len(crystal_locations) != 0:
            closest_crystal_distance = float('inf')
            for crystal in crystal_locations:
                current_distance = abs(current_location.row - crystal.row) + abs(current_location.col - crystal.col)
            
                closest_crystal_distance = min(closest_crystal_distance, current_distance)
        else:
            closest_crystal_distance = 0
            

        # Put heavy weight for collected crystals (state.score)
        # -1.5 * Goal dist + goblin dist + 10 *crystal score
        return (-1.5 * goal_distance + closest_goblin_distance - (2) * closest_crystal_distance + (10) * state.score)

    def is_terminal(self, state: GameState) -> bool:
        if len(state.get_all_entity_locations(Wizard)) == 0:
            return True
        

        # Returns true if reached portal, otherwise reaches false
        return state.get_all_entity_locations(Wizard)[0] == state.get_all_tile_locations(Portal)[0]

    def react(self, state: GameState) -> WizardMoves:
        
        action = None
        optimal_outcome = float('-inf')

        for potential_action, successor in self.get_successors(state):
            outcome = self.expectimax(successor, depth = self.max_depth - 1)

            # Compare to current optimal_outcome, overwrite if better
            # Choose action with best outcome
            if outcome > optimal_outcome:
                optimal_outcome = outcome
                action = potential_action
        
        return action
        


    def expectimax(self, state: GameState, depth: int):
        
        # Check if terminal before every turn
        if self.is_terminal(state):
            return self.evaluation(state)
        
        # Check if the active entity is of type wizard, and maximize
        if type(state.get_active_entity()) == Wizard:
            
            if depth == 0:
                return self.evaluation(state)
            
            value = float('-inf')

            for action, successor in self.get_successors(state):
                value = max(value, self.expectimax(successor, depth - 1))
            return value
        # Goblin's turn, calculate expected value
        else:

            successors = self.get_successors(state)
            total_val = 0

            for action, successor in successors:
                total_val += self.expectimax(successor, depth)
            
            # Average out total value across all successors
            return total_val / len(successors)

