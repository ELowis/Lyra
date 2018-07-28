from copy import deepcopy
from typing import Set

from lyra.abstract_domains.data_structures.key_wrapper import KeyWrapper
from lyra.abstract_domains.data_structures.scalar_wrapper import ScalarWrapper
from lyra.abstract_domains.data_structures.value_wrapper import ValueWrapper
from lyra.abstract_domains.lattice import Lattice
from lyra.abstract_domains.numerical.interval_domain import IntervalState, IntervalLattice
from lyra.core.expressions import VariableIdentifier
from lyra.core.utils import copy_docstring


class IntervalSWrapper(ScalarWrapper, IntervalState):
    """Wrapper around IntervalState for scalar domain of DictContentState"""

    def __init__(self, scalar_variables: Set[VariableIdentifier]):
        super().__init__(scalar_variables)

    @copy_docstring(ScalarWrapper.add_var)
    def add_var(self, var: VariableIdentifier):
        if var not in self.store.keys():
            self.variables.add(var)
            self.store[var] = IntervalLattice()     # top
        else:
            raise ValueError(f"Variable can not be added to a store if it is already present")

    @copy_docstring(ScalarWrapper.remove_var)
    def remove_var(self, var: VariableIdentifier):
        if var in self.store.keys():
            self.variables.remove(var)
            del self.store[var]
        else:
            raise ValueError(f"Variable can only be removed from a store if it is already present")

    @copy_docstring(ScalarWrapper.invalidate_var)
    def invalidate_var(self, var: VariableIdentifier):
        self.store[var].top()


class IntervalKWrapper(KeyWrapper, IntervalSWrapper):
    """Wrapper around IntervalState for key domain of DictContentState"""

    def __init__(self, scalar_variables: Set[VariableIdentifier], k_var: VariableIdentifier):
        super().__init__(scalar_variables, k_var)

    @copy_docstring(KeyWrapper.decomp)
    def decomp(self, state: 'IntervalKWrapper', exclude: 'IntervalKWrapper') \
            -> Set['IntervalKWrapper']:
        left = deepcopy(state)  # left & right non-exclude
        right = deepcopy(state)

        k_state = state.store[state.k_var]
        k_exclude = exclude.store[state.k_var]
        if k_state.is_bottom():
            left.store[state.k_var].bottom()
            right.store[state.k_var].bottom()
        elif k_exclude.is_bottom():
            left.store[state.k_var] = IntervalLattice(k_state.lower, k_state.upper)
            right.store[state.k_var].bottom()
        elif k_exclude.is_top():  # exclude everything
            left.store[state.k_var].bottom()
            right.store[state.k_var].bottom()
        else:
            left.store[state.k_var] = IntervalLattice(k_state.lower,
                                                      k_exclude.lower - 1)  # bottom if empty
            right.store[state.k_var] = IntervalLattice(k_exclude.upper + 1,
                                                       k_state.upper)  # bottom if empty

        return {left, right}

    @copy_docstring(KeyWrapper.is_singleton)
    def is_singleton(self) -> bool:
        key_interval = self.store[self.k_var]
        return (not key_interval.is_bottom()) and (key_interval.lower == key_interval.upper)

    def __eq__(self, other: 'Lattice'):
        return isinstance(other, self.__class__) and repr(self) == repr(other)

    def __ne__(self, other: 'Lattice'):
        return not (self == other)

    def __hash__(self):
        return hash(repr(self))

    @copy_docstring(KeyWrapper.__lt__)
    def __lt__(self, other):
        if isinstance(other, IntervalKWrapper):
            s_upper = self.store[self.k_var].upper
            o_lower = other.store[other.k_var].lower
            if s_upper < o_lower:   # other boundaries should conform with interval property by def
                return True
            else:
                return False
        return NotImplemented

    @copy_docstring(KeyWrapper.is_bottom)
    def is_bottom(self):
        return self.store[self.k_var].is_bottom()


class IntervalVWrapper(ValueWrapper, IntervalSWrapper):
    """Wrapper around IntervalState for value domain of DictContentState"""

    def __init__(self, scalar_variables: Set[VariableIdentifier], v_var: VariableIdentifier):
        super().__init__(scalar_variables, v_var)

    @copy_docstring(KeyWrapper.is_bottom)
    def is_bottom(self):
        return self.store[self.v_var].is_bottom()

    def __eq__(self, other: 'Lattice'):
        return isinstance(other, self.__class__) and repr(self) == repr(other)

    def __ne__(self, other: 'Lattice'):
        return not (self == other)

    def __hash__(self):
        return hash(repr(self))