# Commons data model

This creates a common data model to be used
in the finngen project.

The current objects are currently modeled.

 - Variant
 - Locus

Data products

 - Colocalization


## Overview

The following class methods are provided.

 __str__ : string representation of object
 json_rep : json representation of object
 __repr__ : shallow representation of object
 __composite_values__ : needed to persist in sqlalchemy

The following static methods are providied.

 columns : sqlalchemy columns 
 from_str : construct objecct by parsing

