from landsites import Land
from data_structures.heap import MaxHeap
from data_structures.referential_array import ArrayR

class Mode2Navigator:
    """
    The navigator uses a MaxHeap data structure to store the land sites where the key is the score of the land site.
    The MaxHeap is used to maintain the land sites in heap order based on the score of the land site.
    The simulate_day method simulates a day of the game by selecting the land sites that will maximise the scores of the adventure teams.
    The compute_score method computes the maximum/potential score of a land site based on the number of adventurers the team currently has.
    
    Other data structures and data types used include:
        Land - which represents the land site object.
        list - which is used to store the choices of adventurer numbers made by the adventure teams.
    
    Example:
        Given the array of following scores of the land sites:
        [400, 350, 375, 300, 325, 275, 250]
        
        The MaxHeap will be constructed as follows:
                            400
                           /   \
                         375    350
                        /   \   /  \
                      325  300 275 250
                    
        The time complexity will be O(N) for bottom-up heap construction, where N is the number of land sites.

        By using get_max() method, it will return the maximum element from the heap which is 400, and so on.
        The time complexity of get_max() method will be O(log(N)) where N is the number of land sites.
        If we were to get_max() K number of times, the time complexity will be O(K log(N)).

    Complexity:
        __init__:
            O(1) for best/worst case when initialising the object.

        add_sites:
            O(S) for best/worst case when looping through the list of land sites where 
            S is the length of the additional land sites (input sites) to be added.

        simulate_day:
            O(N + K log(N)) for best/worst case when constructing the MaxHeap,
            getting the maximum score of the land site out of the MaxHeap and
            adding back the updated score back to the MaxHeap K times
            where N is the number of existing land sites and K is the number of adventure teams participating in the game.

        compute_score:
            O(1) for best/worst case when computing the maximum/potential score of a land site which it
            involves arithmetic operations that take constant time operations.
    """

    def __init__(self, n_teams: int) -> None:
        """
        The method initialises the object and stores the number of adventurer teams in the game.

        Args:
            n_teams (int): The total number of teams in the game.

        Complexity: O(1) for best/worst case when initialising the object.
        """
        self.sites = []
        self.n_teams = n_teams

    def add_sites(self, sites: list[Land]) -> None:
        """
        The method stores and adds land sites (sites) to the object.
        If there are existing land sites already in the object, then
        this method will append land sites (sites) to the existing land sites.

        Args:
            sites (list[Land]): A list of land sites to be added to the object.

        Complexity: O(S) for best/worst case when looping through the list of land sites where 
            S is the length of the additional land sites (input sites) to be added.
        """
        for land in sites:
            self.sites.append(land)

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        The method simulates a day of the game.
        It will alter the internal states of the land sites.

        Args:
            adventurer_size (int): The size of the adventurers for every team.

        Returns:
            list[tuple[Land | None, int]]: A list of tuples, where each tuple represents the choices of adventurer numbers
                                           made by the first, second, third, ...,  n_teams team leaders in the order. 
                                           Each tuple should contain the land sites that the team leader chooses
                                           (or None object if the team leader decides not to send any adventurers), 
                                           and how many adventurers onto the land site
                                           (or 0 if the team leader decides not to send any adventurers).
        
        Complexity: O(N + K log(N)) for best/worst case when constructing the MaxHeap,
                    getting the maximum score of the land site out of the MaxHeap and
                    adding back the updated score back to the MaxHeap K times

            Where N is the number of existing land sites.
            Where K is the number of adventure teams participating in the game.
        """
        # Create a list to store the tuples of choices in order
        choices = []
        points = ArrayR(len(self.sites)) # O(N)
        
        for i, land in enumerate(self.sites): # O(N)
            # Compute score of the land site for each existing land site
            points[i] = (self.compute_score(land, adventurer_size)[0], land.get_name(), land) # O(1)
            
        # Construct the appropriate data structure to organize the scores of all the land sites
        sites_by_highest_score = MaxHeap.heapify(points, len(self.sites)) # O(N) for bottom-up heap construction

        # Each adventurer team takes turn selecting one land site to adventure
        for i in range(self.n_teams): # O(K)
            land: Land = sites_by_highest_score.get_max()[2] # O(log(N))
            _, adventurers_remaining, received = self.compute_score(land, adventurer_size)
            sent_adventurers = adventurer_size - adventurers_remaining

            if sent_adventurers == 0:
                # The adventure team skips their turn and do nothing
                choices.append((None, 0))
            else:
                # The adventure team selects the land site that will maximise their scores and sends the adventurers with a specific adventureer size
                choices.append((land, sent_adventurers))

            # Update the guardians and gold count of the land site
            land.set_gold(land.get_gold() - received)
            land.set_guardians(max(0, land.get_guardians() - sent_adventurers))

            # Update the score of the land site
            new_score = self.compute_score(land, adventurer_size)[0]
            sites_by_highest_score.add((new_score, land.get_name(), land)) # O(log(N))

        # Return the list of tuples
        return choices

    def compute_score(self, land: Land, adventurer_size: int) -> tuple[float, int, float]:
        """
        The method computes the maximum/potential score of a land site, based on the number of adventurers the team currently has.

        Args:
            land (Land): The land site object.
            adventurer_size (int): The size of the adventurers for every team.
        
        Returns:
            tuple[float, int, float]: A tuple containing the maximum/potential score of the land site, 
                                      the remaining adventure numbers, 
                                      and the gold (reward) gained for the particular score.

        Complexity: O(1) for best/worst case when computing the maximum/potential score of a land site which it
                    involves arithmetic operations that take constant time operations.
        """
        gold = land.get_gold()
        guardians = land.get_guardians()
        sent_adventurers = min(adventurer_size, guardians)

        if guardians == 0:
            received = gold
        else:
            received = min(sent_adventurers * gold / guardians, gold)

        adventurers_remaining = adventurer_size - sent_adventurers
        score = 2.5 * adventurers_remaining + received

        return score, adventurers_remaining, received