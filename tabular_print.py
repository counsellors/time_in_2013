teams_list = ["Man Utd", "Man City", "T Hotspur"]
data = ([[1, 2, 1],[0, 1, 0],[2, 4, 2]])
row_format ="{:>20}" * (len(teams_list) + 1)
print row_format.format("", *teams_list)
#zip函数是将多个序列的第n个元素取出,拼成新的数组,当然,按序列的最小数输出。
for team, row in zip(teams_list, data):
        print row_format.format(team, *row)
