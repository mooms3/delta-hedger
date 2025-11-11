from math import log, sqrt, exp
from scipy.stats import norm

def bs_delta(S, K, T, r, q, sigma, option_type):
    """
    Calculate Black-Scholes delta for European option.
    
    Parameters
    ----------
    S : float
        Current underlying price
    K : float
        Strike price
    T : float
        Time to expiry in years
    r : float
        Risk-free rate (annualized)
    q : float
        Dividend yield (annualized)
    sigma : float
        Implied volatility (annualized)
    option_type : str
        'C' for call, 'P' for put

    Returns
    -------
    delta : float
        Option delta
    """
    if T <= 0:
        # If expired, delta is 0 or 1
        if option_type.upper() == 'C':
            return 1.0 if S > K else 0.0
        else:
            return -1.0 if S < K else 0.0

    d1 = (log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))

    if option_type.upper() == 'C':
        delta = exp(-q * T) * norm.cdf(d1)
    elif option_type.upper() == 'P':
        delta = -exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'C' or 'P'")

    return delta
