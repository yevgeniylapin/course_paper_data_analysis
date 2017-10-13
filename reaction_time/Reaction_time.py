from math import log
import operator
import re
from statistics import stdev

with open('stimuli.txt', 'r', encoding = 'utf-8') as f:
	stimuli = f.read().split('\n')

with open('younger_august.csv', 'r', encoding = 'utf-8') as f_y: #вставь название файла про молодых
	younger_database = f_y.read().split('\n')

with open('older_august.csv', 'r', encoding = 'utf-8') as f_o: #вставь название файла про пожилых
	older_database = f_o.read().split('\n')

def create_time_info_table(db, name):
	art = []
	min_rt = []
	max_rt = []
	stdev_rt = []
	art_abs = []
	min_rt_abs = []
	max_rt_abs = []
	stdev_rt_abs = []
	
	for line in db[1:]:
		line = line.split('\t')
		t = line[5::4]
		t_st = line[6::4]
		times = []
		times_abs = []
		times_sum = 0
		times_abs_sum = 0
		for i in range(len(t)):
			try:
				times_sum += int(t[i])
				times.append(int(t[i]))
				try:
					tmp = int(t_st[i])
				except:
					tmp = 0
				times_abs.append(times[-1] - tmp)
				times_abs_sum += times[-1] - tmp
			except:
				continue
		
		n = len(times)
		print(n)
		art.append(times_sum/n)
		min_rt.append(min(times))
		max_rt.append(max(times))
		stdev_rt.append(stdev(times))
		art_abs.append(times_abs_sum/n)
		min_rt_abs.append(min(times_abs))
		max_rt_abs.append(max(times_abs))
		stdev_rt_abs.append(stdev(times_abs))
	
	table_out = '№	Context	ART	min RT	max RT	stdev RT	ART\'	min ART\'	max ART\'	stdev ART\'\n'
	out_line = '%d\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n'
	for i in range(len(stimuli)):
		s = out_line % (i + 1, stimuli[i], art[i], min_rt[i], max_rt[i], stdev_rt[i], art_abs[i], min_rt_abs[i], max_rt_abs[i], stdev_rt_abs[i])
		table_out += s
	with open(name + '_out.csv', 'w', encoding='utf-8') as f:
		f.write(table_out)

create_time_info_table(younger_database, 'younger')
create_time_info_table(older_database, 'older')
	
