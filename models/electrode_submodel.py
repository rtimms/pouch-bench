import pybamm


class FullPotentiostatic(pybamm.electrode.ohm.Full):
    """
    Full model of electrode employing Ohm's law with specified potential at
    the positive electrode/current collector interface.

    Parameters
    ----------
    param : parameter class
        The parameters to use for this submodel
    domain : str
        Either 'Negative' or 'Positive'
    options : dict, optional
        A dictionary of options to be passed to the model.

    **Extends:** :class:`pybamm.electrode.ohm.Full`
    """

    def __init__(self, param, domain, options=None):
        super().__init__(param, domain, options=options)
        self.set_positive_potential = False

    def set_boundary_conditions(self, variables):

        phi_s = variables[self.domain + " electrode potential"]

        if self.domain == "Negative":
            phi_s_cn = variables["Negative current collector potential"]
            lbc = (phi_s_cn, "Dirichlet")
            rbc = (pybamm.Scalar(0), "Neumann")

        elif self.domain == "Positive":
            phi_s_cp = variables["Positive current collector potential"]
            lbc = (pybamm.Scalar(0), "Neumann")
            rbc = (
                phi_s_cp,
                "Dirichlet",
            )

        self.boundary_conditions[phi_s] = {"left": lbc, "right": rbc}
