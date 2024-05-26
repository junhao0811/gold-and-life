from landsites import Land
from data_structures.bst import BinarySearchTree
from data_structures.node import TreeNode


class Mode1Navigator:
    """
    This class is to guide adventurers to help them select the best land sites to visit in order to maximise their rewards.

    The navigator uses a BinarySearchTree to store the land sites where the key is the ratio of guardians to reward and the item is the land site.
    Using BinarySearchTree can utilize in-order traversal to traverse the tree in order to maximise the rewards of the adventurers.
    
    The select_sites method selects the land sites the navigator desire to attack by iterating through the BinarySearchTree.
    The select_sites_from_adventure_numbers method calculates the maximum amount of reward that can be made with different adventurer numbers.
    The update_site method is used to update the state of the land object.

    Another data structure used in this class is list, which is used to store the selected land sites and the number of adventurers the navigator will be sending to the corresponding land site.
    A data type used in this class is Land, which represents the land site object.

    Example:
        Given the BinarySearchTree with the following guardians to reward ratios:
                                    0.6
                                  /     \
                                0.4      0.8
                               /   \     /  \
                              0.3  0.5  0.7  0.9

        By using in-order traversal, it will produce a sorted output -> 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
        The time complexity of this action will be O(N) because we need to visit each and every tree node in-order to produce the output above,
        where N is the number of nodes in the tree.

        The output enables us to know how to maximise the reward for the adventure team as the lowest ratio of guardians to reward will be selected first, which is 0.3 in this case.
        
    Complexity:
        __init__:
            The best and worst case will cost O(N log(N)) when looping through the list of land sites whilst inserting it at the bottom of the balanced tree
            where N is the number land sites.
            
        select_sites:
            The best case is when we need to traverse until the leftmost node of the balanced tree to start the in-order traversal, and all the adventurers are sent there which will trigger the break condition of the loop,
            which will cost O(log(N)) for the traversal only until the first tree node, where N is the number of land sites.

            The worst case is when we need to traverse each and every node in the tree in in-order, which will be O(N), where N is the number of land sites.

        select_sites_from_adventure_numbers:
            The best case will cost O(A log(N)) when we iterate through the list of adventure numbers and in each iteration, all the adventurers are sent to the land site which will trigger the break condition in select_sites method

            The worst case will cost O(A * N) when we iterate through the list of adventure numbers and in each iteration,
            we still need to loop through the list of land sites to calculate the maximum amount of reward that can be made by each adventurer number.
            where A is the length of adventure_numbers and N is the number of land sites and N is the number of land sites.

        update_site:
            The best and worst case will cost O(log(N)) when we remove the land site from the BinarySearchTree and insert the land site with the new amount of reward and the new number of guardians at the bottom of the balanced tree,
            which actually costs O(log(N) + log(N)) = O(2 log(N)), ignoring the constant factor, where N is the number of land sites.
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        This method perform initialisation.

        Args:
            sites (list[Land]): A list that holds the initial states of the land sites.
            adventurers (int): The total number of adventurers c you are going to take with you on your journey.

        Complexity: O(N log(N)) for best/worst case when looping through the list of land sites whilst inserting it at the bottom of the balanced tree
            Where N is the number land sites
        """
        # Initialise a BinarySearchTree where each TreeNode contains the ratio of guardians to reward as its key and the land site as its item       
        self.sites = BinarySearchTree()
        for land in sites:
            try:
                self.sites[land.get_guardians() / land.get_gold()] = land
            except ZeroDivisionError:
                continue
        self.adventurers = adventurers

    def select_sites(self, adventurers: int | None = None) -> list[tuple[Land, int]]:
        """
        The method shall selects the land sites you desire to attack.

        Args:
            adventurers (int | None): The number of adventurers to be sent to the land site.

        Returns:
            list[tuple[Land, int]]: A list of pairs (in tuple data type) where each pair containing a land object
                                    and the number of adventurers you will be sending to the corresponding land site.

        Complexity:
            Best case: O(log(N)) when traversing until the leftmost tree node of the balanced tree to start the in-order traversal,
                       and all the adventurers are sent there which will trigger the break condition of the loop,
                       which will only cost O(log(N)) for the traversal until the first tree node, where N is the number of land sites.

            Worst case: O(N) when we need to traverse each and every node in the tree in in-order to select all of the land sites
                Where N is the number of land sites
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
            Best case: O(A log(N)) when we iterate through the list of adventure numbers and in each iteration,
                       all the adventurers are sent to the land site which will trigger the break condition in select_sites method for each adventure number

            Worst case: O(A * N) when we iterate through the list of adventure numbers and in each iteration,
                        we still need to loop through the list of land sites to calculate the maximum amount of reward that can be made by each adventurer number.

                Where A is the length of adventure_numbers
                Where N is the number of land sites
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
            O(log(N)) for best/worst case when removing the land site from the BinarySearchTree and 
                    inserting the land site with the new amount of reward and the new number of guardians at the bottom of the balanced tree

            Where N is the number of land sites
        """
        # Delete the land site from the BinarySearchTree
        del self.sites[land.get_guardians() / land.get_gold()]
        
        # Update the land site with the new amount of reward and the new number of guardians
        land.set_gold(new_reward)
        land.set_guardians(new_guardians)

        # Insert the land site with the ratio of guardians to reward as its key and the land site as its item
        try:
            self.sites[new_guardians / new_reward] = land
        except ZeroDivisionError:
            return