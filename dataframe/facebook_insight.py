import pandas as pd

class FacebookInsight(pd.DataFrame):
    def filter(self, *columns):
        return self.reindex(columns=columns)

    def get_action(self, column_name, action_type):
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