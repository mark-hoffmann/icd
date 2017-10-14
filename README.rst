icd
===

.. image:: https://img.shields.io/pypi/v/icd.svg
    :target: https://pypi.python.org/pypi/icd
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/mark-hoffmann/icd.png
   :target: https://travis-ci.org/mark-hoffmann/icd
   :alt: Latest Travis CI build status

.. image:: https://codecov.io/gh/mark-hoffmann/icd/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/mark-hoffmann/icd
   :alt: Coverage

Tools for working with icd codes and comorbidities. This was inspired by the R package, `icd <https://cran.r-project.org/web/packages/icd/index.html>`_, as a simple python implementation for some of the base functionality. This has been benchmarked to be able to hand large datasets (tens of millions of rows) for various icd code manipulation tasks.

If you would be interested in helping contribute to this repository, feel free to `send me an email <markkhoffmann@gmail.com>`_.

Usage
-----
Basic usage includes two very common tasks while dealing with icd code data. 

- Transforming datasets from a long to wide format
- Processing icd codes for known comorbidity mappings

|
|

**Transforming from long to wide**


Data is commonly in a long format that may have a key for an individual such as *person_id* with many claims *claim_id* belonging to it. 

For example:

+------------+------------+-----------+------------+------------+
| claim_id   | person_id  | icd_cd_1  |  icd_cd_2  |  icd_cd_3  |
+============+============+===========+============+============+
|    001     |    A       | code_6    |  code_2    |            |
+------------+------------+-----------+------------+------------+
|    002     |    A       | code_8    |            |            |
+------------+------------+-----------+------------+------------+
|    003     |    A       | code_3    |  code_2    |  code_6    |
+------------+------------+-----------+------------+------------+
|    004     |    B       | code_1    |            |            |
+------------+------------+-----------+------------+------------+
|    005     |    B       | code_2    |  code_3    |            |
+------------+------------+-----------+------------+------------+
|    006     |    C       | code_4    |  code_2    |  code_5    |
+------------+------------+-----------+------------+------------+

For easier processing, we must transform the table into a more collapsed version. The number of *icd* columns then becomes the maximum unique codes for any given *person_id*.

Such as:

+------------+-----------+------------+------------+------------+
| person_id  | icd_cd_1  |  icd_cd_2  |  icd_cd_3  |   icd_cd_4 |
+============+===========+============+============+============+
|    A       |  code_6   | code_2     |  code_8    |    code_3  |
+------------+-----------+------------+------------+------------+
|    B       |  code_1   | code_2     |  code_3    |            |
+------------+-----------+------------+------------+------------+
|    C       |  code_4   | code_2     |  code_5    |            |
+------------+-----------+------------+------------+------------+

To accomplish this task, simply use the function *long_to_short_transformation* as such:

.. code-block:: python
  
  import pandas as pd 
  import icd

  data = {"person_id":[1,1,1,2,2,3],
           "dx_1":["F11","E40","","F32","C77","G10"],
           "dx_2":["F1P","E400","","F322","C737",""]}
  df = pd.DataFrame.from_dict(data)
  icd.long_to_short_transformation(df,"person_id",["dx_1","dx_2"])

Where *df* is your pandas dataframe, *"person_id"* is the column you want to roll up on, and *["dx_1","dx_2"]* is the array of columns that contain icd codes.

It is important to note that even if you only have one icd column, it **must still be an array**. Also, you must **impute NaN values** to be an **empty string** such as "".

The function will return a new dataframe with index of *person_id*, a column of *person_id*, as well as as many unique columns as needed in the following form *icd_0*, *icd_1*, ... , *icd_n*.

|
|

**Processing icd codes to known comorbidities**

The second task has to do with actually mapping comorbidities to these icd codes. For this, you can use the function *icd_to_comorbidities*. This can be seen from going from a table of the format:

+------------+-----------+------------+------------+------------+
| person_id  | icd_cd_1  |  icd_cd_2  |  icd_cd_3  |   icd_cd_4 |
+============+===========+============+============+============+
|    A       |  code_6   | code_2     |  code_8    |    code_3  |
+------------+-----------+------------+------------+------------+
|    B       |  code_1   | code_2     |  code_3    |            |
+------------+-----------+------------+------------+------------+
|    C       |  code_4   | code_2     |  code_5    |            |
+------------+-----------+------------+------------+------------+

To the format:

+------------+-----------+------------+------------+------------+
| person_id  | comorb_1  |  comorb_2  |  comorb_3  |   comorb_4 |
+============+===========+============+============+============+
|    A       |  True     | False      |  True      |    True    |
+------------+-----------+------------+------------+------------+
|    B       |  False    | True       |  False     |     False  |
+------------+-----------+------------+------------+------------+
|    C       |  False    | False      |  False     |   False    |
+------------+-----------+------------+------------+------------+

This comorbidity mapping is pending on the mapping used.

|

An example of doing is is carried out as such:

.. code-block:: python

  import pandas as pd
  import icd

  df = pd.DataFrame.from_dict({'icd_0': {1: 'F1P', 2: 'F322', 3: ''},
		               'icd_1': {1: 'F11', 2: 'C77', 3: 'G10'},
			       'icd_2': {1: '', 2: 'C737', 3: ''},
			       'icd_3': {1: 'E400', 2: 'F32', 3: ''},
		               'icd_4': {1: 'E40', 2: '', 3: ''},
			       'person_id': {1: 1, 2: 2, 3: 3}})
  icd.icd_to_comorbidities(df, "person_id", ["icd_0","icd_1","icd_2","icd_3","icd_4"])

|

The default default mapping is the *quan_elixhauser10*, which is a transcription by Quan of the original Elixhauser icd 9 comorbidities in the `following paper <https://www.ncbi.nlm.nih.gov/pubmed/16224307>`_.

Optionally, you can provide a *mapping* keyword argument as such:

.. code-block:: python

  icd.icd_to_comorbidities(df, "person_id", ["icd_0","icd_1","icd_2","icd_3","icd_4"], mapping="quan_elixhauser10")

The currently supported mappings are the default *"quan_elixhauser10"* as well as the *"charlson10"* mapping as referenced from the same paper above. Additionally, you can find them laid out in SAS code `here <http://web.archive.org/web/20110225042437/http://www.chaps.ucalgary.ca/sas>`_.


If you want to to create a custom comborbidity mapping, simply pass in a dict for the mapping argument instead of a supported keyword string. The dict must follow the following format as such:

.. code-block:: python

  custom_mapping = {"paraplegia_and_hemiplegia":['G81','G82','G041','G114','G801','G802','G830','G831','G832','G833','G834','G839'],
				    "renal_disease":['N18','N19','N052','N053','N054','N055','N056','N057','N250','I120','I131','N032','N033','N034','N035','N036','N037','Z490','Z491','Z492','Z940','Z992'],
				    "cancer":['C00','C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21','C22','C23','C24','C25','C26','C30','C31','C32','C33','C34','C37','C38','C39','C40','C41','C43','C45','C46','C47','C48','C49','C50','C51','C52','C53','C54','C55','C56','C57','C58','C60','C61','C62','C63','C64','C65','C66','C67','C68','C69','C70','C71','C72','C73','C74','C75','C76','C81','C82','C83','C84','C85','C88','C90','C91','C92','C93','C94','C95','C96','C97'],
				    "moderate_or_sever_liver_disease":['K704','K711','K721','K729','K765','K766','K767','I850','I859','I864','I982'],
				    "metastitic_carcinoma":['C77','C78','C79','C80'],
				    "aids_hiv":['B20','B21','B22','B24']
				  }
  icd.icd_to_comorbidities(df, "person_id", ["icd_0","icd_1","icd_2","icd_3","icd_4"], mapping=custom_mapping)

The above function returns a new DataFrame with the *person_id* values as the index, a column of whatever "person_id" string is passed in, along with a column for every comorbidity populated with either **True** or **False**.

Installation
------------

icd can easily be downloaded from Pypi package index via the following:

.. code-block:: python

  pip install icd



Requirements
^^^^^^^^^^^^
- `pandas <https://github.com/pandas-dev/pandas>`_

Compatibility
-------------

icd currently supports Python 3.4, 3.5, and 3.6

Licence
-------

`MIT <https://github.com/mark-hoffmann/icd/blob/master/LICENSE.txt>`_

Authors
-------

`icd` was written by `Mark Hoffmann <markkhoffmann@gmail.com>`_.