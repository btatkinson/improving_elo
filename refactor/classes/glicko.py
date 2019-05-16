import numpy as np
import pandas as pd
import math

from settings import *

MU = glicko_set['init']
PHI = glicko_set['phi']
SIGMA = glicko_set['sigma']
TAU = glicko_set['tau']
EPSILON = glicko_set['epsilon']
Q = math.log(10)/400
ratio = 173.7178

# class Rating(object):
#
#     def __init__(self, mu=MU, phi=PHI, sigma=SIGMA):
#         self.mu = mu
#         self.phi = phi
#         self.sigma = sigma


class Glicko(object):
    """docstring for Glicko."""
    def __init__(self, arg=None):
        super(Glicko, self).__init__()
        self.arg = arg

    def scale_down(self, mu, phi):
        return (mu - MU)/ratio, phi/ratio

    def get_expected(self, mu, opp_mu, impact):
        return 1. / (1 + math.exp(-impact * (mu- opp_mu)))

    def determine_sigma(self, phi, sigma, difference, variance):
        """Determines new sigma."""
        difference_squared = difference ** 2
        # 1. Let a = ln(s^2), and define f(x)
        alpha = math.log(sigma ** 2)
        def f(x):
            """This function is twice the conditional log-posterior density of
            phi, and is the optimality criterion.
            """
            tmp = phi ** 2 + variance + math.exp(x)
            a = math.exp(x) * (difference_squared - tmp) / (2 * tmp ** 2)
            b = (x - alpha) / (TAU ** 2)
            return a - b
        # 2. Set the initial values of the iterative algorithm.
        a = alpha
        if difference_squared > phi ** 2 + variance:
            b = math.log(difference_squared - phi ** 2 - variance)
        else:
            k = 1
            while f(alpha - k * math.sqrt(TAU ** 2)) < 0:
                k += 1
            b = alpha - k * math.sqrt(TAU ** 2)
        # 3. Let fA = f(A) and f(B) = f(B)
        f_a, f_b = f(a), f(b)
        # 4. While |B-A| > e, carry out the following steps.
        # (a) Let C = A + (A - B)fA / (fB-fA), and let fC = f(C).
        # (b) If fCfB < 0, then set A <- B and fA <- fB; otherwise, just set
        #     fA <- fA/2.
        # (c) Set B <- C and fB <- fC.
        # (d) Stop if |B-A| <= e. Repeat the above three steps otherwise.
        while abs(b - a) > EPSILON:
            c = a + (a - b) * f_a / (f_b - f_a)
            f_c = f(c)
            if f_c * f_b < 0:
                a, f_a = b, f_b
            else:
                f_a /= 2
            b, f_b = c, f_c
        # 5. Once |B-A| <= e, set s' <- e^(A/2)
        return math.exp(1) ** (a / 2)

    def reduce_impact(self, RD):
        return 1 / math.sqrt(1 + (3 * RD ** 2) / (math.pi ** 2))

    def update(self, team):
        opps = team.glicko_opp

        mu = (team.glicko - MU)/ratio
        phi = team.g_phi/ratio
        sigma = team.g_sigma

        dsq_inv = 0
        var_inv = 0
        diff = 0
        for opp, result in opps:
            opp_mu = (opp.glicko - MU)/ratio
            opp_phi = opp.g_phi/ratio
            opp_sigma = opp.g_sigma

            impact = self.reduce_impact(opp_phi)
            expected_result = self.get_expected(mu, opp_mu, impact)
            var_inv += impact ** 2 * expected_result * (1 - expected_result)
            diff += impact * (result - expected_result)
            dsq_inv += (expected_result * (1 - expected_result) * (Q ** 2) * (impact ** 2))
        diff /= var_inv
        var = 1/var_inv
        denom = phi ** -2 + dsq_inv

        mu_new = mu + Q / denom * (diff / var_inv)
        phi_new = math.sqrt(1/denom)
        sigma = self.determine_sigma(phi,sigma,diff,var)
        phi_star = math.sqrt(phi_new ** 2 + sigma **2)

        phi = 1 / math.sqrt(1 / phi_star ** 2 + 1 / var)
        mu = mu + phi ** 2 * (diff / var)

        team.glicko = mu * ratio + MU
        team.g_phi = phi * ratio
        team.g_sigma = sigma

        return team


# end
