
<div style="margin-right: 70px;">

### **Overview**

I developed and presented a ranking system through an interactive Power BI dashboard to evaluate the research performance of UK higher education institutions (HEIs), utilising data from the 2021 Research Excellence Framework (REF 2021). The dashboard can guide university administrators in strategic decision-making:

For instance, at the University of Cambridge, the Anthropology and Development Studies, Area Studies, and Classics departments rank in the 19th, 30th, and 35th percentiles respectively, compared to all UK universities. This analysis suggests prioritising these departments for review, with Area Studies and Classics demonstrating particular weakness in impact, while Anthropology and Development Studies consistently underperforms across all assessed areas: outputs, environment, and impact.

This user-friendly dashboard supports stakeholders, including administrators and researchers, by enabling meaningful comparisons across institutions and disciplines.

In the process of designing the scoring system, I evaluated the approach taken by other consultancies, who weight GPA by size to produce a "research power" score. My models demonstrate that this approach is misguided, as size almost perfectly correlates with research power. Furthermore, modeling the relationship between scores and size for non-specialist institutions (comprising 76% of the data) using a power function indicates a strong fit (R-squared ≈ 79%).

A more detailed description of the project, including charts of the models and distributions described, can be found [here](https://github.com/Dank-o/UK-University-Research-Performance-PowerBI/blob/main/detailed_description.ipynb).

If you have Power BI, the dashboard can be viewed by downloading the [PBIX](https://github.com/Dank-o/UK-University-Research-Performance-PowerBI/blob/main/REF%20Dashboard.pbix) and [XLSX](https://github.com/Dank-o/UK-University-Research-Performance-PowerBI/blob/main/REF%202021%20Results%20-%20All%20-%20NO%20HEADER.xlsx) files.

<div style="text-align: center; margin-right: 70px;">
    <img src="quick_demo.gif" alt="A brief demo of the dashboard showing its filtering functions and interactions between the visuals." style="width: 20cm;">
    <p style="text-align: center;"><em>A brief demonstration of the dashboard showing its filtering functions and interactions between the visuals.</em></p>
</div>

### **Defining the Problem**

University administrators need a system to assess and compare departmental research performance to highlight top performers and identify areas for improvement. Similarly, researchers and graduate students benefit from a data-driven approach to identifying institutions excelling in their chosen disciplines. Existing ranking systems often fail to address these needs due to their reliance on indirect metrics (e.g., reputation, legacy awards) and inadequate evaluation of discipline-specific performance—often with a clear bias towards STEM-focused metrics.

REF 2021, a direct and comprehensive assessment of research quality across UK HEIs, offers a more robust dataset. However, the raw data lacks an accessible scoring system for comparing performance. My challenge was to:

1. Develop an adequately discriminative scoring system.
2. Visualise data to provide actionable insights for stakeholders.
3. Enable meaningful comparisons across institutions and disciplines.

### **Factors Guiding the Analysis**

#### **_Choice of Dataset_**

REF 2021 data provide a high-quality, audited evaluation of research outputs, environment, and societal impact across 157 HEIs and 34 disciplines. It avoids biases present in popular rankings and ensures fair evaluation of diverse disciplines, including social sciences and humanities.

#### **_Scoring System Design_**

To create a balanced scoring system, I analysed existing schemes that also utilise REF 2021 data:

- **Funding Bodies:** In order to allocate around £2 billion per year to universities for research, the four governmental funders of HEIs in the UK use a strict system (weights: 4, 1, 0, 0, 0) that heavily rewards top-performing institutions but fails to differentiate between moderate and poor performance.
- **Times Higher Education:** A lenient system (weights: 4, 3, 2, 1, 0) that produces a left-skewed distribution of GPAs —such that there is little separating high-performing institutions, while the low-performing end has large differences from one HEI to the next. They also multiply the GPAs by the number of staff to produce a “research power” score. However, the research power ranking is overwhelmingly determined by staff numbers, as indicated by an R-squared of 99.75% (compared to around 31% for the raw GPA). Moreover, there is already a strong (non-linear) relationship between GPA and size in non-specialist institutions. This suggests that GPA substantially reflects the influence of staff numbers in these categories, making it redundant to explicitly factor size into rankings.

I designed a hybrid weighting system (4, 1.5, 1, 0.5, 0) that:

- Rewards excellence while valuing moderate quality.
- Produces a nearly normal distribution; successfully discriminates between institutions in any score range. This is inspired by the scheme used by the funding bodies that produces a GPA distribution that is also approximately normal, suggesting that the difference in quality within groups of institutions at either end of the scale is expected to be symmetric.

I had also considered using submission rates as a weight to penalise incomplete submissions, however, I decided against it as I could not determine why these rates should vary.

Most of this additional analysis, model fitting, experimentation and visualisation was done in Python.

#### **_Data Filtering and Comparisons_**

I incorporated filters for staff numbers and comprehensiveness (range of disciplines) to ensure meaningful comparisons. This deals with a number of issues plaguing other systems. For example:

- Comparing the overall scores of the London Business School (specialised) to Anglia Ruskin University (comprehensive) would be misleading despite their close staff numbers.
- Offering and excelling in Business and Management Studies alone places the London Business School as the top institution overall. This is unsurprising; institutions that offer a single discipline are compared against others that offer up to 30 disciplines. (This is likely what motivated the research power metric mentioned previously.)

#### **_Presentation Choices_**

The dashboard is organised to easily compare a selected institution against a group of filtered institutions. The prominent charts on the dashboard are:

- Ranking Table: Displays all institutions in the filtered range, showing their scores, ranks, and staff numbers. Users can dynamically sort the institution table by performance in areas of interest by clicking on one or more disciplines in the bar chart described below.
- Discipline Bar Chart: Visualises scores for each discipline, with side-by-side bars representing the selected institution’s score and the average score of the filtered group. The bars are sorted and labelled by the rank percentile of the selected institution’s score in each discipline (within the group scores for that discipline). Percentiles were chosen to compress the individual ranking tables for each discipline into a number that allows an administrator, for example, to evaluate multiple disciplines at a glance.

Additional design considerations included:

- Coarse-grained rankings to cluster institutions into groups, avoiding the common pitfall of false precision in rankings.
- Scores are expressed as percentages (e.g., "60%") as these are immediately more informative than GPAs (e.g., "2.4"), particularly for British users.
- A two-hue palette distinguishes the selected institution’s data from that of the filtered group, with colours chosen to align with a fictional organisation’s branding.

Additional charts and interactions are afforded by the dashboard, however, the above are the most important.

### **Disregarded Information**

The source data file contained 7506 rows and 14 columns, of which I used 9 columns. I discarded data for submission rates, as well as certain data that was only given for a small number of institutions; information about joint submissions and disciplines with subdivisions. (There were also numerical codes that I only used for building relationships in the data model, as recommended by Power BI best practices.)

I renamed technical terms (e.g., "units of assessment" to "disciplines") for accessibility and shortened HEI names (e.g., "University College London" to "UCL") for better readability and use of the dashboard space.

### **Ensuring Accuracy and Relevance**

I conducted checks to ensure that my results were accurate and reasonable by inspecting summary data for institutions I was familiar with, checked for internal consistency of results by creating charts and tables to explore how different aspects of the data were related, and compared my results with existing summaries and analyses. I also researched existing systems to understand their goals, strengths and weaknesses.

### **Conclusion**

I used Power BI to create an intuitive, interactive dashboard with filtering and comparison capabilities tailored to stakeholders. The dashboard enables users to:

- Identify strengths and weaknesses within institutions and across disciplines.
- Evaluate overall performance against similar institutions using size and comprehensiveness filters.

This project demonstrates my ability to analyse complex datasets, design user-focused solutions, and present actionable insights.

</div>
