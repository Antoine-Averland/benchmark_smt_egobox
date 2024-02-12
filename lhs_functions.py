from smt.sampling_methods import LHS
import egobox as egx


def smt_lhs_opti(xlimits, num_points):
    sampling = LHS(xlimits=xlimits, criterion="ese", random_state=42)
    sampling(num_points)


def egobox_lhs_opti(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    egx.lhs(xspecs, num_points)


def smt_lhs_classic(xlimits, num_points):
    sampling = LHS(xlimits=xlimits)
    sampling(num_points)


def egobox_lhs_classic(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_CLASSIC, xspecs, num_points)


def smt_lhs_centered(xlimits, num_points):
    sampling = LHS(xlimits=xlimits, criterion="center")
    sampling(num_points)


def egobox_lhs_centered(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_CENTERED, xspecs, num_points)


def smt_lhs_maximin(xlimits, num_points):
    sampling = LHS(xlimits=xlimits, criterion="maximin")
    sampling(num_points)


def egobox_lhs_maximin(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_MAXIMIN, xspecs, num_points)


def smt_lhs_centered_maximin(xlimits, num_points):
    sampling = LHS(xlimits=xlimits, criterion="centermaximin")
    sampling(num_points)


def egobox_lhs_centered_maximin(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_CENTERED_MAXIMIN, xspecs, num_points)
