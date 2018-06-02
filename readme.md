# Quantify the difference between two arbitrary curves

Curves in this case are:
- discretized by inidviudal data points
- are ordered from a beginning to an ending

The qua

# Methods covered
- **Partial Curve Mapping**<sup>x</sup> (PCM) method: Matches the area of a subset between the two curves [1]
- **Area method**<sup>x</sup>: An algorithm for calculating the Area between two curves in 2D space [2]
- **Discrete Fréchet distance**: The shortest distance in-between two curves, where you are allowed to very the speed at which you travel along each curve independently (walking dog problem) [3, 4, 5, 6, 7, 8]
- **Dynamic Time Warping** (DTW): A non-metric distance between two time-sereis curves that has been proven useful for a variety of applications [9, 10, 11, 12, 13]
- **Curve Length**<sup>x</sup> method: Assumes that the only true independent variable of the curves is the arc-length distance along the curve from the origin [14, 15]

<sup>x</sup> denotes methods created specifically for material parameter identification

# Example
In the ideal case the Numerical curve would match the Experimental curve exactly. This means that the two curves would appear directly on top of each other. Our measures of similarity would return a *zero* distance between the two curves.

Consider the following two curves. We want to quantify how different the Numerical curve is from the Experimental curve. Notice how there are no concurrent Stress or Strain values in the two curves. Additionally one curve has more data points than the other curves.
![Image of two different curves](images/TwoCurves.png)

# References
[1] Katharina Witowski and Nielen Stander. Parameter Identification of Hysteretic Models
Using Partial Curve Mapping. 12th AIAA Aviation Technology, Integration, and Op-
erations (ATIO) Conference and 14th AIAA/ISSMO Multidisciplinary Analysis and
Optimization Conference, sep 2012. doi: doi:10.2514/6.2012-5580.

[2] SOON_TM

[3] M Maurice Fréchet. Sur quelques points du calcul fonctionnel. Rendiconti del Circol
Matematico di Palermo (1884-1940), 22(1):1–72, 1906.

[4] Thomas Eiter and Heikki Mannila. Computing discrete Fréchet distance. Technical
report, 1994.

[5] Anne Driemel, Sariel Har-Peled, and Carola Wenk. Approximating the Fréchet Distance
for Realistic Curves in Near Linear Time. Discrete & Computational Geometry, 48(1):
94–127, 2012. ISSN 1432-0444. doi: 10.1007/s00454-012-9402-z. URL http://dx.doi.
org/10.1007/s00454-012-9402-z.

[6] K Bringmann. Why Walking the Dog Takes Time: Frechet Distance Has No Strongly
Subquadratic Algorithms Unless SETH Fails, 2014.

[7] Sean L Seyler, Avishek Kumar, M F Thorpe, and Oliver Beckstein. Path Similarity
Analysis: A Method for Quantifying Macromolecular Pathways. PLOS Computational
Biology, 11(10):1–37, 2015. doi: 10.1371/journal.pcbi.1004568. URL https://doi.org/
10.1371/journal.pcbi.1004568.

[8] Helmut Alt and Michael Godau. Computing the Fréchet Distance Between Two Polyg-
onal Curves. International Journal of Computational Geometry & Applications, 05
(01n02):75–91, 1995. doi: 10.1142/S0218195995000064.

[9] Donald J Berndt and James Clifford. Using Dynamic Time Warping to Find Pat-
terns in Time Series. In Proceedings of the 3rd International Conference on Knowledge
Discovery and Data Mining, AAAIWS’94, pages 359–370. AAAI Press, 1994. URL
http://dl.acm.org/citation.cfm?id=3000850.3000887.

[10] François Petitjean, Alain Ketterlin, and Pierre Gançarski. A global averaging method for dynamic time warping, with applications to clustering. Pattern Recognition, 44 (3):678–693, 2011. ISSN 0031-3203. doi: https://doi.org/10.1016/j.patcog.2010.09.013.
URL http://www.sciencedirect.com/science/article/pii/S003132031000453X.

[11] Toni Giorgino. Computing and Visualizing Dynamic Time Warping Alignments in R:
The dtw Package. Journal of Statistical Software; Vol 1, Issue 7 (2009), aug 2009. URL
http://dx.doi.org/10.18637/jss.v031.i07.

[12] Stan Salvador and Philip Chan. Toward Accurate Dynamic Time Warping in Linear
Time and Space. Intell. Data Anal., 11(5):561–580, oct 2007. ISSN 1088-467X. URL
http://dl.acm.org/citation.cfm?id=1367985.1367993.

[13] Paolo Tormene, Toni Giorgino, Silvana Quaglini, and Mario Stefanelli. Matching
incomplete time series with dynamic time warping: an algorithm and an applica-
tion to post-stroke rehabilitation. Artificial Intelligence in Medicine, 45(1):11–34,
2009. ISSN 0933-3657. doi: https://doi.org/10.1016/j.artmed.2008.11.007. URL
http://www.sciencedirect.com/science/article/pii/S0933365708001772.

[14] A Andrade-Campos, R De-Carvalho, and R A F Valente. Novel criteria for determina-
tion of material model parameters. International Journal of Mechanical Sciences, 54
(1):294–305, 2012. ISSN 0020-7403. doi: https://doi.org/10.1016/j.ijmecsci.2011.11.010.
URL http://www.sciencedirect.com/science/article/pii/S0020740311002451.

[15] J Cao and J Lin. A study on formulation of objective functions for determin-
ing material models. International Journal of Mechanical Sciences, 50(2):193–204,
2008. ISSN 0020-7403. doi: https://doi.org/10.1016/j.ijmecsci.2007.07.003. URL
http://www.sciencedirect.com/science/article/pii/S0020740307001178.


# Please cite
If you've found this information helpful, please cite

SOON_TM
