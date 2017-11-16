from __future__ import division
import numpy as np
from scipy import stats

class NDimPosterior:
    def __init__(self, samples):
        """Initialize the Gaussian KDE for an n-dimensional
        posterior distribution.
        
	Arguments
	---------
        samples : array [nDims, nSamples]

        Returns
	-------
        None
        """
        self.kde = stats.gaussian_kde(samples)
        self.mean = samples.mean(axis=1)
        self.std = samples.std(axis=1)
        self.xmin = samples.min(axis=1)
        self.xmax = samples.max(axis=1)
        return

    def evaluate(self, x):
        """Evaluate the posterior KDE at a given point x."""
        return self.kde.evaluate(x)


def compute_agreement(chains, nSamples=100000, nBins=100, randomSeed=42):
    """Compute agreement between two n-dimensional (nDim) MCMC chains.

    Arguments
    ---------
    chains: list[[nSamples1,nDim], [nSamples2,nDim]]
        Your two MCMC chains.

    Keywork arguments
    -----------------
    nSamples: number of random samples to draw from each chain
    nBins: number of bins per dimension used to compute agreement
    randomSeed: set different random seed to get different random samples

    Returns
    -------
    probability to exceed, Gaussian "sigmas"
    """
    np.random.seed(randomSeed)

    if len(chains[0].shape)==1:
        nDim = 1
        assert len(chains[1].shape)==1, \
            "Chains have different dimensions %d %d"%(1, len(chains[1].shape))
        chains = (chains[0][:,None], chains[1][:,None])
    else:
        nDim = chains[0].shape[1]
        assert chains[1].shape[1]==nDim, \
            "Chains have different dimensions %d %d"%(nDim, chains[1].shape[1])

    # Draw random samples and build distribution of differences
    idx0 = np.random.randint(0, len(chains[0]), nSamples)
    idx1 = np.random.randint(0, len(chains[1]), nSamples)
    diffDist = chains[0][idx0,:] - chains[1][idx1,:]

    # Build KDE estimator
    posterior = NDimPosterior(diffDist.T)

    # Setup up (flat) grid
    ranges = np.array((posterior.xmin, posterior.xmax)).T
    x = [np.linspace(ranges[i,0], ranges[i,1], nBins) for i in range(nDim)]
    if nDim==1:
        xx = x[0]
    elif nDim==2:
        xx = np.array(np.meshgrid(x[0], x[1]))
    elif nDim==3:
        xx = np.array(np.meshgrid(x[0], x[1], x[2]))
    elif nDim==4:
        xx = np.array(np.meshgrid(x[0], x[1], x[2], x[3]))
    elif nDim==5:
        xx = np.array(np.meshgrid(x[0], x[1], x[2], x[3], x[4]))
    else:
        raise ValueError("nDim is currently only supported up to 5, please raise issue!")
    xx_flat = xx.reshape((nDim,-1))

    diffDistKDE = posterior.evaluate(xx_flat)

    # Get "level" or origin
    zero = np.zeros(nDim)
    level = posterior.evaluate(zero)

    # Total distribution
    I = np.sum(diffDistKDE)
    # Integral over x where f(x)>level
    pbar = np.sum(diffDistKDE[diffDistKDE>level])

    # Probability to exceed zero
    PTE = 1 - pbar/I
    sigma = stats.norm.isf(PTE/2)

    return PTE, sigma

