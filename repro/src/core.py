"""Clean-room ZoVH zeroth-order Hessian estimator (arXiv 2605.30960, OpenReview nEQYu4ndGA).

The Gaussian-smoothed objective is  F_mu(theta) = E_u[ f(theta + mu u) ],  u ~ N(0, I_d).
Its Hessian (Proposition 3.2) is

    grad^2 F_mu(theta) = E_u[ (f(theta+mu u) - b) / mu^2  *  (u u^T - I_d) ]

for ANY scalar baseline b independent of u (since E[u u^T - I_d] = 0).  The rank-one form
(Prop 3.3) drops the -I_d by using the specific averaged baseline b = F_mu(theta):

    grad^2 F_mu(theta) = E_u[ (f(theta+mu u) - b) / mu^2  *  u u^T ],   b = E_u[f(theta+mu u)].

The finite-sample estimator averages K random directions.  Theorem 4.7 gives the
variance-optimal baseline  b* = E_u[ f(theta+mu u) ||u u^T - I_d||_F^2 ] / E_u[ ||u u^T - I_d||_F^2 ]
-> F_mu(theta)  as d -> infty.  Theorem 4.8 bounds the Frobenius MSE

    E ||Ĥ - grad^2 F||_F^2  <=  K d(d+2) V / ((K-1)^2 mu^4)  +  L2^2 mu^2 d

with  V = sigma_xi^2 + 4 L0^2 mu^2 (d+2)  (variance term decreasing in K,mu; bias L2^2 mu^2 d
increasing in mu).
"""
from __future__ import annotations
import numpy as np


# --------------------------------------------------------------------------- #
#  Estimators (Prop 3.2 and Prop 3.3)
# --------------------------------------------------------------------------- #
def zovh_estimator_prop32(f, theta, mu, K, baseline, rng):
    """Ĥ = (1/K) sum_i [(f(theta+mu u_i) - b)/mu^2] (u_i u_i^T - I_d).  Unbiased for any b."""
    d = len(theta)
    U = rng.standard_normal(size=(K, d))
    H = np.zeros((d, d))
    for u in U:
        fu = f(theta + mu * u)
        H += (fu - baseline) / mu**2 * (np.outer(u, u) - np.eye(d))
    return H / K


def zovh_estimator_rank1(f, theta, mu, K, baseline, rng):
    """Rank-one form (Prop 3.3): Ĥ = (1/K) sum [(f-b)/mu^2] u_i u_i^T.  Unbiased iff b=F_mu."""
    d = len(theta)
    U = rng.standard_normal(size=(K, d))
    H = np.zeros((d, d))
    for u in U:
        fu = f(theta + mu * u)
        H += (fu - baseline) / mu**2 * np.outer(u, u)
    return H / K


def smoothed_value(f, theta, mu, rng, N=4000):
    """F_mu(theta) = E_u f(theta+mu u) by Monte-Carlo."""
    U = rng.standard_normal(size=(N, len(theta)))
    return float(np.mean([f(theta + mu * u) for u in U]))


def optimal_baseline(f, theta, mu, rng, N=4000):
    """Theorem 4.7: b* = E_u[ f(theta+mu u) ||u u^T - I_d||_F^2 ] / E_u[ ||u u^T - I_d||_F^2 ]."""
    d = len(theta)
    U = rng.standard_normal(size=(N, d))
    num = 0.0; den = 0.0
    for u in U:
        fu = f(theta + mu * u)
        w = np.sum((np.outer(u, u) - np.eye(d)) ** 2)   # ||u u^T - I||_F^2
        num += fu * w; den += w
    return num / den


# --------------------------------------------------------------------------- #
#  Reference smoothed Hessian  grad^2 F_mu = E_u[ grad^2 f(theta+mu u) ]
# --------------------------------------------------------------------------- #
def smoothed_hessian_mc(hess_f, theta, mu, rng, N=20000):
    """grad^2 F_mu(theta) = E_u[ grad^2 f(theta+mu u) ] by Monte-Carlo (reference)."""
    d = len(theta)
    H = np.zeros((d, d))
    for _ in range(N):
        u = rng.standard_normal(d)
        H += hess_f(theta + mu * u)
    return H / N


def central_difference_hessian(f, theta, h=1e-5):
    """Central-difference Hessian (2nd-order), 2d function evals per row -> O(d^2) evals."""
    d = len(theta)
    H = np.zeros((d, d))
    f0 = f(theta)
    for i in range(d):
        ei = np.eye(d)[i] * h
        H[i, i] = (f(theta + ei) - 2 * f0 + f(theta - ei)) / h**2
        for j in range(i + 1, d):
            ej = np.eye(d)[j] * h
            Hij = (f(theta + ei + ej) - f(theta + ei - ej)
                   - f(theta - ei + ej) + f(theta - ei - ej)) / (4 * h**2)
            H[i, j] = H[j, i] = Hij
    return H


# --------------------------------------------------------------------------- #
#  Test objectives with analytic Hessians
# --------------------------------------------------------------------------- #
def make_quadratic(A, b):
    """f(theta) = 1/2 theta^T A theta + b^T theta.  Hessian = A (constant)."""
    f = lambda th: 0.5 * th @ A @ th + b @ th
    hess = lambda th: A
    return f, hess


def make_quartic():
    """f(theta) = sum_i theta_i^4.  Hessian = diag(12 theta_i^2).
    Smoothed Hessian: grad^2 F_mu = E_u diag(12(theta+mu u)_i^2) = diag(12 theta_i^2 + 12 mu^2)."""
    f = lambda th: np.sum(th**4)
    hess = lambda th: np.diag(12.0 * th**2)
    return f, hess


def rosenbrock(th):
    """Rosenbrock: sum 100(x_{i+1}-x_i^2)^2 + (1-x_i)^2."""
    return float(np.sum(100.0 * (th[1:] - th[:-1]**2)**2 + (1 - th[:-1])**2))
