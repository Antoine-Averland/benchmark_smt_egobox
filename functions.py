from smt.sampling_methods import LHS
import egobox as egx

type_lhs = {
    "classic": "c",
    "opti": "ese",
    "centered": "center",
    "maximin": "maximin",
    "centered_maximin": "centermaximin",
}
type_ego = {
    "classic": egx.Sampling.LHS_CLASSIC,
    "opti": "",
    "centered": egx.Sampling.LHS_CENTERED,
    "maximin": egx.Sampling.LHS_MAXIMIN,
    "centered_maximin": egx.Sampling.LHS_CENTERED_MAXIMIN,
}


def smt_lhs(xlimits, num_points, args):
    sampling = LHS(xlimits=xlimits, criterion=type_lhs[args])
    sampling(num_points)


def egobox_lhs(xlimits, num_points, args):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(type_ego[args], xspecs, num_points)


def egobox_lhs_opti(xlimits, num_points, args):
    xspecs = egx.to_specs(xlimits)
    egx.lhs(xspecs, num_points)


def egobox_lhs_classic(xlimits, num_points, args):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_CLASSIC, xspecs, num_points)


def egobox_lhs_centered(xlimits, num_points, args):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_CENTERED, xspecs, num_points)


def egobox_lhs_maximin(xlimits, num_points, args):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_MAXIMIN, xspecs, num_points)


def egobox_lhs_centered_maximin(xlimits, num_points, args):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_CENTERED_MAXIMIN, xspecs, num_points)
