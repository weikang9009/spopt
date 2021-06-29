from abc import ABC, abstractmethod, abstractproperty
import pulp
from geopandas import GeoDataFrame
import numpy as np
from typing import Type, TypeVar


class LocateSolver(ABC):
    @abstractmethod
    def solve(self, solver: pulp.LpSolver):
        pass


T_FacModel = TypeVar("T_FacModel", bound=LocateSolver)


class FacilityModelBuilder(object):
    """
    Set Constraints and Variables
    """

    @staticmethod
    def add_facility_integer_variable(obj: T_FacModel, range_facility, var_name):
        fac_vars = [
            pulp.LpVariable(
                var_name.format(i=i), lowBound=0, upBound=1, cat=pulp.LpInteger
            )
            for i in range_facility
        ]

        setattr(obj, "fac_vars", fac_vars)

    @staticmethod
    def add_client_integer_variable(obj: T_FacModel, range_client, var_name):
        cli_vars = [
            pulp.LpVariable(
                var_name.format(i=i), lowBound=0, upBound=1, cat=pulp.LpInteger
            )
            for i in range_client
        ]

        setattr(obj, "cli_vars", cli_vars)

    @staticmethod
    def add_client_assign_integer_variable(
        obj: T_FacModel, range_client, range_facility, var_name
    ):
        cli_assgn_vars = [
            [
                pulp.LpVariable(
                    var_name.format(i=i, j=j), lowBound=0, upBound=1, cat=pulp.LpInteger
                )
                for j in range_facility
            ]
            for i in range_client
        ]

        setattr(obj, "cli_assgn_vars", cli_assgn_vars)

    @staticmethod
    def add_weight_continuous_variable(obj: T_FacModel):
        weight_var = pulp.LpVariable("W", lowBound=0, cat=pulp.LpContinuous)

        setattr(obj, "weight_var", weight_var)

    @staticmethod
    def add_set_covering_constraint(
        obj: T_FacModel, model, ni, range_facility, range_client
    ):
        try:
            fac_vars = getattr(obj, "fac_vars")
            for i in range_client:
                model += (
                    pulp.lpSum([ni[i][j] * fac_vars[j] for j in range_facility]) >= 1
                )
        except AttributeError:
            raise Exception("before setting constraints must set facility variable")

    @staticmethod
    def add_facility_constraint(obj: T_FacModel, model, p_facilities):
        try:
            fac_vars = getattr(obj, "fac_vars")
            model += pulp.lpSum(fac_vars) == p_facilities
        except AttributeError:
            raise Exception("before setting constraints must set facility variable")

    @staticmethod
    def add_maximal_coverage_constraint(
        obj: T_FacModel, model, ni, range_facility, range_client
    ):
        try:
            fac_vars = getattr(obj, "fac_vars")
            dem_vars = getattr(obj, "cli_vars")
            for i in range_client:
                model += (
                    pulp.lpSum([ni[i][j] * fac_vars[j] for j in range_facility])
                    >= dem_vars[i]
                )
        except AttributeError:
            raise Exception("before setting constraints must set facility variable")

    @staticmethod
    def add_assignment_constraint(obj: T_FacModel, model, range_facility, range_client):
        try:
            cli_assgn_vars = getattr(obj, "cli_assgn_vars")

            for i in range_client:
                model += pulp.lpSum([cli_assgn_vars[i][j] for j in range_facility]) == 1
        except AttributeError:
            raise Exception("before setting constraints must set facility variable")

    @staticmethod
    def add_opening_constraint(obj: T_FacModel, model, range_facility, range_client):
        try:
            cli_assgn_vars = getattr(obj, "cli_assgn_vars")
            fac_vars = getattr(obj, "fac_vars")

            for i in range_client:
                for j in range_facility:
                    model += fac_vars[j] - cli_assgn_vars[i][j] >= 0
        except AttributeError:
            raise Exception("before setting constraints must set facility variable")

    @staticmethod
    def add_minimized_maximum_constraint(
        obj: T_FacModel, model, cost_matrix, range_facility, range_client
    ):
        try:
            cli_assgn_vars = getattr(obj, "cli_assgn_vars")
            weight_var = getattr(obj, "weight_var")

            for i in range_client:
                model += (
                    pulp.lpSum(
                        [
                            cli_assgn_vars[i][j] * cost_matrix[i][j]
                            for j in range_facility
                        ]
                    )
                    <= weight_var
                )
        except AttributeError:
            raise Exception("before setting constraints must set facility variable")
