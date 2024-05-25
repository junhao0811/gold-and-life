from landsites import Land
from data_structures.bst import BinarySearchTree
from data_structures.node import TreeNode


class Mode1Navigator:
    """
    This class represents a navigator that helps adventurers to select the land sites to attack.
    
    - Required to include short paragraphs (50-300 words) detailing your approach in detail
    - Approach details in general should include:
        - Data structures and data types used
        - Small example(s)
        - Explanations/Reasonings/Proofs on your complexity result (i.e., details on why you obtained the specific best case and worst case results)

    Approach:
    - The navigator uses a BinarySearchTree to store the land sites where the key is the ratio of guardians to reward and the item is the land site.
    - The BinarySearchTree is used to maintain the land sites in sorted order based on the ratio of guardians to reward.
    - The select_sites method selects the land sites you desire to attack by iterating through the BinarySearchTree.
    - The select_sites_from_adventure_numbers method calculates the maximum amount of reward you can make with different adventurer numbers.
    - The update_site method is used to update the state of the land object.

    Data structures and data types used:
    - BinarySearchTree: Used to store the land sites where the key is the ratio of guardians to reward and the item is the land site.
    - Land: Represents the land site object.
    - list: Used to store the selected land sites and the number of adventurers you will be sending to the corresponding land site.

    Example:
    - sites = [Land("Dawn Island", 100, 50), Land("Shimotsuki Village", 200, 100), Land("Gecko Islands", 300, 150)]
    - adventurers = 200
    - navigator = Mode1Navigator(sites, adventurers)
    - selected_sites = navigator.select_sites()
    - Output: [("Dawn Island", 50), ("Shimotsuki Village", 100), ("Gecko Islands", 50)]

    Complexity:
    - select_sites method:
        - Best case: O(log(N)) where N is the number of land sites
        - Worst case: O(N) where N is the number of land sites
    - select_sites_from_adventure_numbers method:
        - Best case: 
        - Worst case: O(A * N) where A is the length of adventure_numbers and N is the number of land sites
    - update_site method:
        - Best case: 
        - Worst case: O(log(N)) where N is the number of land sites
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        This method perform initialisation.

        Args:
            sites (list[Land]): A list that holds the initial states of the land sites.
            adventurers (int): The total number of adventurers c you are going to take with you on your journey.

        Complexity:
            Best case:
            Worst case: O(N log(N)) where N is the number land sites
        """
        # Initialise a BinarySearchTree where each TreeNode contains the ratio of guardians to reward as its key and the land site as its item       
        self.sites = BinarySearchTree()
        for land in sites: # O(N) where N is the number of land sites
            try:
                self.sites[land.get_guardians() / land.get_gold()] = land # O(CompK * log(N)) inserting at the bottom of the balanced tree
            except ZeroDivisionError:
                continue
        self.adventurers = adventurers

    def select_sites(self, adventurers: int | None = None) -> list[tuple[Land, int]]:
        """
        The method shall selects the land sites you desire to attack.

        Returns:
            list[tuple[Land, int]]: A list of pairs (in tuple data type) where each pair containing a land object
                                    and the number of adventurers you will be sending to the corresponding land site.

        Complexity:
            Best case: O(log(N)) where N is the number of land sites
            Worst case: O(N) where N is the number of land sites
        """
        if adventurers is None:
            adventurers = self.adventurers

        # Create an empty list to store the tuples
        selected_sites = []

        for tree_node in self.sites: # Implicitly calls __iter__() to create the in-order iterator
            land: Land = tree_node.item
            number_of_guardians = land.get_guardians()
            # If the land site has more guardians than adventurers then send all the adventurers there
            # Else, send the number of adventurers that matches the number of guardians to max out the reward
            selected_sites.append((land, min(adventurers, number_of_guardians)))
            adventurers -= number_of_guardians
            if adventurers <= 0:
                break

        return selected_sites

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        The method calculates the maximum amount of reward you can make with different adventurer numbers.

        Args:
            adventure_numbers (list[int]): A list indicating the number of adventurers for each of the configuration.

        Returns:
            list[float]: A list containing the amount of reward you could make for each of the configuration (corresponding to adventure_numbers).

        Complexity:
            Best case: 
            Worst case: O(A * N) where
                A is the length of adventure_numbers
                N is the number of land sites
        """
        # Create an empty list to store the maximum amount of reward for different adventure numbers
        rewards = []
        for adventure_number in adventure_numbers:
            selected_sites = self.select_sites(adventure_number)
            received = 0
            for land, sent_adventurers in selected_sites:
                gold = land.get_gold()
                guardians = land.get_guardians()
                if guardians == 0:
                    received += gold
                else:
                    received += min((sent_adventurers * gold) / guardians, gold) # Formula: min((c * r) / g, r)
            rewards.append(received)
        return rewards

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        The method is used to update the state of the land object.
        The method is called whenever an Island needs to be updated.

        Args:
            land (Land): The land object that needs to be updated.
            new_reward (float): The amount of reward to be updated for the particular land site (land).
            new_guardians (int): The number of guardians to be updated for the particular land site (land).

        Complexity:
            Best case: 
            Worst case: O(log(N)) where N is the number of land sites
        """
        # Remove the land site from the BinarySearchTree
        del self.sites[land.get_guardians() / land.get_gold()] # O(log(N))

        # Update the land site with the new amount of reward and the new number of guardians
        try:
            self.sites[new_guardians / new_reward] = land # O(CompK * log(N)) inserting at the bottom of the balanced tree
        except ZeroDivisionError:
            return