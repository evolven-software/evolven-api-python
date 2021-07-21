import pandas as pd
import json

class ApiResultObject(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

    def __repr__(self):
        return "{%s}"%", ".join(["%s: %s"%(key, self.__dict__[key]) for key in self.__dict__])
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
    
    def toDict(self):
        return self.__dict__

    def toDataFrame(self, records_path):
        
        cols = None
        try:
            cols = self.Next.Table.Columns.Column
            if type(cols) != list:
                cols = [cols]
        except:
            pass

        object_path = records_path.split(".")
        records = self
        for obj in object_path:
            if obj in records.__dict__:
                records = getattr(records, obj)
            else:
                return pd.DataFrame()

        if records:
            records = records if type(records) == list else [records]
            if len(records) > 0:
                data = [r.toDict() for r in records]
                
                if cols is not None:
                    L = len(cols)
                    for d in data:
                        for idx in range(L):
                            col = cols[idx]["Name"]
                            val = d["Cell"][idx]["Value"] if type(d["Cell"])==list else d["Cell"]["Value"]
                            d[col] = val
                        del d["Cell"]
                return pd.DataFrame.from_records(data)
                #return pd.DataFrame.from_records([r.toDict() for r in records])
    
        return pd.DataFrame()


    # enables adding of attributes
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
    
