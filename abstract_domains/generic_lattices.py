from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Generic, Type

from abstract_domains.lattice import Lattice
from core.expressions import VariableIdentifier

L = TypeVar('L')


class StoreLattice(Lattice, Generic[L]):
    """A generic lattice that represents a mapping Var -> L for some other lattice L."""

    def __init__(self, variables: List[VariableIdentifier], element_lattice: Type[L]):
        """Create a store lattice that represents a mapping Var -> L for some other lattice L.

        :param variables: list of program variables
        :param element_lattice: type of lattice elements L
        """
        self._variables_list = variables
        self._element_lattice = element_lattice
        self._variables = None
        super().__init__()

    @property
    def variables(self):
        return self._variables

    def __repr__(self):
        variables = "\n".join("{} -> {} ".format(variable, value) for variable, value in self.variables.items())
        return variables

    # noinspection PyCallingNonCallable
    def default(self):
        self._variables = {variable: self._element_lattice().default() for variable in self._variables_list}
        return self

    # noinspection PyCallingNonCallable
    def bottom(self) -> 'StoreLattice[L]':
        self._variables = {variable: self._element_lattice().bottom() for variable in self._variables}
        return self

    # noinspection PyCallingNonCallable
    def top(self) -> 'StoreLattice[L]':
        self._variables = {variable: self._element_lattice().top() for variable in self._variables}
        return self

    def is_bottom(self) -> bool:
        return all(element.is_bottom() for element in self.variables.values())

    def is_top(self) -> bool:
        return all(element.is_top() for element in self.variables.values())

    def _less_equal(self, other: 'StoreLattice[L]') -> bool:
        return all(self.variables[var].less_equal(other.variables[var]) for var in self.variables)

    def _meet(self, other: 'StoreLattice[L]'):
        for var in self.variables:
            self.variables[var].meet(other.variables[var])
        return self

    def _join(self, other: 'StoreLattice[L]') -> 'StoreLattice[L]':
        for var in self.variables:
            self.variables[var].join(other.variables[var])
        return self

    def _widening(self, other: 'StoreLattice[L]'):
        return self._join(other)


class StackLattice(Lattice, Generic[L], metaclass=ABCMeta):
    """A generic lattice that represents a stack of elements of some other lattice L."""

    def __init__(self, element_lattice: Type[L], args_dict):
        """Create a stack lattice of elements of some other lattice L.

        :param element_lattice: type of lattice elements L
        """
        self._args_dict = args_dict
        self._element_lattice = element_lattice
        self._stack = None
        super().__init__()

    @property
    def stack(self):
        return self._stack

    def __repr__(self):
        return " | ".join(map(repr, self.stack))

    # noinspection PyCallingNonCallable
    def default(self):
        self._stack = [self._element_lattice(**self._args_dict).default()]
        return self

    @abstractmethod
    def push(self):
        """push an element on the stack"""

    @abstractmethod
    def pop(self):
        """pop an element from the stack"""

    def _less_equal(self, other: 'StackLattice[L]') -> bool:
        if len(self.stack) != len(other.stack):
            raise Exception("Stacks must be equally long")
        return all(l.less_equal(r) for l, r in zip(self.stack, other.stack))

    def _meet(self, other: 'StackLattice[L]'):
        if len(self.stack) != len(other.stack):
            raise Exception("Stacks must be equally long")
        for i, item in enumerate(self.stack):
            item.meet(other.stack[i])
        return self

    def _join(self, other: 'StackLattice[L]') -> 'StackLattice[L]':
        if len(self.stack) != len(other.stack):
            raise Exception("Stacks must be equally long")
        for i, item in enumerate(self.stack):
            item.join(other.stack[i])
        return self

    def _widening(self, other: 'StackLattice[L]'):
        return self._join(other)
