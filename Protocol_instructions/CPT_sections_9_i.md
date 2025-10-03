# <a id="_Toc267565189"></a><a id="_Toc395881640"></a><a id="_Toc477961651"></a><a id="_Ref449945000"></a><a id="_Ref449944851"></a><a id="_Ref449944826"></a><a id="_Toc421709289"></a><a id="_Toc155184229"></a>Statistical Considerations

Provide a statement on when the main analysis and reporting will be made\.

## <a id="_Toc477927914"></a><a id="_Toc477961652"></a><a id="_Toc155184230"></a>General Considerations

This section should describe general methods and definitions that do not need to be repeated in the subsequent sections\. For example, a general statement that all investigational intervention/treatment condition comparisons for all categorical analyses will be tested using Fisher’s exact test does not need to be repeated for each categorical analysis described in later subsections\. The same would be true for analysis of variance information and the model used\. If different definitions are required for specific analyses, these should be stated in the relevant section\. Suggested topics to be included in this section, if appropriate for the study, are provided\. Subsections can be used, if applicable\. Below example headings are given, but sections can be deleted, added, or modified as needed\. If subsections are used, this section can have the section heading only, with no text required\. 

- Common definitions of baseline 
- For randomized studies, describe stratification factors if applicable, and if not specified in Section 4\.1
- General methods, such as handling of wrong stratification, wrong investigational intervention assignment, handling of values below lower limit of quantification, continuous variables will be summarized with min, max, mean, median, standard deviation, quantiles, etc
- General choice of analysis sets for analyses\.
- Pooling strategies for countries/regions, sites, etc 
- Strategy for grouping study arms, eg, combining all active dose arms versus control\.
- Definition of study periods if needed\.
- Definition of which contrasts between investigational interventions/treatment conditions will be provided\.
- For studies conducted under a master protocol, include details regarding whether analyses will be conducted by combining sub\-studies or within a sub\-study\.

### <a id="_Toc155184231"></a>\[Decision Criteria/Statistical Hypotheses\]

- Decision criteria, such as nominal significance levels, 1\- or 2\-sided tests, and confidence interval probabilities 
- Clearly articulate the statistical hypotheses \(null and alternative hypotheses\), that will be the subject of statistical testing related to each key/confirmatory estimand, when applicable\. It is recommended to state both the formal statistical null and alternative hypotheses and a textual non\-technical description\. In case no hypotheses are planned to be tested, state this in this section\. 
- If Bayesian or estimation approaches \(no formal hypothesis\) are used, describe the decision rule or estimation method\.
- For non\-inferiority tests, the non\-inferiority margin should be justified\.

### <a id="_Toc335643706"></a><a id="_Toc45176403"></a><a id="_Toc155184232"></a><a id="_Toc421709291"></a><a id="_Toc413419804"></a><a id="_Toc477961654"></a><a id="_Toc395881642"></a><a id="_Toc267565211"></a><a id="_Toc395881653"></a>Multiplicity Adjustment

- Clearly state the \(local and/or global\) significance level, the family\-wise error\-rate and the method for controlling overall type I error\.

### <a id="_Toc155184233"></a>Impact of Intercurrent Events Strategies

- For studies with estimands,
	- Consider adding a subsection to describe the intercurrent events, their strategies, and any technical statistical implication\. Alternatively, this can be described in the relevant analysis sections\. 
	- Describe how intercurrent events will be summarized \(number by treatment condition and timing\)\.

### <a id="_Toc155184234"></a>Handling of Missing Data

Consider adding a subsection on handling of missing data including missing baseline values if this is planned to be handled in the same way across analyses\. Alternatively, this can be described in the relevant analysis sections\.

## <a id="_Toc12630735"></a><a id="_Toc16163396"></a><a id="_Toc155184235"></a>Analysis Sets

- This CPT uses the following terminology:
	- ‘Participant Analysis Set’ = set of study participants\.  Examples: all randomized study participants, full analysis set, safety analysis set\.
	- ‘Data Points Set’ = the set of data points from each participant to be included in the analysis considering their \(relative\) timing as well as the occurrence of intercurrent events\.  Example: data points obtained while the participant was exposed to investigational intervention, i\.e, data points collected at or after the start and up to the stop date of investigational intervention \+ 2 calendar days\.
	- ‘Analysis Data Sets’ = the set of data points to be included in the analysis in a set of study participants, ie, combination of ‘Data Points Set’ and ‘Participant Analysis Set’\.
- Regardless of whether estimands are explicitly defined in Section 3 of the study protocol, the sets of participants included in statistical analyses, ie, ‘Participant Analysis Sets’, should be defined\. The number of participant analysis sets should be minimized\.
- In addition, it will often be helpful to define which measurements on a selected set of participants are to be in\- or excluded in a specific analysis\. In studies describing estimands, the treatment effect of interest is defined in a way that guides both the set of participants and the relevant observations from each participant to be included in the estimation in relation to the occurrence of intercurrent events\. 
- The selection and identification of the “to\-be\-analyzed data points” for a set of participants can be achieved by defining ‘Data Points Sets’ as required for the analyses\.
- The description of the assignment of participants to intervention in the analysis \(“as randomized” or “as actually received”\) can be described in this section or in Section 9\.3\.
- Note, naming of the Participant Analysis Set and not only the full data set \(participants and data points\) is recommended for ease of programming\.
- Three examples are provided for illustrative purposes only\. Other formats, other definitions, and different naming conventions can be used\.

## <a id="_Toc421709292"></a><a id="_Ref523049297"></a><a id="_Toc477961655"></a><a id="_Toc155184236"></a>Analyses Supporting Primary Objective\(s\)

Add level 3 subsections for the analysis of all endpoints/estimands supporting the primary objective\(s\), as applicable, after Section 9\.3\.1\.

### <a id="_Toc155184237"></a>Primary \[Endpoint\(s\)/Estimand\(s\)\]

#### Definition of endpoint\(s\)

- State how the primary endpoint\(s\) will be defined/calculated/derived and used to address the primary objective, if not clear from Section 3\. 
- Describe if the primary endpoint will be transformed, such as square\-root and logarithm before analysis\. It is recommended to include the rationale/justification for transformation and the interpretation\.

#### Main Analytical Approach

- Refer to estimand\(s\) in Section 3 and ICH E9 \(R1\) if applicable\. In case of more than one primary estimand due to different requirements across different regulatory agencies, describe the analysis of the primary endpoint for all primary estimands and indicate which estimands are required by which authorities if this is not clear from Section 3\. 
- Refer to the analysis set to be used in the main analytical approach\(es\)\.
- Refer to the Decision Criteria/Statistical Hypotheses subsection \(in Section 9\.1 of this template\) regarding the hypothesis to be tested, if applicable\.
- Describe the main analytical approach\(es\) \(aligned to the primary estimand\[s\] and with a description of the handling of each type of intercurrent event, \(if applicable and not described in Section 9\.1\)\.  Describe how missing data will be handled, if not described in Section 9\.1\.  In case of multiple imputation, state imputation model, number of datasets, and seed\. Specify how datasets will be combined\.
- Describe \(if applicable\) factors, covariates, stratification factors, etc, to be included in the analysis model\.
- Describe underlying assumption\(s\) of the main analytical approach\(es\) including assumptions on the missing data mechanism\.

#### <a id="_Toc44422564"></a><a id="_Ref34741151"></a><a id="_Toc52192297"></a>Sensitivity \[Analysis/Analyses\]

- Describe the planned sensitivity analyses and how the sensitivity analyses will target the assumptions behind the main analytical approach or limitations in data\. Pay special attention to assumptions regarding the missing data mechanism\. If a range of methods is proposed, each should target different assumptions in order to explore how these may influence the results obtained from the main analysis\. 

#### Supplementary \[Analysis/Analyses\]

- Describe any supplementary analyses\. This could be estimation of supplementary estimands defined in Section 3 for the primary objective, if it will not be described as a stand\-alone estimand in a level 3 subsection\.  If not described in Section 9\.2, describe which participants and data points are included in the analysis set to be used to estimate each of the estimand\(s\) related to supplementary analyses\. Consider if supplementary analyses including estimand definitions related to them can be moved to the SAP\.

## <a id="_Toc45176423"></a><a id="_Toc44937959"></a><a id="_Toc44676521"></a><a id="_Toc44596884"></a><a id="_Toc44325478"></a><a id="_Toc43126356"></a><a id="_Toc45176424"></a><a id="_Ref43126486"></a><a id="_Ref43126456"></a><a id="_Ref42688383"></a><a id="_Toc521927448"></a><a id="_Toc155184238"></a><a id="_Toc421709296"></a><a id="_Ref526520817"></a><a id="_Toc477961659"></a>Analyses Supporting Secondary Objective\(s\)

- Add level 3 subsections as required according to the number of secondary objectives\.

### <a id="_Toc155184239"></a>Analyses Supporting Secondary Objective \[label\]

- Key/confirmatory secondary endpoint\(s\)/estimand\(s\) \(eg, for which a label claim is pursued\) are part of the confirmatory hypotheses where the type 1 error is controlled \(via multiplicity adjustment\)\. It is recommended to use the same structure as in Section 9\.3 and describe the analysis of such endpoint\(s\)/estimand\(s\) to the same level of detail as the primary endpoint\(s\)/estimand\(s\) being described in Section 9\.3\.1\.2 and Section 9\.3\.1\.3\. If the same methodology/analytical approach is taken for these endpoint\(s\)/estimand\(s\), it will be sufficient to add a cross\-reference to Section 9\.3\.1\.2/9\.3\.1\.3 to avoid redundancy\.
- Analysis of other supportive endpoint\(s\)/supplementary estimand\(s\) need not be described with the same level of detail as the key secondary endpoint\(s\)/estimand\(s\)\. A description of supportive secondary endpoint\(s\)/estimand\(s\) can be omitted from the protocol section with a reference made to the SAP\.

## <a id="_Ref42688386"></a><a id="_Toc45176426"></a><a id="_Toc521927449"></a><a id="_Toc155184240"></a>Analyses Supporting \[Tertiary/Exploratory/Other\] Objective\(s\)

It is optional if a description will be provided in the protocol section or in the SAP\. If the description is provided in the SAP only a reference to the SAP should be made in this section\. If the description is provided in the protocol section, it is recommended to describe the analyses to the same level of detail as the supportive secondary endpoint\(s\)/estimand\(s\)\. For example, no sensitivity or supplementary analyses need to be specified for tertiary/exploratory/other endpoints/estimands unless such analyses are planned to be made\. 

Add subsections as required according to the number of tertiary/exploratory/other objectives\.

## <a id="_Toc521927450"></a><a id="_Toc45176428"></a><a id="_Toc155184241"></a>\[Other\] Safety Analyses

- Describe at a high level how the safety data will be analyzed if not already described in either Section 9\.3, Section 9\.4, or Section 9\.5\. Refer to the SAP for details\.
- Specify the analysis set to be used or refer to Section 9\.2\. 
- Specify estimands, if applicable and not defined in Section 3\.

## <a id="_Toc45176430"></a><a id="_Toc44937966"></a><a id="_Toc44676528"></a><a id="_Toc44596891"></a><a id="_Toc44325485"></a><a id="_Toc43126363"></a><a id="_Toc45176431"></a><a id="_Toc521927451"></a><a id="_Toc155184242"></a>Other Analyses

A description can be omitted from the protocol section and a reference made to the SAP\. Alternatively, a high\-level description can be provided and further detailed in the SAP, if not fully detailed in the study protocol\.

Analysis of other variables and/or parameters and subgroup analyses belong to this section\.

### <a id="_Toc155184243"></a>Other variables and/or parameters 

Other analyses may include analyses of assessments or derived parameters, which are not defined as endpoints but need to be prespecified in either the protocol or SAP\. Examples include but are not limited to immunogenicity, biomarkers, PK/PD/population PK parameters, health care utilization variables, and health technology assessment\-related variables\. <a id="_Hlk45020274"></a>State if these will be reported in a separate document\. 

Subsections may be used for different topics\.

It is recommended that the variables used in the analyses should be clearly defined and the analyses should be described at the same level of detail as the supportive secondary endpoint\(s\)/estimand\(s\)\.

The definition and derivation may be specified in a table format\.

Specify estimands if applicable and not defined in Section 3\.

### <a id="_Toc155184244"></a>Subgroup analyses 

Note: Often individual standard clinical studies \(excluding large outcomes or safety studies\) are not designed to allow for statistically meaningful subgroup analyses because of too small sample sizes\. Also, subgroup analyses are not commonly included in the set of <a id="_Hlk11085573"></a>multiplicity\-controlled analyses and are therefore subject to multiplicity issues\.

It is recommended to consider addressing the following topics, if applicable:

- Define the endpoints subject to subgroup analysis – can be for either efficacy and safety, or both\.
- Define subgroups \(may include stratification factor, if relevant\)\. Specify how participants will be classified into a subgroup in case of missing information\.
- Provide the purpose \(consistency, hypothesis\) of each subgroup analysis\. The subgroup analyses should preferably be further substantiated, eg, biological plausibility of anticipated differential effect, regulatory/payer requirement\.
- Specify any rules to define the minimum size of a subgroup in order to carry out the analysis\.
- Specify analysis sets/estimand\(s\), as applicable\.
- Specify the subgroup analysis methods including how missing data are handled\.
- Specify the level of significance for the test of the investigational intervention/treatment condition\-by\-subgroup interaction, if applicable\.
- Assess consistency across regions and subpopulation\(s\) for multiregional clinical studies, as specified in ICH E17\.
- Describe how results will be presented\. It is recommended to focus on estimates and confidence intervals rather than p\-values\. It is often useful to display the results in a forest plot\.

## <a id="_Toc155184245"></a>Interim \[Analysis/Analyses\]

If an interim analysis is planned, describe if any type of data monitoring committee will be established to evaluate the interim analyses \(the safety data and/or the critical efficacy endpoints\) in accordance with ICH E9\. Also describe the role of the committee \(eg, making recommendation to the sponsor whether to continue, modify, or stop a study\)<a id="_Hlk16156810"></a>\. Full details of the committee including any charters should be included in Appendix 10\.1\.5 Committees Structure\.

The following information belongs in this section:

- Reason for conducting interim analyses and the impact on the conduct of the study
- Endpoints to be included in the interim analyses
- Timing of the interim analyses \(eg, number of participants enrolled, number of participants completing a certain number of visits, number of events, calendar time\)
- Any actions resulting from an interim analysis such as sample size re\-estimation or stopping rules
- Multiplicity considerations relating to the interim and final analyses
- Blinding/ unblinding strategy

## <a id="_Toc421709290"></a><a id="_Ref449944842"></a><a id="_Ref449945044"></a><a id="_Toc477961653"></a><a id="_Toc155184246"></a>Sample Size Determination

- State the expected number of participants to be screened, enrolled, assigned to investigational intervention, when applicable\. Consistent with the estimand chosen \(where applicable\) state the assumptions for intercurrent events: frequency per treatment condition and the assumed impact these may have on the effect size and variation\. For an event‑driven study, state the number of events planned along with the number of participants to be randomized\. Adapt the text to the study design\.
- When applicable \(eg, studies not using an estimand concept\), ensure this section clearly explains how non\-evaluable participants are defined\.
- Provide justification of sample size in accordance with the primary and/or other relevant statistical analysis and study objectives/estimands\.
- Assumptions and methodology for calculations \(and/or simulations\) should be provided with references\. If possible, the estimand used in the reference study should be mentioned\. The sensitivity to these assumptions should be investigated by presenting different scenarios based on varying assumptions\. 
- The actual sample size reached in the study will rarely be exactly equal to the target sample size\. Therefore, please add the word approximately in the text when stating the target sample size\. This ensures that the protocol covers the potential to slightly over\- or underenroll\.
- Include power calculations and level of significance to be used as appropriate\. If applicable, describe adjustments for multiple comparisons and/or considerations as to disjunctive or marginal power depending on the clinical objectives\.
- If the sample size is not based on statistical considerations, as outlined above, provide a justification\. An alternative to providing a statistical justification for the sample size is to state that the sample size is not based on statistical considerations and then discuss the statistical implications of the chosen sample size\.
- As applicable, discuss allocation of participants with respect to region\-/country\-specific regulatory requirements\.
- As applicable, specify the software \(and version\) used to determine the sample size\.
