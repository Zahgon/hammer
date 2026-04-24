import json
import os
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Union
import networkx as nx
from hammer.logging import HammerVLSILogging
from hammer.vlsi.cli_driver import CLIDriver

class Status(Enum):
    """Represents the status of a node in the flowgraph."""
    NOT_RUN = 'NOT_RUN'
    RUNNING = 'RUNNING'
    INCOMPLETE = 'INCOMPLETE'
    INVALID = 'INVALID'
    COMPLETE = 'COMPLETE'

@dataclass
class Node:
    """Defines a node for an action in a flowgraph.

    Returns:
        Node: Complete description of an action.
    """
    action: str
    tool: str
    pull_dir: str
    push_dir: str
    required_inputs: list[str]
    required_outputs: list[str]
    status: Status = Status.NOT_RUN
    driver: CLIDriver = field(default_factory=CLIDriver)
    optional_inputs: list[str] = field(default_factory=list)
    optional_outputs: list[str] = field(default_factory=list)
    step_controls: dict[str, str] = field(default_factory=lambda: {'start_before_step': '', 'start_after_step': '', 'stop_before_step': '', 'stop_after_step': '', 'only_step': ''})

    def __key(self) -> tuple:
        """Key value for hashing.

        Returns:
            tuple: All fields concatenated.
        """
        pass

    def __hash__(self) -> int:
        """Dunder method for uniquely hashing a `Node` object.

        Returns:
            int: Hash of a `Node`.
        """
        return hash(self.__key)

    def __is_privileged(self) -> bool:
        """Private method for checking if
        step control is applied to a `Node`.

        Returns:
            bool: If the node is allowed to be the starting point of a flow.
        """
        pass

    @property
    def privileged(self) -> bool:
        """Property for determining node privilege.

        Returns:
            bool: If the node is allowed to be the starting point of a flow.
        """
        pass

class NodeEncoder(json.JSONEncoder):

    def default(self, o: Any) -> Any:
        pass

def as_node(dct: dict) -> Union[Node, dict]:
    pass

@dataclass
class Graph:
    """Defines a flowgraph.

    Returns:
        Graph: HAMMER flowgraph.
    """
    edge_list: dict[Node, list[Node]]
    auto_auxiliary: bool = True

    def __post_init__(self) -> None:
        self.networkx = nx.DiGraph(Graph.insert_auxiliary_actions(self.edge_list) if self.auto_auxiliary else self.edge_list)

    def verify(self) -> bool:
        """Checks if a graph is valid via its inputs and outputs.

        Returns:
            bool: If graph is valid.
        """
        pass

    def __process(self, v: Node) -> bool:
        """Process a specific vertex of a graph.

        Args:
            v (Node): Node to check the validity of.

        Returns:
            bool: If the particular node is valid.
        """
        pass

    @staticmethod
    def insert_auxiliary_actions(edge_list: dict[Node, list[Node]]) -> dict[Node, list[Node]]:
        """Inserts x-to-y actions between two semantically related actions (e.g. if syn and par are connected, then we have to insert a syn-to-par node here).

        Args:
            edge_list (dict[Node, list[Node]]): Edge list without auxiliary actions.

        Returns:
            dict[Node, list[Node]]: Transformed edge list with auxiliary actions.
        """
        pass

    def run(self, start: Node) -> Any:
        """Runs a flowgraph.

        Args:
            start (Node): Node to start the run on.

        Raises:
            RuntimeError: If the flowgraph is invalid.
            RuntimeError: If the starting node is not in the flowgraph.
        """
        pass

    @staticmethod
    def __run_single(node: Node) -> int:
        """Helper function to run a HAMMER node.

        Args:
            node (Node): Node to run action on.

        Returns:
            int: Status code.
        """
        pass

    def to_mermaid(self) -> str:
        """Converts the flowgraph into Mermaid format for visualization.

        Args:
            fname (str): Output file name.

        Returns:
            str: Path to Mermaid Markdown file.
        """
        pass

def convert_to_acyclic(g: Graph) -> Graph:
    """Eliminates cycles in a flowgraph for analysis.

    Args:
        g (Graph): (presumably) cyclic graph to transform.

    Returns:
        Graph: Graph with cloned nodes.
    """
    pass
