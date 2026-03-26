"""
Basic module with a single MA reaction A -> B.
"""

from framework.module_base import PyAntiGenModule

class BasicMAReaction(PyAntiGenModule):
    """
    Creates a simple MA reaction A -> B.
    """
    def build(self):
        Compartments = ['Comp1']
        for Comp in Compartments:
            # Define reaction properties
            Reaction_name = f"Basic_A_to_B_{Comp}"
            Reactants = f"[A_{Comp}]"
            Products = f"[B_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = "k_A_to_B"

        # Add the reaction to the model
        self.add_reaction(Reaction_name, Reactants, Products, Rate_type, Rate_eqtn_prototype)
