import collections
from typing import Any, Dict, List

from ochrona.model.confirmed_vulnerability import Vulnerability
from ochrona.model.dependency import Dependency


class DependencySet:
    """
    A Top level dependencies object for a scan.
    """

    _dependencies: List[Dependency] = []
    _flat_list: List[str] = []
    _confirmed_vulnerabilities: List[Vulnerability] = []
    _policy_violations: List[Dict[str, Any]] = []

    def __init__(self, dependencies=[]):
        self._dependencies = dependencies
        self._flat_list = list(self._flatten_dependencies(dependencies))

    def _flatten_dependencies(self, dependencies):
        """
        Flattens resolved transitive dependencies into a flat list.
        """
        flat_list = []
        for dependency in dependencies:
            flat_list.append(dependency.full)
        return set(flat_list)

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def flat_list(self):
        return self._flat_list

    @property
    def confirmed_vulnerabilities(self):
        return self._confirmed_vulnerabilities

    @confirmed_vulnerabilities.setter
    def confirmed_vulnerabilities(self, confirmed_vulnerabilities: List[Vulnerability]):
        """
        Updates the vuln finding results for `PythonDependencies`
        """
        self._confirmed_vulnerabilities = confirmed_vulnerabilities

    @property
    def policy_violations(self):
        return self._policy_violations

    @policy_violations.setter
    def policy_violations(self, policy_violations=[]):
        self._policy_violations = policy_violations

    def to_json(self):
        """
        Dumps object to json.
        """
        return json.dumps(self.__dict__, default=complex_handler)


def complex_handler(obj):
    """
    Handles nested serialization to JSON.
    """
    if hasattr(obj, "to_json"):
        return obj.to_json()
    raise TypeError(
        "Object of type {} with value of {} is not JSON serializable".format(
            type(obj), repr(obj)
        )
    )


def flatten(lst):
    """
    Flattens a list of lists (..n) into a single dimension list
    """
    for elem in lst:
        if isinstance(elem, collections.Iterable) and not isinstance(
            elem, (str, bytes)
        ):
            yield from flatten(elem)
        else:
            yield elem
