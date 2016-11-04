import csv

dates = ['2013-02-01', '2013-02-04', '2013-02-05', '2013-02-05', '2013-02-06', '2013-02-07', '2013-02-09', '2013-02-10', '2013-02-11']
ids = [395, 397, 398, 399, 400, 401, 500, 501, 502]
names = ['atm-four', 'atm-three', 'cash-five', 'cash-four', 'atm-two', 'atm-one', 'cash-three', 'cash-two', 'cash-one']
amounts = [25, 50, 100, 10, 10, 80, 10, 55, 25]
cash_detected = [False, False, True, True, False, False, True, True, True]
atm_detected = [True, True, False, False, True, True, False, False, False]

with open('challenge_test.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerow(['id'] + ['name'] + ['amount'] + ['date'] + ['is_cash'] + ['is_atm'])
    for i in range(9):
        a.writerow([str(ids[9 - i - 1])] + [names[9 - i - 1]] + [str(amounts[9 - i - 1])] + [dates[9 - i - 1]] + [str(cash_detected[9 - i - 1])] + [str(atm_detected[9 - i - 1])])
        
        