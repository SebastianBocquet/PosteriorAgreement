from __future__ import division
import numpy as np
from scipy import stats
import weighted_kde

class compute_agreement:
    def setup_KDE(self):
        """Initialize the Gaussian KDE for an n-dimensional
        posterior distribution.

	Arguments
	---------
        samples : array [nDims, nSamples]

    Returns
	-------
        None
        """
        if self.diffDistWeight is None:
            self.kde = stats.gaussian_kde(self.diffDist)
        else:
            self.kde = weighted_kde.gaussian_kde(self.diffDist, weights=self.diffDistWeight)
        return


    def evaluate_DiffDist(self, x):
        """Evaluate the posterior KDE at a given point x."""
        return self.kde.evaluate(x)


    def __init__(self, chains, weights=None, nSamples=100000, nBins=100, randomSeed=42):
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

        # Check the chains
        if len(chains[0].shape)==1:
            nDim = 1
            assert len(chains[1].shape)==1, \
                "Chains have different dimensions %d %d"%(1, len(chains[1].shape))
            chains = (chains[0][:,None], chains[1][:,None])
        else:
            nDim = chains[0].shape[1]
            assert chains[1].shape[1]==nDim, \
                "Chains have different dimensions %d %d"%(nDim, chains[1].shape[1])

        # Check the weights
        if weights is not None:
            for i in range(2):
                assert len(weights[i])==len(chains[i]), \
                    "Weights must have same lenght as chain (chain[%d])"%i

        # Draw random samples and build distribution of differences
        idx0 = np.random.randint(0, len(chains[0]), nSamples)
        idx1 = np.random.randint(0, len(chains[1]), nSamples)
        self.diffDist = np.transpose((chains[0][idx0,:] - chains[1][idx1,:]))

        self.diffDistWeight = None
        if weights is not None:
            self.diffDistWeight = (weights[0][idx0]**2 + weights[1][idx1]**2)**.5

        # Build KDE estimator
        self.setup_KDE()

        # General statistics
        self.mean = np.average(self.diffDist, weights=self.diffDistWeight, axis=1)
        self.xmin = self.diffDist.min(axis=1)
        self.xmax = self.diffDist.max(axis=1)


        # Setup up (flat) grid
        ranges = np.array((self.xmin, self.xmax)).T
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

        diffDistKDE = self.evaluate_DiffDist(xx_flat)

        # Get "level" or origin
        zero = np.zeros(nDim)
        level = self.evaluate_DiffDist(zero)

        # Total distribution
        I = np.sum(diffDistKDE)
        # Integral over x where f(x)<level
        self.PTE = np.sum(diffDistKDE[diffDistKDE<level]) / I

        # Convert into sigmas using normal distribution
        self.sigma = stats.norm.isf(self.PTE/2)
