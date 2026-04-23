from model import (
    Location,
    Portal,
    EmptyEntity,
    Wizard,
    Goblin,
    Crystal,
    WizardMoves,
    GoblinMoves,
    GameAction,
    GameState,
)
from agents import WizardSearchAgent
import heapq
from dataclasses import dataclass


class WizardDFS(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, list[WizardMoves]] = {}
    search_stack: list[SearchState] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = []
        self.search_stack = [initial_search_state]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def next_search_expansion(self) -> GameState | None:
        
        # Return if search stack is empty
        if not self.search_stack:
            return None
        
        # Pop from stack
        current_node = self.search_stack.pop()

        
        # Check if current_node is the goal node
        if self.is_goal(current_node):
            self.plan = list(reversed(self.paths[current_node]))
            return
        
        return self.search_to_game(current_node)


        


    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        
        # Variables for simplicity
        source_var = self.game_to_search(source)
        target_var = self.game_to_search(target)

        # If alr visited, skip
        if target_var in self.paths:
            return
        
        # Add to path
        self.paths[target_var] = self.paths[source_var] + [action]
        
        # Add to stack
        self.search_stack.append(target_var)



class WizardBFS(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, list[WizardMoves]] = {}
    search_stack: list[SearchState] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = []
        self.search_stack = [initial_search_state]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def next_search_expansion(self) -> GameState | None:
        
        # COPY PASTED ORIGINAL CODE FROM DFS IMPLEMENTATION AND MADE ALTERATIONS
        
        # Return if search stack is empty
        if not self.search_stack:
            return None
        
        # Remove from queue
        current_node = self.search_stack.pop(0)

        
        # Check if current_node is the goal node
        if self.is_goal(current_node):
            self.plan = list(reversed(self.paths[current_node]))
            return
        
        return self.search_to_game(current_node)

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        
        # COPY PASTED ORIGINAL CODE FROM DFS IMPLEMENTATION

        # Variables for simplicity
        source_var = self.game_to_search(source)
        target_var = self.game_to_search(target)

        # If alr visited, skip
        if target_var in self.paths:
            return
        
        # Add to path
        self.paths[target_var] = self.paths[source_var] + [action]
        
        # Add to queue
        self.search_stack.append(target_var)

class WizardAstar(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, tuple[float, list[WizardMoves]]] = {}
    search_pq: list[tuple[float, SearchState]] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = 0, []
        self.search_pq = [(0, initial_search_state)]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def cost(self, source: GameState, target: GameState, action: WizardMoves) -> float:
        return 1

    def heuristic(self, target: GameState) -> float:

        # Using manhattan formula -> d = | x2 - x1 | + | y2 - y1 |

        # Location formulas used for heuristic computation
        
        current_location = target.active_entity_location
        goal_location = target.get_all_tile_locations(Portal)[0]
        

        return abs(current_location.row - goal_location.row) + abs(current_location.col - goal_location.col)




    def next_search_expansion(self) -> GameState | None:
     
        # Return if priority queue is empty
        if not self.search_pq:
            return None
        
        # Remove from queue
        current_node = heapq.heappop(self.search_pq)[1]

        
        # Check if current_node is the goal node
        if self.is_goal(current_node):
            self.plan = list(reversed(self.paths[current_node][1]))
            return
        
        return self.search_to_game(current_node)

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:

        # Variables for simplicity
        source_var = self.game_to_search(source)
        target_var = self.game_to_search(target)

        g_val_source = self.paths[source_var][0]
        step_cost = self.cost(source, target, action)

        # Calculate f cost -> (g + h)
        f_cost = (g_val_source + step_cost) + self.heuristic(target)

        # If alr visited or more expensive than alr found path, skip
        if target_var in self.paths and self.paths[target_var][0] <= (g_val_source + step_cost):
            return
        
        # Add to path
        self.paths[target_var] = ((g_val_source + step_cost), self.paths[source_var][1] + [action])

        # Add to priority queue
        heapq.heappush(self.search_pq, (f_cost, target_var))


class CrystalSearchWizard(WizardSearchAgent):
    
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location
        # Added crystals to search state
        crystals_loc: tuple[Location, ...]

    # Added closed_set to avoid searching already opened tiles
    closed_set: set[SearchState] = set()
    paths: dict[SearchState, tuple[float, list[WizardMoves]]] = {}
    search_pq: list[tuple[float, SearchState]] = []
    initial_game_state: GameState
    
    # Dictionary to cache mst
    mst_dict: dict = {}

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()


        # Clear entity on current location
        new_game_state = self.initial_game_state.replace_entity(
            initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
        )

        crystal_set = self.initial_game_state.get_all_entity_locations(Crystal)

        # Update new_game_state by replacing collected crystals with empty
        for crystal in crystal_set:
            if crystal not in search_state.crystals_loc:
                new_game_state = new_game_state.replace_entity(
                    crystal.row, crystal.col, EmptyEntity()   
                )

        new_game_state = (
            new_game_state
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]

        # Added crystals, sort the set so it is consistent with every search
        crystals_loc = tuple(sorted(game_state.get_all_entity_locations(Crystal)))
        
        return self.SearchState(wizard_loc, portal_loc, crystals_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state
        initial_search_state = self.game_to_search(game_state)
        
        self.paths = {}
        self.paths[initial_search_state] = 0, []
        self.search_pq = [(0, initial_search_state)]

    # The goal now is -> All crystals collected and at portal
    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc and len(state.crystals_loc) == 0

    def cost(self, source: GameState, target: GameState, action: WizardMoves) -> float:
        return 1
    
    
    def prim_mst(self, nodes: list) -> float:

        # Bounds check
        if len(nodes) <= 1:
            return 0
        
        mst = set()
        minimum_edge = [float('inf')] * len(nodes)
        minimum_edge[0] = 0

        # cost, node
        priority_queue = [(0, 0)]
        
        total_cost = 0

        while priority_queue:
            cost, node = heapq.heappop(priority_queue)

            # Check if already in mst
            if node in mst:
                continue

            mst.add(node)
            total_cost += cost

            for other in range(len(nodes)):
                if other not in mst:
                    distance = (abs(nodes[node].row - nodes[other].row) + abs(nodes[node].col - nodes[other].col))
                    
                    # Update minimum edge if needed
                    if distance < minimum_edge[other]:
                        minimum_edge[other] = distance
                        heapq.heappush(priority_queue, (distance, other))

        return total_cost


    
    def heuristic(self, target: GameState) -> float:

        # Build MST using Prim's algorithm, then return to regular heuristic once no crystals remain

        current_location = target.active_entity_location
        goal_location = target.get_all_tile_locations(Portal)[0]
        crystals_remaining = tuple(sorted(target.get_all_entity_locations(Crystal)))


        if crystals_remaining:

            # Call from cache if able to avoid recomputation
            key = crystals_remaining

            # Add to cache if not already in it
            if key not in self.mst_dict:
                
                nodes = list(crystals_remaining) + [goal_location]
                self.mst_dict[key] = self.prim_mst(nodes)
                
            # Distance from wizard to nearest crystal

            closest_crystal = float('inf')
            for crystal in crystals_remaining:
                distance = abs(current_location.row - crystal.row) + abs(current_location.col - crystal.col)

                # Update minimum
                if distance < closest_crystal:
                    closest_crystal = distance
            
            # ------------------------------------------------------

            return self.mst_dict[key] + closest_crystal
        
        # Return to regular logic once all crystals are collected ------------------------

        return abs(current_location.row - goal_location.row) + abs(current_location.col - goal_location.col)

    def next_search_expansion(self) -> GameState | None:
        # Return if priority queue is empty
        if not self.search_pq:
            return None
        
        # Remove from queue
        current_node = heapq.heappop(self.search_pq)[1]

        # Skip if in closed set
        if current_node in self.closed_set:
            return self.next_search_expansion()
        

        # Add to closed set
        self.closed_set.add(current_node)


        # Check if current_node is the goal node
        if self.is_goal(current_node):
            self.plan = list(reversed(self.paths[current_node][1]))
            return
        
        return self.search_to_game(current_node)

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        
        # Variables for simplicity
        source_var = self.game_to_search(source)
        target_var = self.game_to_search(target)

        g_val_source = self.paths[source_var][0]
        step_cost = self.cost(source, target, action)

        # Calculate f cost -> (g + h)
        f_cost = (g_val_source + step_cost) + self.heuristic(target)

        # If alr visited or more expensive than alr found path, skip
        if target_var in self.paths and self.paths[target_var][0] <= (g_val_source + step_cost):
            return
        
        # Add to path
        self.paths[target_var] = ((g_val_source + step_cost), self.paths[source_var][1] + [action])

        # Add to priority queue
        heapq.heappush(self.search_pq, (f_cost, target_var))



class SuboptimalCrystalSearchWizard(CrystalSearchWizard):

    def heuristic(self, target: GameState) -> float:

        # Make inadmissible by multiplying by a factor of 2
        
        cost_factor = 2


        # Build MST using Prim's algorithm, then return to regular heuristic once no crystals remain

        current_location = target.active_entity_location
        goal_location = target.get_all_tile_locations(Portal)[0]
        crystals_remaining = tuple(sorted(target.get_all_entity_locations(Crystal)))


        if crystals_remaining:

            # Call from cache if able to avoid recomputation
            key = crystals_remaining

            # Add to cache if not already in it
            if key not in self.mst_dict:
                
                nodes = list(crystals_remaining) + [goal_location]
                self.mst_dict[key] = self.prim_mst(nodes)
                
            # Distance from wizard to nearest crystal

            closest_crystal = float('inf')
            for crystal in crystals_remaining:
                distance = abs(current_location.row - crystal.row) + abs(current_location.col - crystal.col)

                # Update minimum
                if distance < closest_crystal:
                    closest_crystal = distance
            
            # ------------------------------------------------------

            return cost_factor * (self.mst_dict[key] + closest_crystal)
        
        # Return to regular logic once all crystals are collected ------------------------

        return cost_factor * (abs(current_location.row - goal_location.row) + abs(current_location.col - goal_location.col))
