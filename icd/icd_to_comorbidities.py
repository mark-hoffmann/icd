import numpy as np
import pandas as pd
import json
import os

def icd_to_comorbidities(df, idx, icds, mapping="quan_elixhauser10"):
    """
    Summary:
        Used for processing dataframe from having icd codes in multiple columns to the comorbidities based on a valid mapping

    Args:
        df (Pandas DataFrame): Dataframe containing the data with the valid ids and columns holding icd codes
        mapping (json str:list(str)): mapping to use for the comorbidity lookup ex. elixhauser, charlson
        idx (str): id column name for reference on the output
        icds (list(strs)): list of columns that contain the icd codes

    Returns:
        New Pandas DataFrame containing the ids specified with same name along with the comorbidites containing Bools True \
        or False if the icd code was found in the mapping

    """
    validMappings = ["quan_elixhauser10", "charlson10"]

    if isinstance(mapping, str) and mapping not in validMappings:
    	raise Exception("Didn't recognize comorbidity mapping. Please use a valid comorbidity or create your own.")

    if isinstance(mapping, str):
        script_dir = os.path.dirname(__file__)
        rel_path = "comorbidity_mappings/" + mapping + ".json"
        file_path = os.path.join(script_dir, rel_path)

        mapping = json.load(open(file_path))
    elif isinstance(mapping, dict):
        pass
    else:
        raise Exception("Bad mapping type")


    comorb_cols = list(mapping.keys())
    comorb_df = pd.DataFrame(index=df[idx], columns=comorb_cols)

    for comorb in comorb_cols:
        #reset truth list then
        #Create a list of lists, will end up with rows of df by len(idxs) long
        truth_list = [[any([m for m in [x] if any(s in m for s in mapping[comorb])]) for x in df[idx]] for idx in icds]

        #Swapping dimensions on list of lists so we can apply a listwise operation to the longer dimension (rows of df)
        truth_list = list(map(list, zip(*truth_list)))

        #Condense the icd truth dimensions on a column basis to get a bool yes or no if multiple or at least one icd code is true
        condensed_truth = [any(truth_list[i]) == True for i in range(0,len(truth_list))]

        #assign the column of comorb_df with the appropriate truth values
        comorb_df[comorb] = condensed_truth

    comorb_df[idx] = comorb_df.index.tolist()

    return comorb_df
