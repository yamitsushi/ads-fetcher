import pandas as pd

class FacebookInsight(pd.DataFrame):
    def limit(self, columns):
        return self.reindex(columns=columns)


    def get_roas(self, column_name):
        temp = []
        for items in self["purchase_roas"]:
            if type(items) is not list:
                temp.append(0.0)
                continue
            for item in items:
                print(item)
                if item["action_type"] == "omni_purchase":
                    temp.append(float(item["value"]))
                    break
            else:
                temp.append(0.0)

        self[column_name] = temp


    def get_purchase(self, column_name):
        temp = []

        for items in self["actions"]:
            if type(items) is not list:
                temp.append(0)
                continue
            for item in items:
                if item["action_type"] == "purchase":
                    temp.append(int(item["value"]))
                    break
            else:
                temp.append(0)

        self[column_name] = temp


    def get_revenue(self, column_name):
        self[column_name] = self["roas"].astype(float) * self["spend"].astype(float)