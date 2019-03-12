import math

from settings import *

Q = math.log(10) / 400
ratio = glicko_set['ratio']
epsilon = glicko_set['epsilon']

class Rating(object):
    """docstring for Rating."""
    def __init__(self, glicko, RD, vol):
        super(Rating, self).__init__()
        self.glicko = glicko
        self.RD = RD
        self.vol = vol

        self.mu, self.phi = self.scale_down(glicko, RD)

    def scale_down(self, glicko, RD):
        mu = (glicko - glicko_set['initial']) / ratio
        phi = RD / ratio
        return mu, phi

    def scale_up(self, mu, phi):
        glicko = mu * ratio + glicko_set['initial']
        RD = phi * ratio
        return glicko, RD

    def set_glicko(self, glicko, RD, vol):
        self.glicko = glicko
        self.RD = RD
        self.vol = vol
        self.mu, self.phi = self.scale_down(glicko, RD)
        return

    def set_mu(self, mu, phi, vol):
        self.mu = mu
        self.phi = phi
        self.vol = vol
        self.glicko, self.RD = self.scale_up(mu, phi)
        return

class Glicko2(object):
    """docstring for Glicko."""
    def __init__(self, tau=0.5):
        super(Glicko2, self).__init__()
        self.tau = tau

      #################
     ## Helper Funx ##
    #################

    def reduce_impact(self, rating):
        return 1 / math.sqrt(1 + (3 * rating.phi ** 2) / (math.pi ** 2))

    def expect_score(self, rating_1, rating_2, impact):
        return 1. / (1 + math.exp(-impact * (rating_1.mu - rating_2.mu)))

    def create_rating(self, glicko, RD, vol):
        return Rating(glicko, RD, vol)

    def expected_score(self, rating_1, rating_2):
        impact = self.reduce_impact(rating_2)
        return self.expect_score(rating_1, rating_2, impact)

    def determine_vol(self, rating, difference, variance):
        """Determines new vol."""
        phi = rating.phi
        difference_squared = difference ** 2
        # 1. Let a = ln(s^2), and define f(x)
        alpha = math.log(rating.vol ** 2)
        def f(x):
            """This function is twice the conditional log-posterior density of
            phi, and is the optimality criterion.
            """
            tmp = phi ** 2 + variance + math.exp(x)
            a = math.exp(x) * (difference_squared - tmp) / (2 * tmp ** 2)
            b = (x - alpha) / (self.tau ** 2)
            return a - b
        # 2. Set the initial values of the iterative algorithm.
        a = alpha
        if difference_squared > phi ** 2 + variance:
            b = math.log(difference_squared - phi ** 2 - variance)
        else:
            k = 1
            while f(alpha - k * math.sqrt(self.tau ** 2)) < 0:
                k += 1
            b = alpha - k * math.sqrt(self.tau ** 2)
        # 3. Let fA = f(A) and f(B) = f(B)
        f_a, f_b = f(a), f(b)
        # 4. While |B-A| > e, carry out the following steps.
        # (a) Let C = A + (A - B)fA / (fB-fA), and let fC = f(C).
        # (b) If fCfB < 0, then set A <- B and fA <- fB; otherwise, just set
        #     fA <- fA/2.
        # (c) Set B <- C and fB <- fC.
        # (d) Stop if |B-A| <= e. Repeat the above three steps otherwise.
        while abs(b - a) > epsilon:
            c = a + (a - b) * f_a / (f_b - f_a)
            f_c = f(c)
            if f_c * f_b < 0:
                a, f_a = b, f_b
            else:
                f_a /= 2
            b, f_b = c, f_c
        # 5. Once |B-A| <= e, set s' <- e^(A/2)
        return math.exp(1) ** (a / 2)

      #################
     ## Rating Funx ##
    #################

    def rate(self, rating, series):
        # Step 2. For each player, convert the rating and RD's onto the
        #         Glicko-2 scale.
        # Step 3. Compute the quantity v. This is the estimated variance of the
        #         team's/player's rating based only on game outcomes.
        # Step 4. Compute the quantity difference, the estimated improvement in
        #         rating by comparing the pre-period rating to the performance
        #         rating based only on game outcomes.
        d_square_inv = 0
        variance_inv = 0
        difference = 0
        for actual_score, other_rating in series:
            impact = self.reduce_impact(other_rating)
            expected_score = self.expect_score(rating, other_rating, impact)
            variance_inv += impact ** 2 * expected_score * (1 - expected_score)
            difference += impact * (actual_score - expected_score)
            d_square_inv += (
                expected_score * (1 - expected_score) *
                (Q ** 2) * (impact ** 2))
        difference /= (variance_inv + epsilon)
        variance = 1. / (variance_inv + epsilon)
        denom = rating.phi ** -2 + d_square_inv
        mu = rating.mu + Q / denom * (difference / (variance_inv+epsilon))
        phi = math.sqrt(1 / denom)
        # Step 5. Determine the new value, vol', or the volatility. This
        #         computation requires iteration.
        vol = self.determine_vol(rating, difference, variance)
        # Step 6. Update the rating deviation to the new pre-rating period
        #         value, Phi*.
        phi_star = math.sqrt(phi ** 2 + vol ** 2)
        # Step 7. Update the rating and RD to the new values, Mu' and Phi'.
        phi = 1 / math.sqrt(1 / phi_star ** 2 + 1 / variance)
        mu = rating.mu + phi ** 2 * (difference / variance)
        # Step 8. Convert ratings and RD's back to original scale.
        rating.set_mu(mu, phi, vol)
        return rating









#end
