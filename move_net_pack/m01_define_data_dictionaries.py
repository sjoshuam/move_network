# Create data dictionary for Census ACS data. See variable lists:
# https://api.census.gov/data/2016/acs/acs5/subject/groups/S0801.html
acs_dict = {
    'header': ('column', 'name', 'unit', 'aggregate', 'type'),
    'columns': [
    ('state'         ,'fips_state'  ,'states'  , 'id'   ,str),
    ('county'        ,'fips_county' ,'counties', 'id'   ,str),
    ('S0101_C01_001E','pop_age_all' ,'persons' ,'sum'   ,int),
    ('S0101_C01_002E','pop_age_00-04' ,'persons' ,'sum' ,int),
    ('S0101_C01_003E','pop_age_05-09' ,'persons' ,'sum' ,int),
    ('S0101_C01_004E','pop_age_10-14' ,'persons' ,'sum' ,int),
    ('S0101_C01_015E','pop_age_65-69' ,'persons' ,'sum' ,int),
    ('S0101_C01_016E','pop_age_70-74' ,'persons' ,'sum' ,int),
    ('S0101_C01_017E','pop_age_75-79' ,'persons' ,'sum' ,int),
    ('S1501_C01_006E','pop_edu_all' ,'persons' ,'sum'   ,int),
    ('S1501_C01_012E','pop_edu_ba'  ,'persons' ,'sum'   ,int),
    ('S1501_C01_013E','pop_edu_ma+' ,'persons' ,'sum'   ,int),
    ('S2301_C01_001E','pop_unemp_all','persons' ,'sum'  ,int),
    ('S2301_C04_002E','pop_unemp_rate','persons','sum'  ,float),
    ('S2503_C01_013E','hh_cost_inc' ,'dollars' ,'median',float),
    ('S2503_C01_024E','hh_cost_cost','dollars' ,'median',float),
    ('S2503_C01_028E','hh_cost_cost_pre2015', 'dollars', 'median',float),
    ('S0801_C01_046E','commute_time','minutes' ,'median',float),
    ]}

# Create data dictionary for IRS SOI county-to-county movement data
soi_dict = {
    'header': ('columns', 'name', 'unit', 'aggregate', 'type'),
    'columns': [
        ('y1_statefips' , 'y1_fips_state'  , 'state'  , 'id',  str),
        ('y1_countyfips', 'y1_fips_county' , 'county' , 'id',  str),
        ('y2_statefips' , 'y2_fips_state'  , 'state'  , 'id',  str),
        ('y2_countyfips', 'y2_fips_county' , 'county' , 'id',  str),
        ('n1'           , 'return_count'   , 'returns', 'sum', float),
        ('n2'           , 'person_count'   , 'persons', 'sum', float),
        ('agi'          , 'income_total'   , 'dollars', 'sum', float),
        ('year'         , 'year'           , 'years'  , 'id',  int),
    ]
}

# Create data dictionary for Census Tiger county shapefiles
tiger_dict = {
    'header': ('columns', 'name', 'unit', 'aggregate', 'type'),
    'columns':[
        ('STATEFP' , 'fips_state' , 'states'  , 'id'    , str),
        ('COUNTYFP', 'fips_county', 'counties', 'id'    , str),
        ('NAMELSAD', 'name_county', 'counties', 'id'    , str),
        ('CBSAFP'  , 'fips_cbsa'  , 'metros'  , 'subset', str),
        ('ALAND'   , 'area_land'  , 'km2'     , 'sum'   , int),
        ('AWATER'  , 'area_water' , 'km2'     , 'sum'   , int),
        ('INTPTLAT', 'coords_lat' , 'degrees' , 'id'    , float),
        ('INTPTLON', 'coords_lon' , 'degrees' , 'id'    , float),
    ]
}

# Create data dictionary for MIT Election Lab county-level presidential votes
mit_dict = {
    'header': ('columns', 'name', 'unit', 'aggregate', 'type'),
    'columns':[
        ('year'          , 'year'       , 'year'    , 'id' , int),
        ('state_po'      , 'usps_state' , 'states'  , 'id' , str),
        ('county_fips'   , 'fips_county', 'counties', 'id' , int),
        ('party'         , 'party_name' , 'parties' , 'id' , str),
        ('candidatevotes', 'party_votes', 'persons' , 'sum', int),
        ('totalvotes'    , 'total_votes', 'persons' , 'sum', int), 
    ]
}

## Create data dictionary for US state identifiers
state_dict = {
    'header': ('fips_state', 'id_state', 'name_state'),
    'columns':[
        ('01', 'AL', 'Alabama'),
        ('02', 'AK', 'Alaska'),
        ('04', 'AZ', 'Arizona'),
        ('05', 'AR', 'Arkansas'),
        ('06', 'CA', 'California'),
        ('08', 'CO', 'Colorado'),
        ('09', 'CT', 'Connecticut'),
        ('10', 'DE', 'Delaware'),
        ('11', 'DC', 'District of Columbia'),
        ('12', 'FL', 'Florida'),
        ('13', 'GA', 'Georgia'),
        ('15', 'HI', 'Hawaii'),
        ('16', 'ID', 'Idaho'),
        ('17', 'IL', 'Illinois'),
        ('18', 'IN', 'Indiana'),
        ('19', 'IA', 'Iowa'),
        ('20', 'KS', 'Kansas'),
        ('21', 'KY', 'Kentucky'),
        ('22', 'LA', 'Louisiana'),
        ('23', 'ME', 'Maine'),
        ('24', 'MD', 'Maryland'),
        ('25', 'MA', 'Massachusetts'),
        ('26', 'MI', 'Michigan'),
        ('27', 'MN', 'Minnesota'),
        ('28', 'MS', 'Mississippi'),
        ('29', 'MO', 'Missouri'),
        ('30', 'MT', 'Montana'),
        ('31', 'NE', 'Nebraska'),
        ('32', 'NV', 'Nevada'),
        ('33', 'NH', 'New Hampshire'),
        ('34', 'NJ', 'New Jersey'),
        ('35', 'NM', 'New Mexico'),
        ('36', 'NY', 'New York'),
        ('37', 'NC', 'North Carolina'),
        ('38', 'ND', 'North Dakota'),
        ('39', 'OH', 'Ohio'),
        ('40', 'OK', 'Oklahoma'),
        ('41', 'OR', 'Oregon'),
        ('42', 'PA', 'Pennsylvania'),
        ('44', 'RI', 'Rhode Island'),
        ('45', 'SC', 'South Carolina'),
        ('46', 'SD', 'South Dakota'),
        ('47', 'TN', 'Tennessee'),
        ('48', 'TX', 'Texas'),
        ('49', 'UT', 'Utah'),
        ('50', 'VT', 'Vermont'),
        ('51', 'VA', 'Virginia'),
        ('53', 'WA', 'Washington'),
        ('54', 'WV', 'West Virginia'),
        ('55', 'WI', 'Wisconsin'),
        ('56', 'WY', 'Wyoming'),
        ('60', 'AS', 'American Samoa'),
        ('66', 'GU', 'Guam'),
        ('69', 'MP', 'Northern Mariana Islands'),
        ('72', 'PR', 'Puerto Rico'),
        ('74', 'UM', 'U.S. Minor Outlying Islands'),
        ('78', 'VI', 'U.S. Virgin Islands'),
    ]
}

##########==========##########==========##########==========##########==========
