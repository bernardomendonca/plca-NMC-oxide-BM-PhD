


# List of ReCiPe Midpoint (H)
# H stands for Hierarchist
## https://www.rivm.nl/bibliotheek/rapporten/2016-0104.pdf
recipe_midpoint_h = [
    ('ReCiPe Midpoint (H)', 'terrestrial ecotoxicity', 'TETPinf'),
    ('ReCiPe Midpoint (H)', 'natural land transformation', 'NLTP'),
    ('ReCiPe Midpoint (H)', 'photochemical oxidant formation', 'POFP'),
    ('ReCiPe Midpoint (H)', 'human toxicity', 'HTPinf'),
    ('ReCiPe Midpoint (H)', 'marine eutrophication', 'MEP'),
    ('ReCiPe Midpoint (H)', 'climate change', 'GWP100'),
    ('ReCiPe Midpoint (H)', 'particulate matter formation', 'PMFP'),
    ('ReCiPe Midpoint (H)', 'agricultural land occupation', 'ALOP'),
    ('ReCiPe Midpoint (H)', 'freshwater eutrophication', 'FEP'),
    ('ReCiPe Midpoint (H)', 'metal depletion', 'MDP'),
    ('ReCiPe Midpoint (H)', 'terrestrial acidification', 'TAP100'),
    ('ReCiPe Midpoint (H)', 'water depletion', 'WDP'),
    ('ReCiPe Midpoint (H)', 'urban land occupation', 'ULOP'),
    ('ReCiPe Midpoint (H)', 'ionising radiation', 'IRP_HE'),
    ('ReCiPe Midpoint (H)', 'fossil depletion', 'FDP'),
    ('ReCiPe Midpoint (H)', 'freshwater ecotoxicity', 'FETPinf'),
    ('ReCiPe Midpoint (H)', 'marine ecotoxicity', 'METPinf'),
    ('ReCiPe Midpoint (H)', 'ozone depletion', 'ODPinf')
]

'''recipe_midpoint_article = [
    ('ReCiPe Midpoint (H)', 'natural land transformation', 'NLTP'),
    ('ReCiPe Midpoint (H)', 'climate change', 'GWP100'),
    ('ReCiPe Midpoint (H)', 'particulate matter formation', 'PMFP'),
    ('ReCiPe Midpoint (H)', 'water depletion', 'WDP')
]'''

recipe_endpoint_h_a = [
    ('ReCiPe Endpoint (H,A)', 'human health', 'total'),
    ('ReCiPe Endpoint (H,A)', 'ecosystem quality', 'total'),
    ('ReCiPe Endpoint (H,A)', 'resources', 'total')
]


recipe_midpoint_h_premise_gwp = [
    ('ReCiPe Midpoint (H)', 'terrestrial ecotoxicity', 'TETPinf'),
    ('ReCiPe Midpoint (H)', 'natural land transformation', 'NLTP'),
    ('ReCiPe Midpoint (H)', 'photochemical oxidant formation', 'POFP'),
    ('ReCiPe Midpoint (H)', 'human toxicity', 'HTPinf'),
    ('ReCiPe Midpoint (H)', 'marine eutrophication', 'MEP'),
# IMPORTANT: We are substituting the ReCiPe Midpoint (H) GWP100 with the GWP 100a, incl. H and bio CO2
# See https://github.com/polca/premise_gwp?tab=readme-ov-file#impact-category
    # ('ReCiPe Midpoint (H)', 'climate change', 'GWP100'),
    ('IPCC 2013', 'climate change', 'GWP 100a, incl. H and bio CO2'),
    ('ReCiPe Midpoint (H)', 'particulate matter formation', 'PMFP'),
    ('ReCiPe Midpoint (H)', 'agricultural land occupation', 'ALOP'),
    ('ReCiPe Midpoint (H)', 'freshwater eutrophication', 'FEP'),
    ('ReCiPe Midpoint (H)', 'metal depletion', 'MDP'),
    ('ReCiPe Midpoint (H)', 'terrestrial acidification', 'TAP100'),
    ('ReCiPe Midpoint (H)', 'water depletion', 'WDP'),
    ('ReCiPe Midpoint (H)', 'urban land occupation', 'ULOP'),
    ('ReCiPe Midpoint (H)', 'ionising radiation', 'IRP_HE'),
    ('ReCiPe Midpoint (H)', 'fossil depletion', 'FDP'),
    ('ReCiPe Midpoint (H)', 'freshwater ecotoxicity', 'FETPinf'),
    ('ReCiPe Midpoint (H)', 'marine ecotoxicity', 'METPinf'),
    ('ReCiPe Midpoint (H)', 'ozone depletion', 'ODPinf')
]


#### DATABASES ####

db_remindSSP1_baseline = [
 'EI38_cutoff_remind_SSP1-Base_2025_baseline',
 'EI38_cutoff_remind_SSP1-Base_2030_baseline',
 'EI38_cutoff_remind_SSP1-Base_2035_baseline',
 'EI38_cutoff_remind_SSP1-Base_2040_baseline'
]

db_remindSSP2_baseline = [
 'EI38_cutoff_remind_SSP2-Base_2025_baseline',
 'EI38_cutoff_remind_SSP2-Base_2030_baseline',
 'EI38_cutoff_remind_SSP2-Base_2035_baseline',
 'EI38_cutoff_remind_SSP2-Base_2040_baseline'
]

db_remindSSP5_baseline = [
 'EI38_cutoff_remind_SSP5-Base_2025_baseline',
 'EI38_cutoff_remind_SSP5-Base_2030_baseline',
 'EI38_cutoff_remind_SSP5-Base_2035_baseline',
 'EI38_cutoff_remind_SSP5-Base_2040_baseline'
]

db_remindSSP1_VSI = [
 'EI38_cutoff_remind_SSP1-Base_2025_VSI',
 'EI38_cutoff_remind_SSP1-Base_2030_VSI',
 'EI38_cutoff_remind_SSP1-Base_2035_VSI',
 'EI38_cutoff_remind_SSP1-Base_2040_VSI'
]

db_remindSSP2_VSI = [
 'EI38_cutoff_remind_SSP2-Base_2025_VSI',
 'EI38_cutoff_remind_SSP2-Base_2030_VSI',
 'EI38_cutoff_remind_SSP2-Base_2035_VSI',
 'EI38_cutoff_remind_SSP2-Base_2040_VSI', 
]

db_remindSSP5_VSI = [
 'EI38_cutoff_remind_SSP5-Base_2025_VSI',
 'EI38_cutoff_remind_SSP5-Base_2030_VSI',
 'EI38_cutoff_remind_SSP5-Base_2035_VSI',
 'EI38_cutoff_remind_SSP5-Base_2040_VSI' 
]

#### ACTIVITIES ####


activities_li = [
    ('spodumene production', 'AU'),
    ('spodumene production', 'RoW'),
    ('lithium carbonate production, from concentrated brine', 'GLO'),
    ('lithium brine inspissation', 'GLO'),
    ('lithium carbonate production, from spodumene', 'RoW'),
    ('lithium carbonate production, from spodumene', 'CN')
]

reference_product_lithium = 'lithium carbonate'

activities_ni = [
    ('treatment of metal part of electronics scrap, in copper, anode, by electrolytic refining', 'RoW'),

    ('platinum group metal mine operation, ore with high palladium content', 'RU'),

    ('platinum group metal, mine and concentration operations', 'ZA'),
    ('platinum group metal, extraction and refinery operations', 'ZA'),

    ('nickel mine operation and benefication to nickel concentrate, 16% Ni', 'CA-QC'),
    ('processing of nickel-rich materials', 'GLO'),
    
    ('nickel mine operation and benefication to nickel concentrate, 16% Ni', 'GLO'),
    ('smelting and refining of nickel concentrate, 16% Ni', 'GLO'),

    ('nickel mine operation and benefication to nickel concentrate, 7% Ni', 'CN'),
    ('smelting and refining of nickel concentrate, 7% Ni', 'CN'),

    ('cobalt production', 'GLO'),

    ('treatment of metal part of electronics scrap, in copper, anode, by electrolytic refining', 'SE')
]

reference_product_nickel = 'nickel, class 1'

activities_mn = [
    ('manganese concentrate production','GLO'),
    ('manganese(III) oxide production','CN'),
    ('manganese(III) oxide production','RoW'),
    ('manganese dioxide production', 'GLO'),
    ('manganese sulfate production', 'GLO')
]

reference_product_manganese = 'manganese sulfate'

activities_nmcoxide = [
    ('NMC111 oxide production, for Li-ion battery', 'CN')
]

reference_product_nmcoxide = 'NMC111 oxide'