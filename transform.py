#используется для анализа данных по эксперименту. сделай два csv файла с выборкой по пожилым и молодым, не забудь про csv со стимулами (с первой строчки), а также про частотный словарь

from math import log
from pymystem3 import Mystem
import pymorphy2
import operator

with open('younger_august.csv', 'r', encoding = 'utf-8') as f_y: #вставь название файла про молодых
       younger_database = f_y.read().split('\n')
with open('older_august.csv', 'r', encoding = 'utf-8') as f_o: #вставь название файла про пожилых
       older_database = f_o.read().split('\n')

with open('freq_young.csv', 'w', encoding = 'utf-8') as y:
     with open('freq_old.csv', 'w', encoding = 'utf-8') as o:
          with open('freq_all.csv', 'w', encoding = 'utf-8') as all:
               arr_young = []
               arr_young_sorted = []
               for line in younger_database[1:]:
                    line = line.split('\t')
                    s = line[4::4]
                    dictionary = {}
                    for el in s:
                         if el in dictionary:
                              dictionary[el] += 1
                         elif el:
                              dictionary[el] = 1
                    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse = True)
                    arr_young.append(dictionary)
                    arr_young_sorted.append(sorted_dictionary)                    
               i = 1
               for dictionary in arr_young_sorted:
                    for element in dictionary:
                         to_write = str(i)+'\t'+str(dictionary[0:])+' \n'
                         to_write = to_write.replace(',',' ')
                         to_write = to_write.replace('[','')
                         to_write = to_write.replace(']','')
                         to_write = to_write.replace('\'','')
                         to_write = to_write.replace(')  (','\t')
                         to_write = to_write.replace(')','')
                         to_write = to_write.replace('(','')
                         to_write = to_write.replace('  ',' ')
                    y.write(to_write)
                    i += 1
               
               
               arr_old = []
               arr_old_sorted = []
               for line in older_database[1:]:
                    line = line.split('\t')
                    s = line[4::4]
                    dictionary = {}
                    for el in s:
                         if el in dictionary:
                              dictionary[el] += 1
                         elif el:
                              dictionary[el] = 1
                    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse = True)
                    arr_old.append(dictionary)
                    arr_old_sorted.append(sorted_dictionary)
               i = 1
               for dictionary in arr_old_sorted:
                    for element in dictionary:
                         to_write = str(i)+'\t'+str(dictionary[0:])+'\n'
                         to_write = to_write.replace(',',' ')
                         to_write = to_write.replace('[','')
                         to_write = to_write.replace(']','')
                         to_write = to_write.replace('\'','')
                         to_write = to_write.replace(')  (','\t')
                         to_write = to_write.replace(')','')
                         to_write = to_write.replace('(','')
                         to_write = to_write.replace('  ',' ')
                    o.write(to_write)
                    i += 1
               
               arr_all = []
               arr_all_sorted = []
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
               for dictionary in arr_all_sorted:
                    for element in dictionary:
                         to_write = str(i)+'\t'+str(dictionary[0:])+'\n'
                         to_write = to_write.replace(',',' ')
                         to_write = to_write.replace('[','')
                         to_write = to_write.replace(']','')
                         to_write = to_write.replace('\'','')
                         to_write = to_write.replace(')  (','\t')
                         to_write = to_write.replace(')','')
                         to_write = to_write.replace('(','')
                         to_write = to_write.replace('  ',' ')                         
                         to_write = to_write.replace('  ',' ')                         
                    all.write(to_write)
                    i += 1


with open('Freq_all.csv', 'r', encoding = 'utf-8') as f:
	table = f.read().split('\n')

with open('stimuli.txt', 'r', encoding = 'utf-8') as f:
	stimuli = f.read().split('\n')
	
table_out = '№	Context	Dominant response	Number of completions	Ommitted completions or no completion	Number of unique responses	Alternative completions	Percentage of ending agreement %EA	H-statistic	Frequency (ipm)	Number of syllables\n'
vow = 'ёуеоыаэяию'

with open('freqrnc2011.csv', 'r', encoding='utf-8') as f:
        ipms = {i.split('\t')[0]: float(i.split('\t')[2]) for i in f.read().split('\n')[1:-1]}

m = Mystem()
for z, line in enumerate(table[:-1]):
	number, values = line.split('\t')[0], line.strip(' ').split('\t')[0:]
	print (number)
	print (values)
	values = dict(v.split() for v in values)
	print(values)

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

	if lemmas in ipms:
		ipm = str(ipms[lemmas])
	elif lemmas == 'марк':
		ipm = str(ipms["марка"])
	elif lemmas == 'почтить':
		ipm = str(ipms["почта"])
	else:
		ipm = 'NA'
	j = 0
	for i in max_k:
		if i in vow:
			j += 1


	out_line = '%s\t%s\t%s\t%s\t%d\t%d\t%s\t%f\t%f\t%s\t%d\n' % (number, stimuli[z], max_kk, S, int(86-S), len(values), values_line, int(values[max_kk])*100/S, H, ipm, j)
	table_out += out_line
	max_k = 0
	max_k_k = 0

with open('freq_table.csv', 'w', encoding='utf-8') as f:
	f.write(table_out)
