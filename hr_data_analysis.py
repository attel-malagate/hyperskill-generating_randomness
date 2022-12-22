import pandas as pd
import requests
import os

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')
#
#         # All data in now loaded to the Data folder.

office_a = pd.read_xml('../Data/A_office_data.xml')
office_b = pd.read_xml('../Data/B_office_data.xml')
hr_data = pd.read_xml('../Data/hr_data.xml')

office_a.index = ['A' + str(a) for a in office_a['employee_office_id']]
office_b.index = ['B' + str(b) for b in office_b['employee_office_id']]
hr_data.set_index('employee_id', inplace=True)

office_combine = pd.concat([office_a, office_b])
office_merge = office_combine.merge(hr_data, left_index=True, right_index=True, indicator=True)

office_merge.drop(['employee_office_id', '_merge'], axis=1, inplace=True)
office_merge.sort_index(inplace=True)

hard_working = office_merge.sort_values("average_monthly_hours", ascending=False)[:10]
# print(hard_working.Department.tolist())

low_salary_projects = office_merge.query("Department == 'IT' & salary == 'low'")
# print(low_salary_projects.number_project.sum())

specific_employ = office_merge.loc[["A4", "B7064", "A3033"], ["last_evaluation", "satisfaction_level"]]
# print(specific_employ.values.tolist())


def frac(series):
    return series.count() / 5982


def count_bigger_5(series):
    counter = 0
    for employee in series:
        if employee > 5:
            counter += 1
    return counter
table = round(office_merge.groupby(["left"]).agg({"number_project": ["median", count_bigger_5], "time_spend_company":
    ["mean", "median"], "Work_accident": "mean", "last_evaluation": ["mean", "std"]}), 2)

pt_1 = office_merge.pivot_table(aggfunc='median', values='average_monthly_hours', index="Department", columns=["left", "salary"])
ans_1 = round(pt_1.loc[(pt_1[(0,'high')] < pt_1[(0,'medium')]) | (pt_1[(1,'low')] < pt_1[(1,'high')])], 2)
print(ans_1.to_dict())

pt_2 = round(office_merge.pivot_table(aggfunc=["min", "max", "mean"], values=["satisfaction_level", "last_evaluation"],
                                      index='time_spend_company', columns='promotion_last_5years'), 2)
ans_2 = pt_2.loc[pt_2[('mean', 'last_evaluation', 0)] > pt_2[('mean', 'last_evaluation', 1)]]
print(ans_2.to_dict())
