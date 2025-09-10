# move_network

IRS provides data showing how many people moved between counties for each year
 between 2011 and 2022. This project examines movement patterns, projects future
 trends and infers policy recommendations.


## Training objectives
Skill maintenance is the major motivation for this project.  My training
 objective is to implement all sets of a project in Python and Palantir
 Foundry.

 1. Retrieve data from Census ACS, Census Tiger, and IRS SOI.
     + Palantir: Data Connection (with schedule and ingress policies)
     + Python: requests
 2. Refine data from each data source to a defect-free state.
     + Palantir: Pipeline Builder
     + Python: pyspark
 3. Reshape data to logical objects (e.g., nodes & edges).
     + Palantir: Ontology Manager
     + Python: pandas, geopandas
  4. Do descriptive analysis.
     + Palantir: Quiver
     + Python: pandas, iGraph
  5. Build model.
     + Palantir: Code Repository
     + Python: pytorch_geometric
  6. Visualize results
     + Palantir: Dash App
     + Python: dash


## Research questions

For the 2011 to 2022 time period:
+ How did US counties vary?
+ How did people move between US counties?

If a major US metro area declined:
+ Where would former inhabitants go?
+ Which other metro areas would benefit most?


 ## Planned files

00. execute_project
  + [ ] 00 execute_project.py
  + [ ] 01 define_settings.py
  + [ ] 02 define_utilities.py
10. get_data
  + [ ] 11 get_demography_data.py
  + [ ] 12 get_move_data.py
  + [ ] 13 get_geography_data.py
  + [ ] 14 get_polity_data.py
  + [ ] 15 get_climate_data.py (after MVP)
20. refine_data
  + [ ] 21 refine_demography_data.py
  + [ ] 22 refine_move_data.py
  + [ ] 23 refine_geography_data.py
  + [ ] 24 refine_polity_data.py
  + [ ] 25 refine_climate_data.py (after mvp)
30. make_objects
  + [ ] 31 compile_node_data.py
  + [ ] 32 compile_edge_data.py
40. describe_object
  + [ ] 41 describe_node.py
  + [ ] 42 describe_edge.py
50. model_object
  + [ ] 51 model_move.py
60. see_result
  + [ ] 61 see_node_result
  + [ ] 62 see_edge_result
  + [ ] 63 see_move_result


##########==========##########==========##########==========##########==========
