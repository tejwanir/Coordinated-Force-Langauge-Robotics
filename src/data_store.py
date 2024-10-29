from typing import Any, Optional, Union, List
import threading

class DataStore:
    def __init__(self, columns: Optional[int] = None, column_names: Optional[List[str]] = None):
        if columns is None and isinstance(column_names, (list, tuple)):
            columns = len(column_names)

        if not isinstance(columns, int) or columns < 1:
            raise ValueError(f'Invalid value for column: {columns}. Must be a counting number.')
        
        if len(column_names) != columns:
            raise ValueError(f'Invalid number of column names: {len(column_names)}. Must be equal to number of columns: {columns}.')
        
        self.data = tuple([] for _ in range(columns))
        
        self.column_names_to_index = {}

        if column_names is None:
            for i in range(columns):
                self.column_names_to_index[str(i)] = i
        else:
            for i, column_name in enumerate(column_names):
                if column_name in self.column_names_to_index:
                    raise ValueError(f"Duplicate column name found: '{column_name}'")
                
                self.column_names_to_index[column_name] = i

        self.data_changed = tuple(threading.Event() for _ in range(columns))

    def store(self, row: List[Any]):
        if len(row) != len(self.data):
            raise ValueError(f'Expected {len(self.data)} values, got {len(row)}.')
        
        for i, entry in enumerate(row):
            self.data[i].append(entry)

        for data_changed in self.data_changed:
            data_changed.set()

    def read_column(self, column: Union[str, int]):
        if isinstance(column, str):
            column_index = self.column_names_to_index[column]
            if self.data_changed[column_index].is_set():
                column_data = self.data[column_index]
                self.data_changed[column_index].clear()
                return column_data
        elif isinstance(column, int):
            if self.data_changed[column].is_set():
                column_data = self.data[column]
                self.data_changed[column_index].clear()
                return column_data
        else:
            raise ValueError(f"Expected a column name string or column index int but got '{column}' instead.")

    def read(self, columns: Optional[Union[List[Union[str, int]], Union[str, int]]] = None):
        if columns is None:
            return self.data
        elif isinstance(columns, (str, int)):
            return self.read_column(columns)
        elif isinstance(columns, (list, tuple)):
            return tuple(self.read_column(column) for column in columns)
        else:
            raise ValueError(f'Invalid columns: {columns}. Must be a sequence of strings and/or ints, a string, an int, or None.')
