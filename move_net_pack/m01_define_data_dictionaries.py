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
        ('geometry', 'geometry'   , 'shapes'  ,'shape'  , None),
        ('year'    , 'year'       , 'years'   ,'id'     , int),
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
        ('year'          , 'year'       , 'years'   ,'id'  , int),
    ]
}

## Create data dictionary for US state identifiers
state_dict = {
    'header': ('fips_state', 'id_state', 'name_state', 'use'),
    'columns':[
        ('01', 'AL', 'Alabama', True),
        ('02', 'AK', 'Alaska', False),
        ('04', 'AZ', 'Arizona', True),
        ('05', 'AR', 'Arkansas', True),
        ('06', 'CA', 'California', True),
        ('08', 'CO', 'Colorado', True),
        ('09', 'CT', 'Connecticut', True),
        ('10', 'DE', 'Delaware', True),
        ('11', 'DC', 'District of Columbia', True),
        ('12', 'FL', 'Florida', True),
        ('13', 'GA', 'Georgia', True),
        ('15', 'HI', 'Hawaii', False),
        ('16', 'ID', 'Idaho', True),
        ('17', 'IL', 'Illinois', True),
        ('18', 'IN', 'Indiana', True),
        ('19', 'IA', 'Iowa', True),
        ('20', 'KS', 'Kansas', True),
        ('21', 'KY', 'Kentucky', True),
        ('22', 'LA', 'Louisiana', True),
        ('23', 'ME', 'Maine', True),
        ('24', 'MD', 'Maryland', True),
        ('25', 'MA', 'Massachusetts', True),
        ('26', 'MI', 'Michigan', True),
        ('27', 'MN', 'Minnesota', True),
        ('28', 'MS', 'Mississippi', True),
        ('29', 'MO', 'Missouri', True),
        ('30', 'MT', 'Montana', True),
        ('31', 'NE', 'Nebraska', True),
        ('32', 'NV', 'Nevada', True),
        ('33', 'NH', 'New Hampshire', True),
        ('34', 'NJ', 'New Jersey', True),
        ('35', 'NM', 'New Mexico', True),
        ('36', 'NY', 'New York', True),
        ('37', 'NC', 'North Carolina', True),
        ('38', 'ND', 'North Dakota', True),
        ('39', 'OH', 'Ohio', True),
        ('40', 'OK', 'Oklahoma', True),
        ('41', 'OR', 'Oregon', True),
        ('42', 'PA', 'Pennsylvania', True),
        ('44', 'RI', 'Rhode Island', True),
        ('45', 'SC', 'South Carolina', True),
        ('46', 'SD', 'South Dakota', True),
        ('47', 'TN', 'Tennessee', True),
        ('48', 'TX', 'Texas', True),
        ('49', 'UT', 'Utah', True),
        ('50', 'VT', 'Vermont', True),
        ('51', 'VA', 'Virginia', True),
        ('53', 'WA', 'Washington', True),
        ('54', 'WV', 'West Virginia', True),
        ('55', 'WI', 'Wisconsin', True),
        ('56', 'WY', 'Wyoming', True),
        ('60', 'AS', 'American Samoa', False),
        ('66', 'GU', 'Guam', False),
        ('69', 'MP', 'Northern Mariana Islands', False),
        ('72', 'PR', 'Puerto Rico', False),
        ('74', 'UM', 'U.S. Minor Outlying Islands', False),
        ('78', 'VI', 'U.S. Virgin Islands', False),
    ]
}

##########==========##########==========##########==========##########==========
