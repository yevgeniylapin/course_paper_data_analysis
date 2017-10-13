#используется для анализа данных по эксперименту. сделай два csv файла с выборкой по пожилым и молодым, не забудь про csv со стимулами (с первой строчки), а также про частотный словарь

from math import log
from pymystem3 import Mystem
import pymorphy2
import operator
import re

with open('freqrnc2011.csv', 'r', encoding='utf-8') as f:
        ipms = {i.split('\t')[0]: float(i.split('\t')[2]) for i in f.read().split('\n')[1:-1]}

with open('stimuli.txt', 'r', encoding = 'utf-8') as f:
        stimuli = f.read().split('\n')

'''
1. сделать раздельные сводные таблицы, как последняя –> для пожилых и молодых отдельно

2. посчитать сколько было RT's (НЕ считать время реакции, если нет ответа), их среднее, минимальное, максимальное и stdev

считать чисто по RT и ещё по RT-actual_start, то есть из RT вычитать actual start
- 

3 добавить время реакции во все три итоговые таблицы (п, м, все)


4. сделать отдельную таблицу со всеми результатами по времени реакции и указанием предложения по м, п и всем
'''

with open('younger_august.csv', 'r', encoding = 'utf-8') as f_y: #вставь название файла про молодых
       younger_database = f_y.read().replace('ё','е').replace('Ё','Е').split('\n')

with open('older_august.csv', 'r', encoding = 'utf-8') as f_o: #вставь название файла про пожилых
       older_database = f_o.read().replace('ё','е').replace('Ё','Е').split('\n')
       
with open('freq_young.csv', 'w', encoding = 'utf-8') as y:
     with open('freq_old.csv', 'w', encoding = 'utf-8') as o:
          with open('freq_all.csv', 'w', encoding = 'utf-8') as all:
               arr_young = []
               arr_young_sorted = []
               time_younger = []
               time_younger_st = []
               for line in younger_database[1:]:
                    line = line.split('\t')
                    s = line[4::4]
                    number_of_younger = len(s)
                    dictionary = {}
                    t = line[5::4]
                    t_st = line[6::4]
                    t_total = 0
                    t_total_abs = 0
                    for i, el in enumerate(s):
                         if el in dictionary:
                              dictionary[el] += 1
                         elif el:
                              dictionary[el] = 1
                         try:
                         	t_total += int(t[i])
                         	try:
                         		t_st[i] = int(t_st[i])
                         	except:
                         		t_st[i] = 0
                         	t_total_abs += (int(t[i]) - int(t_st[i]))
                         except:
                         	continue
                    time_younger.append(t_total)
                    time_younger_st.append(t_total_abs)
                    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse = True)
                    arr_young.append(dictionary)
                    arr_young_sorted.append(sorted_dictionary)                    
               i = 1
               all_answers_young = []
               for dictionary in arr_young_sorted:
                    to_write = str(i)+'\t'
                    all_answers_young_to_write = ''
                    for element in dictionary:
                         to_write = to_write + element[0] + ' ' + str(element[1]) + '\t'
                    for element in dictionary:
                         all_answers_young_to_write = all_answers_young_to_write + element[0] + ' '+ str(element[1]) + ', '
                    all_answers_young.append(all_answers_young_to_write.strip(', '))
                    to_write = to_write.strip('\t')+'\n'
                    y.write(to_write)
                    i += 1
               
               
               arr_old = []
               arr_old_sorted = []
               time_older = []
               time_older_st = []
               for line in older_database[1:]:
                    line = line.split('\t')
                    s = line[4::4]
                    number_of_older = len(s)
                    dictionary = {}
                    t = line[5::4]
                    t_st = line[6::4]
                    t_total = 0
                    t_total_abs = 0
                    for i, el in enumerate(s):
                         if el in dictionary:
                              dictionary[el] += 1
                         elif el:
                              dictionary[el] = 1
                         try:
                         	t_total += int(t[i])
                         	try:
                         		t_st[i] = int(t_st[i])
                         	except:
                         		t_st[i] = 0
                         	t_total_abs += (int(t[i]) - int(t_st[i]))
                         except:
                         	continue
                    time_older.append(t_total)
                    time_older_st.append(t_total_abs)
                    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse = True)
                    arr_old.append(dictionary)
                    arr_old_sorted.append(sorted_dictionary)
               i = 1
               all_answers_old = []
               for dictionary in arr_old_sorted:
                    to_write = str(i)+'\t'
                    all_answers_old_to_write = ''
                    for element in dictionary:
                         to_write = to_write + element[0] + ' ' + str(element[1]) + '\t'
                    for element in dictionary:
                         all_answers_old_to_write = all_answers_old_to_write + element[0] + ' '+ str(element[1]) + ', '
                    all_answers_old.append(all_answers_old_to_write.strip(', '))
                    to_write = to_write.strip('\t')+'\n'
                    o.write(to_write)
                    i += 1

               total_number = number_of_older + number_of_younger
               
               arr_all = []
               arr_all_sorted = []
               time = [time_younger[i] + time_older[i] for i in range(len(time_younger))]
               time_st = [time_younger_st[i] + time_older_st[i] for i in range(len(time_younger))]
               for i, sent in enumerate(arr_young):
                    all_dict = sent
                    for el in arr_old[i]:
                         if el in all_dict:
                              all_dict[el] += arr_old[i][el]
                         else:
                              all_dict[el] = arr_old[i][el]
                    arr_all.append(all_dict)
               i = 1
               for dictionary in arr_all:
                    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse = True)
                    arr_all_sorted.append(sorted_dictionary)

                          

               i = 1
               all_answers = []
               for dictionary in arr_all_sorted:
                    to_write = str(i)+'\t'
                    all_answers_to_write = ''
                    for element in dictionary:
                         to_write = to_write + element[0] + ' ' + str(element[1]) + '\t'
                    for element in dictionary:
                         all_answers_to_write = all_answers_to_write + element[0] + ' '+ str(element[1]) + ', '
                    all_answers.append(all_answers_to_write.strip(', '))
                    to_write = to_write.strip('\t')+'\n'                        
                    all.write(to_write.strip(','))
                    i += 1

vow = ['у','е','о','ы','а','э','я','и','ю']
m = Mystem()
with open('freq_all.csv', 'r', encoding = 'utf-8') as f:
	table = f.read().split('\n')

table_out = '№	Context	Dominant response	Number of completions	Ommitted completions or no completion	Number of unique responses	Alternative completions	Percentage of ending agreement %EA	H-statistic	Frequency (ipm)	Number of syllables	ART	ART\'\n'

for z, line in enumerate(table[:-1]):
	number = line.split('\t')[0]
	values = line[len(number)+1:]
	regex = re.findall('\t?(.*?) (\d[0-9]*)', values)
	values = dict(v for v in regex)

	S = 0
	
	max_k = 0
	values_line = ''

	H = 0

	for k in values:
		S += int(values[k])
		if int(values[k]) >= int(max_k):
			max_k = values[k]
			max_kk = k
		values_line += k + ' ' + values[k]+ '; '
	lemmas = m.lemmatize(max_kk)
	lemmas = "".join(lemmas).strip('\n')
				 
	for k in values:
		H += int(values[k])/S * log(S/int(values[k]), 2)

	
	if lemmas == 'марк':
		ipm = str(ipms["марка"])
	elif lemmas == 'почтить':
		ipm = str(ipms["почта"])
	elif lemmas == 'печь':
		ipm = str(32.6)
	elif lemmas in ipms:
		ipm = str(ipms[lemmas])
	else:
		ipm = 'NA'
	j = 0
	for i in max_kk:
		if i in vow:
			j += 1
	
	art = time[z] / S
	art_abs = time_st[z] / S

	out_line = '%s\t%s\t%s\t%s\t%d\t%d\t%s\t%f\t%f\t%s\t%d\t%f\t%f\n' % (number, stimuli[z], max_kk, S, int(total_number-S), len(values), all_answers[z], int(values[max_kk])*100/S, H, ipm, j, art, art_abs)
	table_out += out_line
	max_k = 0
	max_k_k = 0

with open('freq_table.csv', 'w', encoding='utf-8') as f:
	f.write(table_out)

with open('freq_young.csv', 'r', encoding = 'utf-8') as f:
	table_young = f.read().split('\n')

table_young_out = '№	Context	Dominant response	Number of completions	Ommitted completions or no completion	Number of unique responses	Alternative completions	Percentage of ending agreement %EA	H-statistic	Frequency (ipm)	Number of syllables	ART	ART\'\n'

for z, line in enumerate(table_young[:-1]):
	number = line.split('\t')[0]
	values = line[len(number)+1:]
	regex = re.findall('\t?(.*?) (\d[0-9]*)', values)
	values = dict(v for v in regex)

	S = 0
	
	max_k = 0
	values_line = ''

	H = 0

	for k in values:
		S += int(values[k])
		if int(values[k]) >= int(max_k):
			max_k = values[k]
			max_kk = k
		values_line += k + ' ' + values[k]+ '; '
	lemmas = m.lemmatize(max_kk)
	lemmas = "".join(lemmas).strip('\n')
				 
	for k in values:
		H += int(values[k])/S * log(S/int(values[k]), 2)

	
	if lemmas == 'марк':
		ipm = str(ipms["марка"])
	elif lemmas == 'почтить':
		ipm = str(ipms["почта"])
	elif lemmas == 'печь':
		ipm = str(32.6)
	elif lemmas in ipms:
		ipm = str(ipms[lemmas])
	else:
		ipm = 'NA'
	j = 0
	for i in max_kk:
		if i in vow:
			j += 1
	
	art = time_younger[z] / S
	art_abs = time_younger_st[z] / S
	print(S)

	out_line = '%s\t%s\t%s\t%s\t%d\t%d\t%s\t%f\t%f\t%s\t%d\t%f\t%f\n' % (number, stimuli[z], max_kk, S, int(number_of_younger-S), len(values), all_answers_young[z], int(values[max_kk])*100/S, H, ipm, j, art, art_abs)
	table_young_out += out_line
	max_k = 0
	max_k_k = 0

with open('freq_table_young.csv', 'w', encoding='utf-8') as f:
	f.write(table_young_out)
	
with open('freq_old.csv', 'r', encoding = 'utf-8') as f:
	table_old = f.read().split('\n')

table_old_out = '№	Context	Dominant response	Number of completions	Ommitted completions or no completion	Number of unique responses	Alternative completions	Percentage of ending agreement %EA	H-statistic	Frequency (ipm)	Number of syllables	ART	ART\'\n'

for z, line in enumerate(table_old[:-1]):
	number = line.split('\t')[0]
	values = line[len(number)+1:]
	regex = re.findall('\t?(.*?) (\d[0-9]*)', values)
	values = dict(v for v in regex)

	S = 0
	
	max_k = 0
	values_line = ''

	H = 0

	for k in values:
		S += int(values[k])
		if int(values[k]) >= int(max_k):
			max_k = values[k]
			max_kk = k
		values_line += k + ' ' + values[k]+ '; '
	lemmas = m.lemmatize(max_kk)
	lemmas = "".join(lemmas).strip('\n')
				 
	for k in values:
		H += int(values[k])/S * log(S/int(values[k]), 2)

	
	if lemmas == 'марк':
		ipm = str(ipms["марка"])
	elif lemmas == 'почтить':
		ipm = str(ipms["почта"])
	elif lemmas == 'печь':
		ipm = str(32.6)
	elif lemmas in ipms:
		ipm = str(ipms[lemmas])
	else:
		ipm = 'NA'
	j = 0
	for i in max_kk:
		if i in vow:
			j += 1
	
	art = time_older[z] / S
	art_abs = time_older_st[z] / S
	print(S)


	out_line = '%s\t%s\t%s\t%s\t%d\t%d\t%s\t%f\t%f\t%s\t%d\t%f\t%f\n' % (number, stimuli[z], max_kk, S, int(number_of_older-S), len(values), all_answers_old[z], int(values[max_kk])*100/S, H, ipm, j, art, art_abs)
	table_old_out += out_line
	max_k = 0
	max_k_k = 0

with open('freq_table_old.csv', 'w', encoding='utf-8') as f:
	f.write(table_old_out)