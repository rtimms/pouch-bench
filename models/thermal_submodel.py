#
# Class for one-dimensional thermal submodel for use in the "1+1D" pouch cell model
#
import pybamm


class HeatEquation1D(pybamm.thermal.pouch_cell.CurrentCollector1D):
    """
    Class for one-dimensional thermal submodel for use in the "1+1D" pouch cell
    model, with no Newton cooling and a fixed temperature on the top and bottom
    surfaces of the pouch. For more information see [1]_ and [2]_.

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel

    References
    ----------
    .. [1] R Timms, SG Marquis, V Sulzer, CP Please and SJ Chapman. “Asymptotic
           Reduction of a Lithium-ion Pouch Cell Model”. In preparation, 2020.
    .. [2] SG Marquis, R Timms, V Sulzer, CP Please and SJ Chapman. “A Suite of
           Reduced-Order Models of a Single-Layer Lithium-ion Pouch Cell”. In
           preparation, 2020.

    **Extends:** :class:`pybamm.thermal.pouch_cell.CurrentCollector1D`
    """

    def set_rhs(self, variables):
        T_av = variables["X-averaged cell temperature"]
        Q_av = variables["X-averaged total heating"]

        self.rhs = {
            T_av: (pybamm.laplacian(T_av) + self.param.B * Q_av)
            / (self.param.C_th * self.param.rho(T_av))
        }

    def set_boundary_conditions(self, variables):
        T_amb = variables["Ambient temperature"]
        T_av = variables["X-averaged cell temperature"]

        # left = bottom of cell (z=0)
        # right = top of cell (z=L_z)
        self.boundary_conditions = {
            T_av: {
                "left": (
                    T_amb,
                    "Dirichlet",
                ),
                "right": (
                    T_amb,
                    "Dirichlet",
                ),
            }
        }

    def set_initial_conditions(self, variables):
        T_av = variables["X-averaged cell temperature"]
        self.initial_conditions = {T_av: self.param.T_init}
