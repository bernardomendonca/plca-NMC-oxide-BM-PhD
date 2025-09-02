# Life cycle assessment of battery minerals to 2040: contribution of voluntary sustainability initiatives

This repository supports the analysis presented in the article:

**Life cycle assessment of battery minerals to 2040: contribution of voluntary sustainability initiatives**  
by Bernardo Mendonca Severiano¹\*, Stephen A. Northey¹, Carina Harpprecht² ³, Damien Giurco¹  
¹ University of Technology Sydney, Institute for Sustainable Futures, Bldg 10, 235 Jones St, Ultimo NSW 2007  
² German Aerospace Center (DLR), Institute of Networked Energy Systems, Curiestr. 4, 70563 Stuttgart, Germany  
³ Leiden University, Institute of Environmental Sciences (CML), P.O.Box 9518, 2300 RA Leiden, The Netherlands  
\* Corresponding Author. Email: Bernardo.MendoncaSeveriano@student.uts.edu.au

---

## Overview

This codebase enables prospective life cycle impact assessment (LCIA) of mining and refining operations for battery minerals under future scenarios, including the contribution of mitigation strategies inspired by voluntary sustainability initiatives (VSIs). The framework is built using Brightway2.5 and premise, and is structured around reusable Python modules and analytical Jupyter notebooks.

---

## Structure

### Jupyter Notebooks

| Notebook | Description |
|---------|-------------|
| `1_loading_datasets.ipynb` | Load and inspect Brightway2-compatible databases |
| `2_generating_datasets.ipynb` | Generate and duplicate scenario-specific databases |
| `3_foreground_analysis.ipynb` | Run LCIA on specific foreground activities |
| `4_background_analys.ipynb` | Perform background system LCIA |
| `5_contribution_analysis.ipynb` | Analyze exchange-level contributions |
| `6_individual_inventory_generation.ipynb` | Perform detailed inventory and impact calculations |
| `7_exchange_update.ipynb` | Apply scaling coefficients to flows |
| `8_synthesis.ipynb` | Compare baseline vs. VSI scenarios across time |
| `9_visualisation.ipynb` | Generate radar plots of results |
| `10_useful_db_operations.ipynb` | Support operations like loading or naming scenario databases |

---

### Python Scripts

| Script | Purpose |
|--------|---------|
| `config.py` | Stores impact method lists, activity tuples, and scenario database names |
| `database_setup.py` | Find activities, extract results, and convert outputs to DataFrames |
| `lifecycle.py` | Core LCIA methods for individual and comparative assessments |
| `activity_modify.py` | Apply exchange scaling (temporary or permanent) and collect results |
| `data_parsing.py` | Combine CSVs and convert them to structured Excel files |
| `plotting.py` | Radar plots and comparative tables using Matplotlib |
| `synthesis.py` | Aggregates LCIA results to summarize VSI and baseline changes |

---