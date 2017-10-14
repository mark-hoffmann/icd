import numpy as np
import pandas as pd

def long_to_short_transformation(df, idx, icds):
    """
    Summary:
        Used for processing a dataframe from a long format where you want to roll up many claims into an episode for example,
        but aggregate all of the possible icd codes. This is a usual preprocessing step to then use function icd_to_comorbidities.
        REQUIRED: RESET THE INDEX BEFORE USING ON DF
        REQUIRED: DATAFRAME MUST ALREADY BE SORTED IN IDX AND SECONDAR_IDX THAT YOU ARE ROLLING UP
    
    Args:
        df (Pandas DataFrame): Dataframe containing the data witht he valid ids and columns holding the icd codes on a LONG dataset
        idx (str): id column name for reference on the output
        icds (list(strs)): list of columns that contain the icd codes
    
    Returns:
        New pandas DataFrame containing the ids specified with the rolled up icd codes appended wide wise with format icd_1, icd_2, ... icd_n
    """
    info_dict = {}
    current_icd_set = set()
    id_list = []
    unique_icd_count = 0
    current_id = ""
    last_id = df.loc[0,idx] #Initializing last_id to get over first iteration
    
    #Step 1
    #Populate the appropriate info and find the largest unique_icd_count to allocate column space
    for row in range(0,len(df)):
        #Initialize the new row id
        current_id = df.loc[row,idx]
        
        #Know when to switch to a new set and save the temp info
        if current_id != last_id:
            #update new dataframe column counter
            if len(current_icd_set) > unique_icd_count:
                unique_icd_count = len(current_icd_set)
            #save the icd set casted to a list for faster iteration in the next step
            info_dict[last_id] = list(current_icd_set)
            #clear the current set
            current_icd_set = set()
            
        #Loop over columns, adding to set 
        for col in icds:
            icd = df.loc[row,col]
            current_icd_set.add(icd)
        
        #Remember the last id for next loop
        last_id = current_id
    
    #Loop is done save out one last time for last record
    if len(current_icd_set) > unique_icd_count:
        unique_icd_count = len(current_icd_set)
    #save the icd set casted to a list for faster iteration in the next step
    info_dict[last_id] = list(current_icd_set)

    
    #Step 2
    #Create and populate output df
    
    #Need equal length lists if mapping a df from dict, so we pad the lists in the current dict
    for key in info_dict.keys():
        info_dict[key] += [''] * (unique_icd_count - len(info_dict[key]))
    
    #Populating the out_df
    out_df = pd.DataFrame.from_dict(info_dict, orient="index")
    
    #Creating columns list
    columns = ["icd_" + str(i) for i in range(0,unique_icd_count)]
    out_df.columns = columns #rename to out columns
    out_df[idx] = out_df.index.tolist() #Give us a column 'id' in addition in case we want to throw into icd_to_comorbidities next
    return(out_df)
