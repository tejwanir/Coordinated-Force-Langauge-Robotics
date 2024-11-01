from typing import Any, Callable, Dict, Optional, List, Tuple, Union
import threading
import pandas as pd

class DataBuffer:
    def __init__(self, data=None):
        self._data = data
        self._write_flag = threading.Event()
        self._read_flag = threading.Event()

        self._write_flag.set()
        self._read_flag.clear()

    def written_since_last_read(self):
        return self._write_flag.is_set()

    def read_since_last_write(self):
        return self._read_flag.is_set()

    def write(self, new_data):
        self._data = new_data
        self._write_flag.set()
        self._read_flag.clear()

    def safe_write(self, new_data):
        if not self.read_since_last_write():
            raise RuntimeError("Can't write to buffer because current contents haven't been read yet.")

        self.write(new_data)

    def read(self):
        data = self._data
        self._read_flag.set()
        self._write_flag.clear()
        return data
    
    def safe_read(self):
        if not self.written_since_last_read():
            raise RuntimeError("Can't read buffer because new data hasn't been written yet.")
        
        return self.read()
    
class TabularDataStore:
    def __init__(self, columns: Optional[int] = None, column_names: Optional[List[str]] = None):
        if columns is None and column_names is None:
            raise ValueError('Must specify at least number of columns or column names.')
        
        if column_names is None:
            column_names = []

        duplicate_column_names = [name for name in set(column_names) if column_names.count(name) > 1]
        if duplicate_column_names:
            raise ValueError(f'Duplicate column names found: {", ".join(duplicate_column_names)}.')

        if columns is not None:
            for i in range(columns):
                if i >= len(column_names):
                    column_names.append(f'column_{i}')

            column_names = column_names[:columns]

        self.column_names = column_names
        self._table = DataBuffer({column_name:[] for column_name in column_names})

    def updated_since_last_read(self):
        return self._table.written_since_last_read()

    def read_since_last_update(self):
        return self._table.read_since_last_write()

    def append_row(self, row_data: Tuple[Any]):
        if len(row_data) != len(self.column_names):
            raise ValueError("Row data does not match number of columns.")
        
        table = self._table.read()
        for i, column_name in enumerate(self.column_names):
            table[column_name].append(row_data[i])
        self._table.write(table)

    def get_column(self, column: Union[int, str]) -> List[Any]:
        table = self._table.read()
        if isinstance(column, int):
            if column < 0 or column >= len(self.column_names):
                raise IndexError("Column index out of range.")
            column_name = self.column_names[column]
        elif isinstance(column, str):
            column_name = column
            if column_name not in table:
                raise KeyError(f"Column '{column_name}' does not exist.")
        else:
            raise TypeError("Column must be specified by index (int) or name (str).")
        
        return table[column_name]
    
    def get_all_columns(self, ordered: bool = False) -> Union[Dict[str, List[Any]], Tuple[List[Any]]]:
        table = self._table.read()
        if ordered:
            table = tuple(table[column_name] for column_name in self.column_names)
        return table
    
    def __getitem__(self, key: Union[int, str, List[Union[int, str]]]) -> Union[List[Any], Dict[str, List[Any]]]:
        if isinstance(key, (int, str)):
            return self.get_column(key)
        elif isinstance(key, (list, tuple)):
            return tuple(self.get_column(k) for k in key)
        else:
            raise TypeError(f"Key must be an integer, string, or list of integers/strings. Instead got: {key}")
        
    def run_if_updated(self, method: Callable):
        if self.updated_since_last_read():
            method()

    def __len__(self):
        return len(self.get_column(0))
    
    def to_pandas(self):
        return pd.DataFrame(self.get_all_columns(), columns=self.column_names)