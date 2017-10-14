
import pandas as pd
import icd as icd

#from icd import long_to_short_transformation
#from icd import icd_to_comorbidities
# Sample Test passing with nose and pytest

def test_long_to_short_transformation():
	d_data = {"id":[1,1,1,2,2,3],"idx_roll":["A","B","C","A","B","A"],"dx_1":["F11","E40","","F32","C77","G10"],"dx_2":["F1P","E400","","F322","C737",""]}
	d = pd.DataFrame.from_dict(d_data)
	d2 = icd.long_to_short_transformation(d,"id",["dx_1","dx_2"])

	validation_data = {'icd_0': {1: 'F1P', 2: 'F322', 3: ''},
						 'icd_1': {1: 'F11', 2: 'C77', 3: 'G10'},
						 'icd_2': {1: '', 2: 'C737', 3: ''},
						 'icd_3': {1: 'E400', 2: 'F32', 3: ''},
						 'icd_4': {1: 'E40', 2: '', 3: ''},
						 'id': {1: 1, 2: 2, 3: 3}}

	assert d2.to_dict(orient="dict"), validation_data
