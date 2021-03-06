# PosteriorAgreement

Quantify whether the difference between two posterior distributions is consistent with zero difference. Accepts samples from one- or multidimensional posterior distributions. The code returns the *p*-value that both distributions agree. This can be converted into a number of sigmas, assuming Gaussian statistics.

## Installation

I recommend you install the package straight from GitHub:

`pip install git+https://github.com/SebastianBocquet/PosteriorAgreement`

## Let's get started with a one-dimensional example

We draw representative samples [**x1**] and [**x2**] from *P1(**x**)* and *P2(**x**)*, compute the difference between pairs of points **δ** ≡ **x1** - **x2** and construct the probability distribution *D* from the ensemble [**δ**]. The probability value (or *p*-value) then is

![](eqn.png)

where *D*(**0**) is the probability of zero difference.

The following figure show the normalized difference distribution, and highlights the are that is integrated to obtain the *p*-value. This makes sense intuitively: if zero is well within the difference distribution, the *p*-value is large, indicating good agreement. Conversely, if zero is far from the distribution, the *p*-value will be very small.

![](one-d_example.png)

## Higher dimensions

This becomes hard to visualize. But the program is the same: construct the difference distribution *D*, and compute the *p*-value using the Equation above.

## Using weighted samples
There are many scenarios where your sample point have non-integer weights. You can pass the `weights` argument, and we use a modified gaussian kernel density estimator:
https://gist.github.com/tillahoffmann/f844bce2ec264c1c8cb5
