from landsites import Land
from data_structures.bst import BinarySearchTree
from data_structures.node import TreeNode


class Mode1Navigator:
    """
    This class represents a navigator that helps adventurers to select the land sites to attack.
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        This method perform initialisation.

        Args:
            sites (list[Land]): A list that holds the initial states of the land sites.
            adventurers (int): The total number of adventurers c you are going to take with you on your journey.

        Complexity:
            Best case:
            Worst case: O(N*log(N)) where N is the number land sites
        """
        # Initialise a BinarySearchTree where each TreeNode contains the ratio of guardians to reward as its key and the land site as its item       
        self.sites = BinarySearchTree()
        for land in sites: # O(N) where N is the number of land sites
            self.sites[land.get_ratio()] = land # O(CompK * log(N)) inserting at the bottom of the balanced tree
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
            if adventurers <= 0:
                break
            land: Land = tree_node.item
            number_of_guardians = land.get_guardians()
            # If the land site has more guardians than adventurers then send all the adventurers there
            if number_of_guardians > adventurers:
                selected_sites.append((land, adventurers))
                adventurers = 0
            # Otherwise, send the number of adventurers that matches the number of guardians to max out the reward
            else:
                selected_sites.append((land, number_of_guardians))
                adventurers -= number_of_guardians

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
            Worst case: O(A * N) or O(N + A log(A)) where
                A is the length of adventure_numbers
                N is the number of land sites
        """
        # Create an empty list to store the maximum amount of reward for different adventure numbers
        rewards = []
        for adventure_number in adventure_numbers:
            # Choose the land site that gives the maximum amount of reward for the particular adventure number
            selected_sites = self.select_sites(adventure_number)
            reward = 0

            for land, adventurers in selected_sites:
                gold_count = land.get_gold()
                reward += min((adventurers * gold_count) / land.get_guardians(), gold_count) # Formula: min((c * r) / g, r)
            rewards.append(reward)

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
        del self.sites[land.get_ratio()]

        # Update the land site with the new amount of reward and the new number of guardians
        self.sites[new_guardians / new_reward] = land


if __name__ == "__main__":
    # Create the land sites
    a = Land("A", 400, 100)
    b = Land("B", 300, 150)
    c = Land("C", 100, 5)
    d = Land("D", 350, 90)
    e = Land("E", 300, 100)
    # Create deepcopies of the sites
    sites = [
        Land(a.get_name(), a.get_gold(), a.get_guardians()),
        Land(b.get_name(), b.get_gold(), b.get_guardians()),
        Land(c.get_name(), c.get_gold(), c.get_guardians()),
        Land(d.get_name(), d.get_gold(), d.get_guardians()),
        Land(e.get_name(), e.get_gold(), e.get_guardians()),
    ]

    nav = Mode1Navigator(sites, 200)
    results = nav.select_sites_from_adventure_numbers([0, 200, 500, 300, 40])
    print(results) # [0, 865, 1450, 1160, 240]

    print(nav.sites.draw())