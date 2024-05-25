from landsites import Land
from data_structures.heap import MaxHeap
from data_structures.referential_array import ArrayR

class Mode2Navigator:
    """
    - Required to include short paragraphs (50-300 words) detailing your approach in detail
    - Approach details in general should include:
        - Data structures and data types used
        - Small example(s)
        - Explanations/Reasonings/Proofs on your complexity result (i.e., details on why you obtained the specific best case and worst case results)

    Approach:
    - The navigator uses a MaxHeap data structure to store the land sites where the key is the score of the land site.
    - The MaxHeap is used to maintain the land sites in sorted order based on the score of the land site.
    - The simulate_day method simulates a day of the game by selecting the land sites that will maximise the scores of the adventure teams.
    - The compute_score method computes the maximum/potential score of a land site based on the number of adventurers the team currently has.
    
    Data structures and data types used:
    - MaxHeap: Used to store the land sites where the key is the score of the land site.
    - Land: Represents the land site object.
    - list: Used to store the choices of adventurer numbers made by the adventure teams.
    
    Example:
    - sites = [Land("Dawn Island", 100, 50), Land("Shimotsuki Village", 200, 100), Land("Gecko Islands", 300, 150)]
    - n_teams = 3
    - navigator = Mode2Navigator(n_teams)
    - navigator.add_sites(sites)
    - choices = navigator.simulate_day(100)
    - Output: [(Land("Gecko Islands", 300, 50), 50), (Land("Shimotsuki Village", 200, 50), 50), (None, 0)]

    Complexity:
    - simulate_day method:
        - Best case:
        - Worst case: O(N + K log(N)) where N is the number of existing land sites and K is the number of adventure teams participating in the game
    - compute_score method:
        - Best case:
        - Worst case: O(1) where the maximum/potential score of a land site is computed
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
        
        Complexity:
            Best case:
            Worst case: O(N + K log(N)) where
                N is the number of existing land sites.
                K is the number of adventure teams participating in the game.
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
        Keep in mind multiple land sites could have the same maximum/potential score. 

        Args:
            land (Land): The land site object.
            adventurer_size (int): The size of the adventurers for every team.
        
        Returns:
            tuple[float, int, float]: A tuple containing the maximum/potential score of the land site, 
                                      the remaining adventure numbers, 
                                      and the gold (reward) gained for the particular score.

        Complexity: O(1) for best/worst case when computing the maximum/potential score of a land site.
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