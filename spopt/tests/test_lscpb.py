import os
import pickle

import geopandas
import numpy
import pandas
import pulp
import pytest
from shapely import Point, Polygon

from spopt.locate import LSCPB
from spopt.locate.base import FacilityModelBuilder


class TestSyntheticLocate:
    @pytest.fixture(autouse=True)
    def setup_method(self, network_instance) -> None:
        self.dirpath = os.path.join(os.path.dirname(__file__), "./data/")

        client_count, facility_count = 100, 5
        (
            self.clients_snapped,
            self.facilities_snapped,
            self.cost_matrix,
        ) = network_instance(client_count, facility_count)

        self.ai = numpy.random.randint(1, 12, client_count)

        self.clients_snapped["weights"] = self.ai

    def test_lscpb_from_cost_matrix(self):
        lscpb = LSCPB.from_cost_matrix(
            self.cost_matrix, 10, pulp.PULP_CBC_CMD(msg=False)
        )
        result = lscpb.solve()

        assert isinstance(result, LSCPB)

    def test_lscpb_from_cost_matrix_no_results(self):
        lscpb = LSCPB.from_cost_matrix(
            self.cost_matrix, 10, pulp.PULP_CBC_CMD(msg=False)
        )
        result = lscpb.solve(results=False)
        assert isinstance(result, LSCPB)

        with pytest.raises(AttributeError):
            result.cli2fac  # noqa: B018
        with pytest.raises(AttributeError):
            result.fac2cli  # noqa: B018
        with pytest.raises(AttributeError):
            result.backup_perc  # noqa: B018

    def test_lscpb_facility_client_array_from_cost_matrix(self):
        with open(self.dirpath + "lscpb_fac2cli.pkl", "rb") as f:
            lscpb_objective = pickle.load(f)

        lscpb = LSCPB.from_cost_matrix(
            self.cost_matrix, 8, pulp.PULP_CBC_CMD(msg=False)
        )
        lscpb = lscpb.solve()

        numpy.testing.assert_array_equal(
            numpy.array(lscpb.fac2cli, dtype=object),
            numpy.array(lscpb_objective, dtype=object),
        )

    def test_lscpb_client_facility_array_from_cost_matrix(self):
        with open(self.dirpath + "lscpb_cli2fac.pkl", "rb") as f:
            lscpb_objective = pickle.load(f)

        lscpb = LSCPB.from_cost_matrix(
            self.cost_matrix, 8, pulp.PULP_CBC_CMD(msg=False)
        )
        lscpb = lscpb.solve()

        numpy.testing.assert_array_equal(
            numpy.array(lscpb.cli2fac, dtype=object),
            numpy.array(lscpb_objective, dtype=object),
        )

    def test_lscpb_from_geodataframe(self):
        lscpb = LSCPB.from_geodataframe(
            self.clients_snapped,
            self.facilities_snapped,
            "geometry",
            "geometry",
            10,
            pulp.PULP_CBC_CMD(msg=False),
        )
        result = lscpb.solve()

        assert isinstance(result, LSCPB)

    def test_lscpb_facility_client_array_from_geodataframe(self):
        with open(self.dirpath + "lscpb_geodataframe_fac2cli.pkl", "rb") as f:
            lscpb_objective = pickle.load(f)

        lscpb = LSCPB.from_geodataframe(
            self.clients_snapped,
            self.facilities_snapped,
            "geometry",
            "geometry",
            8,
            pulp.PULP_CBC_CMD(msg=False),
        )
        lscpb = lscpb.solve()

        numpy.testing.assert_array_equal(
            numpy.array(lscpb.fac2cli, dtype=object),
            numpy.array(lscpb_objective, dtype=object),
        )

    def test_lscpb_client_facility_array_from_geodataframe(self):
        with open(self.dirpath + "lscpb_geodataframe_cli2fac.pkl", "rb") as f:
            lscpb_objective = pickle.load(f)

        lscpb = LSCPB.from_geodataframe(
            self.clients_snapped,
            self.facilities_snapped,
            "geometry",
            "geometry",
            8,
            pulp.PULP_CBC_CMD(msg=False),
        )
        lscpb = lscpb.solve()

        numpy.testing.assert_array_equal(
            numpy.array(lscpb.cli2fac, dtype=object),
            numpy.array(lscpb_objective, dtype=object),
        )

    def test_lscpb_preselected_facility_client_array_from_geodataframe(self):
        with open(
            self.dirpath + "lscpb_preselected_loc_geodataframe_fac2cli.pkl", "rb"
        ) as f:
            lscpb_objective = pickle.load(f)

        fac_snapped = self.facilities_snapped.copy()
        fac_snapped["predefined_loc"] = numpy.array([0, 0, 0, 0, 1])

        lscpb = LSCPB.from_geodataframe(
            self.clients_snapped,
            fac_snapped,
            "geometry",
            "geometry",
            8,
            pulp.PULP_CBC_CMD(msg=False, warmStart=True),
            predefined_facility_col="predefined_loc",
        )
        lscpb = lscpb.solve()

        numpy.testing.assert_array_equal(
            numpy.array(lscpb.fac2cli, dtype=object),
            numpy.array(lscpb_objective, dtype=object),
        )


class TestRealWorldLocate:
    def setup_method(self) -> None:
        self.dirpath = os.path.join(os.path.dirname(__file__), "./data/")
        network_distance = pandas.read_csv(
            self.dirpath
            + "SF_network_distance_candidateStore_16_censusTract_205_new.csv"
        )

        ntw_dist_piv = network_distance.pivot_table(
            values="distance", index="DestinationName", columns="name"
        )

        self.cost_matrix = ntw_dist_piv.to_numpy()

        demand_points = pandas.read_csv(
            self.dirpath + "SF_demand_205_centroid_uniform_weight.csv"
        )
        facility_points = pandas.read_csv(self.dirpath + "SF_store_site_16_longlat.csv")

        self.facility_points_gdf = (
            geopandas.GeoDataFrame(
                facility_points,
                geometry=geopandas.points_from_xy(
                    facility_points.long, facility_points.lat
                ),
            )
            .sort_values(by=["NAME"])
            .reset_index()
        )

        self.demand_points_gdf = (
            geopandas.GeoDataFrame(
                demand_points,
                geometry=geopandas.points_from_xy(
                    demand_points.long, demand_points.lat
                ),
            )
            .sort_values(by=["NAME"])
            .reset_index()
        )

        self.service_dist = 5000.0
        self.p_facility = 4
        self.ai = self.demand_points_gdf["POP2000"].to_numpy()

    def test_optimality_lscpb_from_cost_matrix(self):
        lscpb = LSCPB.from_cost_matrix(
            self.cost_matrix, self.service_dist, pulp.PULP_CBC_CMD(msg=False)
        )
        lscpb = lscpb.solve()

        assert lscpb.problem.status == pulp.LpStatusOptimal

    def test_infeasibility_lscpb_from_cost_matrix(self, loc_raises_infeasible):
        with loc_raises_infeasible:
            lscpb = LSCPB.from_cost_matrix(
                self.cost_matrix, 20, pulp.PULP_CBC_CMD(msg=False)
            )
            lscpb.solve()

    def test_mixin_lscpb_get_percentage(self):
        percentage_expected = 81.46341463414633
        lscpb = LSCPB.from_cost_matrix(
            self.cost_matrix, self.service_dist, pulp.PULP_CBC_CMD(msg=False)
        )
        lscpb = lscpb.solve()

        assert lscpb.backup_perc == pytest.approx(percentage_expected)

    def test_optimality_lscpb_from_geodataframe(self):
        lscpb = LSCPB.from_geodataframe(
            self.demand_points_gdf,
            self.facility_points_gdf,
            "geometry",
            "geometry",
            self.service_dist,
            pulp.PULP_CBC_CMD(msg=False),
        )
        lscpb = lscpb.solve()

        assert lscpb.problem.status == pulp.LpStatusOptimal

    def test_infeasibility_lscpb_from_geodataframe(self, loc_raises_infeasible):
        with loc_raises_infeasible:
            lscpb = LSCPB.from_geodataframe(
                self.demand_points_gdf,
                self.facility_points_gdf,
                "geometry",
                "geometry",
                0,
                pulp.PULP_CBC_CMD(msg=False),
            )
            lscpb.solve()


class TestErrorsWarnings:
    @pytest.fixture(autouse=True)
    def setup_method(self, loc_warns_geo_crs) -> None:
        pol1 = Polygon([(0, 0), (1, 0), (1, 1)])
        pol2 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        pol3 = Polygon([(2, 0), (3, 0), (3, 1), (2, 1)])
        polygon_dict = {"geometry": [pol1, pol2, pol3]}

        point = Point(10, 10)
        point_dict = {"weight": 4, "geometry": [point]}

        self.gdf_fac = geopandas.GeoDataFrame(polygon_dict, crs="EPSG:4326")
        self.gdf_dem = geopandas.GeoDataFrame(point_dict, crs="EPSG:4326")

        self.gdf_dem_crs = self.gdf_dem.to_crs("EPSG:3857")

        self.gdf_dem_buffered = self.gdf_dem.copy()
        with loc_warns_geo_crs:
            self.gdf_dem_buffered["geometry"] = self.gdf_dem.buffer(2)

    def test_error_lscpb_different_crs(
        self, loc_warns_mixed_type_fac, loc_raises_diff_crs, loc_warns_geo_crs
    ):
        with loc_warns_mixed_type_fac, loc_raises_diff_crs, loc_warns_geo_crs:
            LSCPB.from_geodataframe(
                self.gdf_dem_crs,
                self.gdf_fac,
                "geometry",
                "geometry",
                10,
                pulp.PULP_CBC_CMD(msg=False),
            )

    def test_warning_lscpb_demand_geodataframe(
        self, loc_warns_mixed_type_dem, loc_warns_mixed_type_fac, loc_warns_geo_crs
    ):
        with loc_warns_mixed_type_dem, loc_warns_mixed_type_fac, loc_warns_geo_crs:
            LSCPB.from_geodataframe(
                self.gdf_dem_buffered,
                self.gdf_fac,
                "geometry",
                "geometry",
                100,
                pulp.PULP_CBC_CMD(msg=False),
            )

    def test_attribute_error_add_backup_covering_constraint(self):
        with pytest.raises(AttributeError, match="Before setting backup coverage"):
            dummy_class = LSCPB(
                "dummy", pulp.LpProblem("name"), pulp.PULP_CBC_CMD(msg=False)
            )
            dummy_fac_r = 0
            dummy_cli_r = 0
            FacilityModelBuilder.add_backup_covering_constraint(
                dummy_class,
                dummy_fac_r,
                dummy_cli_r,
            )
