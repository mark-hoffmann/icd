import pandas as pd
import icd

import pytest

df = pd.DataFrame.from_dict({'icd_0': {1: 'F1P', 2: 'F322', 3: ''},
					 'icd_1': {1: 'F11', 2: 'C77', 3: 'G10'},
					 'icd_2': {1: '', 2: 'C737', 3: ''},
					 'icd_3': {1: 'E400', 2: 'F32', 3: ''},
					 'icd_4': {1: 'E40', 2: '', 3: ''},
					 'id': {1: 1, 2: 2, 3: 3}})


def test_invalid_stings():
	with pytest.raises(Exception):
		icd.icd_to_comorbidities(df, "id", ["icd_0","icd_1","icd_2","icd_3","icd_4"], mapping="bad_string")

def test_default_mapping():
	d = icd.icd_to_comorbidities(df, "id", ["icd_0","icd_1","icd_2","icd_3","icd_4"])

	validation_data = {'aids_hiv': {1: False, 2: False, 3: False},
						 'alcohol_abuse': {1: False, 2: False, 3: False},
						 'blood_loss_anemia': {1: False, 2: False, 3: False},
						 'cardiac_arrhythmia': {1: False, 2: False, 3: False},
						 'chronic_pulmonary_disease': {1: False, 2: False, 3: False},
						 'coagulopathy': {1: False, 2: False, 3: False},
						 'congestive_heart_failure': {1: False, 2: False, 3: False},
						 'deficiency_anemia': {1: False, 2: False, 3: False},
						 'depression': {1: False, 2: True, 3: False},
						 'diabetes_complicated': {1: False, 2: False, 3: False},
						 'diabetes_uncomplicated': {1: False, 2: False, 3: False},
						 'drug_abuse': {1: True, 2: False, 3: False},
						 'fluid_and_electrolyte_disorders': {1: False, 2: False, 3: False},
						 'hypertension_complicated': {1: False, 2: False, 3: False},
						 'hypertension_uncomplicated': {1: False, 2: False, 3: False},
						 'hypothyroidism': {1: False, 2: False, 3: False},
						 'id': {1: 1, 2: 2, 3: 3},
						 'liver_disease': {1: False, 2: False, 3: False},
						 'lymphoma': {1: False, 2: False, 3: False},
						 'metastatic_cancer': {1: False, 2: True, 3: False},
						 'obesity': {1: False, 2: False, 3: False},
						 'other_neurological_disorder': {1: False, 2: False, 3: True},
						 'paralysis': {1: False, 2: False, 3: False},
						 'peptic_ulcer_disease_excluding_bleeding': {1: False, 2: False, 3: False},
						 'peripheral vascular_disorder': {1: False, 2: False, 3: False},
						 'psychoses': {1: False, 2: False, 3: False},
						 'pulmonary_circulation_disorder': {1: False, 2: False, 3: False},
						 'renal_failure': {1: False, 2: False, 3: False},
						 'rheumatoid_arhritis': {1: False, 2: False, 3: False},
						 'solid_tumor_wo_metastasis': {1: False, 2: False, 3: False},
						 'valvular_disease': {1: False, 2: False, 3: False},
						 'weight_loss': {1: True, 2: False, 3: False}}

	assert d.to_dict(), validation_data


def test_quan_elixhauser10_mapping():
	d = icd.icd_to_comorbidities(df, "id", ["icd_0","icd_1","icd_2","icd_3","icd_4"], mapping="quan_elixhauser10")

	validation_data = {'aids_hiv': {1: False, 2: False, 3: False},
						 'alcohol_abuse': {1: False, 2: False, 3: False},
						 'blood_loss_anemia': {1: False, 2: False, 3: False},
						 'cardiac_arrhythmia': {1: False, 2: False, 3: False},
						 'chronic_pulmonary_disease': {1: False, 2: False, 3: False},
						 'coagulopathy': {1: False, 2: False, 3: False},
						 'congestive_heart_failure': {1: False, 2: False, 3: False},
						 'deficiency_anemia': {1: False, 2: False, 3: False},
						 'depression': {1: False, 2: True, 3: False},
						 'diabetes_complicated': {1: False, 2: False, 3: False},
						 'diabetes_uncomplicated': {1: False, 2: False, 3: False},
						 'drug_abuse': {1: True, 2: False, 3: False},
						 'fluid_and_electrolyte_disorders': {1: False, 2: False, 3: False},
						 'hypertension_complicated': {1: False, 2: False, 3: False},
						 'hypertension_uncomplicated': {1: False, 2: False, 3: False},
						 'hypothyroidism': {1: False, 2: False, 3: False},
						 'id': {1: 1, 2: 2, 3: 3},
						 'liver_disease': {1: False, 2: False, 3: False},
						 'lymphoma': {1: False, 2: False, 3: False},
						 'metastatic_cancer': {1: False, 2: True, 3: False},
						 'obesity': {1: False, 2: False, 3: False},
						 'other_neurological_disorder': {1: False, 2: False, 3: True},
						 'paralysis': {1: False, 2: False, 3: False},
						 'peptic_ulcer_disease_excluding_bleeding': {1: False, 2: False, 3: False},
						 'peripheral vascular_disorder': {1: False, 2: False, 3: False},
						 'psychoses': {1: False, 2: False, 3: False},
						 'pulmonary_circulation_disorder': {1: False, 2: False, 3: False},
						 'renal_failure': {1: False, 2: False, 3: False},
						 'rheumatoid_arhritis': {1: False, 2: False, 3: False},
						 'solid_tumor_wo_metastasis': {1: False, 2: False, 3: False},
						 'valvular_disease': {1: False, 2: False, 3: False},
						 'weight_loss': {1: True, 2: False, 3: False}}

	assert d.to_dict(), validation_data

def test_charlson_mapping():
	d = icd.icd_to_comorbidities(df, "id", ["icd_0","icd_1","icd_2","icd_3","icd_4"], mapping="charlson10")

	validation_data = {'aids_hiv': {1: False, 2: False, 3: False},
						 'cancer': {1: False, 2: False, 3: False},
						 'cerebrovascular_disease': {1: False, 2: False, 3: False},
						 'chronic_pulmonary_disease': {1: False, 2: False, 3: False},
						 'congestive_heart_failure': {1: False, 2: False, 3: False},
						 'connective_tissue_disease_rheumatic_disease': {1: False, 2: False, 3: False},
						 'dementia': {1: False, 2: False, 3: False},
						 'diabetes_w_complications': {1: False, 2: False, 3: False},
						 'diabetes_wo_complications': {1: False, 2: False, 3: False},
						 'id': {1: 1, 2: 2, 3: 3},
						 'metastitic_carcinoma': {1: False, 2: True, 3: False},
						 'mild_liver_disease': {1: False, 2: False, 3: False},
						 'moderate_or_sever_liver_disease': {1: False, 2: False, 3: False},
						 'myocardial_infarction': {1: False, 2: False, 3: False},
						 'paraplegia_and_hemiplegia': {1: False, 2: False, 3: False},
						 'peptic_ulcer_disease': {1: False, 2: False, 3: False},
						 'periphral_vascular_disease': {1: False, 2: False, 3: False},
						 'renal_disease': {1: False, 2: False, 3: False}}

	assert d.to_dict(), validation_data

def test_custom_mapping():
	custom_map = {"paraplegia_and_hemiplegia":['G81','G82','G041','G114','G801','G802','G830','G831','G832','G833','G834','G839'],
				    "renal_disease":['N18','N19','N052','N053','N054','N055','N056','N057','N250','I120','I131','N032','N033','N034','N035','N036','N037','Z490','Z491','Z492','Z940','Z992'],
				    "cancer":['C00','C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21','C22','C23','C24','C25','C26','C30','C31','C32','C33','C34','C37','C38','C39','C40','C41','C43','C45','C46','C47','C48','C49','C50','C51','C52','C53','C54','C55','C56','C57','C58','C60','C61','C62','C63','C64','C65','C66','C67','C68','C69','C70','C71','C72','C73','C74','C75','C76','C81','C82','C83','C84','C85','C88','C90','C91','C92','C93','C94','C95','C96','C97'],
				    "moderate_or_sever_liver_disease":['K704','K711','K721','K729','K765','K766','K767','I850','I859','I864','I982'],
				    "metastitic_carcinoma":['C77','C78','C79','C80'],
				    "aids_hiv":['B20','B21','B22','B24']
				  }

	d = icd.icd_to_comorbidities(df, "id", ["icd_0","icd_1","icd_2","icd_3","icd_4"], mapping=custom_map)

	validation_data = {'aids_hiv': {1: False, 2: False, 3: False},
						 'cancer': {1: False, 2: False, 3: False},
						 'id': {1: 1, 2: 2, 3: 3},
						 'metastitic_carcinoma': {1: False, 2: True, 3: False},
						 'moderate_or_sever_liver_disease': {1: False, 2: False, 3: False},
						 'paraplegia_and_hemiplegia': {1: False, 2: False, 3: False},
						 'renal_disease': {1: False, 2: False, 3: False}}

	assert d.to_dict(), validation_data


