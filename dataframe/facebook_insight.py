import pandas as pd

class FacebookInsight(pd.DataFrame):
    def get_action(self, column_name = None, action_type = None):
        if column_name is None or action_type is None:
            raise ValueError("The key column_name and action_type is required")
        if type(column_name) is not str:
            raise TypeError("The key column_name must be a string")
        if type(action_type) is not str:
            raise TypeError("The key action_type must be a string")

        temp = []
        for items in self[column_name]:
            if type(items) is not list:
                temp.append(0)
                continue
            for item in items:
                if item["action_type"] == action_type:
                    temp.append(item["value"])
                    break
            else:
                temp.append(0)
        return temp


    def sort(self, column_name=None, ascending=None):
        if column_name is None or ascending is None:
            raise ValueError("The key column_name and ascending is required")
        if type(column_name) is not str:
            raise TypeError("The key column_name must be a string")
        if type(ascending) is not bool:
            raise TypeError("The key ascending must be a boolean")

        return FacebookInsight(self.sort_values(by=column_name, ascending=ascending, ignore_index=True))