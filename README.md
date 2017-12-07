# PosteriorAgreement
Compute the agreement between the parameters of two *N*-dimensional MCMC chains. The code returns the *p*-value and the corresponding number of sigmas, assuming Gaussian statistics for that latter number.

The idea is the following: We are trying to quantify whether and to what degree two distributions *P1(**x**)* and *P2(**x**)* agree within the parameter space **x**, by computing the probability to exceed (PTE) zero difference. We draw representative samples [**x1**] and **x2** from *P1(**x**)* and *P2(**x**)*, compute the distance between pairs of points
**δ** ≡ **x1** - **x2**
and construct the probability distribution P**δ** from the ensemble [**δ**]. The PTE zero difference then is

*p = ∫S d**y** P**δ**(**y**), S: **y** ϵ P**δ**(**y**) < P**δ**(**0**)*

where *P**δ**(**0**)* is the probability of zero difference. Finally, we can convert the PTE *p* into a significance *σ* using Gaussian statistics.

# Using weighted samples
There are many scenarios where your sample point have non-integer weights. You can pass the `weights` argument, and we use a modified gaussian kernel density estimator:
https://gist.github.com/tillahoffmann/f844bce2ec264c1c8cb5
