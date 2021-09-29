import pybamm


class EquipotentialPair(pybamm.current_collector.BaseModel):
    """
    A submodel for equipotential current collectors. We solve an equation for
    the current in each of the through-cell models (they behave like batteries
    in parallel).

    For details on the potential pair formulation see [1]_ and [2]_.

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel

    References
    ----------
    .. [1] R Timms, SG Marquis, V Sulzer, CP Please and SJ Chapman. “Asymptotic
           Reduction of a Lithium-ion Pouch Cell Model”. Submitted, 2020.
    .. [2] SG Marquis, R Timms, V Sulzer, CP Please and SJ Chapman. “A Suite of
           Reduced-Order Models of a Single-Layer Lithium-ion Pouch Cell”. In
           preparation, 2020.

    **Extends:** :class:`pybamm.current_collector.BaseModel`
    """

    def __init__(self, param):
        super().__init__(param)

        pybamm.citations.register("Timms2021")

    def get_fundamental_variables(self):

        phi_s_cn = pybamm.PrimaryBroadcast(0, "current collector")

        # Since the potential is uniform we solve for a scalar valued current
        # collector potential and then broadcast this to the current collector
        # domain
        phi_s_cp_scalar = pybamm.Variable(
            "Positive current collector potential (scalar)"
        )
        phi_s_cp = pybamm.PrimaryBroadcast(phi_s_cp_scalar, "current collector")

        variables = self._get_standard_current_collector_potential_variables(
            phi_s_cn, phi_s_cp, phi_s_cp_scalar
        )

        return variables

    def get_coupled_variables(self, variables):
        # TODO: grad not implemented for 2D yet
        i_cc = pybamm.Scalar(0)

        i_s = variables["Electrode current density"]
        i_boundary_cc = pybamm.boundary_value(i_s, "right")

        variables.update(self._get_standard_current_variables(i_cc, i_boundary_cc))

        return variables

    def set_algebraic(self, variables):

        param = self.param

        phi_s_cp_scalar = variables["Positive current collector potential (scalar)"]
        i_boundary_cc = variables["Current collector current density"]
        applied_current = variables["Total current density"]
        z = pybamm.standard_spatial_vars.z

        self.algebraic = {
            phi_s_cp_scalar: pybamm.Integral(i_boundary_cc, z)
            - applied_current / param.l_z,
        }

    def set_initial_conditions(self, variables):

        phi_s_cp_scalar = variables["Positive current collector potential (scalar)"]

        self.initial_conditions = {
            phi_s_cp_scalar: self.param.U_p_init - self.param.U_n_init,
        }

    def _get_standard_current_collector_potential_variables(
        self, phi_s_cn, phi_s_cp, phi_s_cp_scalar
    ):
        """
        A private function to obtain the standard variables which
        can be derived from the potentials in the current collector.

        Parameters
        ----------
        phi_s_cn : :class:`pybamm.Symbol`
            The potential in the negative current collector.
        phi_s_cp : :class:`pybamm.Symbol`
            The potential in the positive current collector (broadcasted to the
            current collector domain).
        phi_s_cp : :class:`pybamm.Symbol`
            The (scalar valued) potential in the positive current collector.

        Returns
        -------
        variables : dict
            The variables which can be derived from the potential in the
            current collector.
        """

        pot_scale = self.param.potential_scale
        U_ref = self.param.U_p_ref - self.param.U_n_ref
        phi_s_cp_dim = U_ref + phi_s_cp * pot_scale
        phi_s_cp_scalar_dim = U_ref + phi_s_cp_scalar * pot_scale

        # Local potential difference
        V_cc = phi_s_cp - phi_s_cn

        # Terminal voltage
        # Note phi_s_cn is always zero at the negative tab
        V = pybamm.boundary_value(phi_s_cp, "positive tab")
        V_dim = pybamm.boundary_value(phi_s_cp_dim, "positive tab")

        # Voltage is local current collector potential difference at the tabs, in 1D
        # this will be equal to the local current collector potential difference

        variables = {
            "Negative current collector potential": phi_s_cn,
            "Negative current collector potential [V]": phi_s_cn * pot_scale,
            "Positive current collector potential": phi_s_cp,
            "Positive current collector potential [V]": phi_s_cp_dim,
            "Positive current collector potential (scalar)": phi_s_cp_scalar,
            "Positive current collector potential (scalar) [V]": phi_s_cp_scalar_dim,
            "Local voltage": V_cc,
            "Local voltage [V]": U_ref + V_cc * pot_scale,
            "Terminal voltage": V,
            "Terminal voltage [V]": V_dim,
        }

        return variables
