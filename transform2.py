from operator import itemgetter
from statistics import mean

with open('freq_table.csv', 'r', encoding='utf-8') as f:
        freq_table = [line.split('\t') for line in f.readlines()]

freq_dict = {title: [] for title in freq_table[0]}
for line in freq_table[1:]:
        for i, val in enumerate(line):
                freq_dict[freq_table[0][i]].append(val)

sentences = [(freq_dict['№'][i], freq_dict['H-statistic'][i]) for i in range(len(freq_dict['Context']))]
easiest = sorted(sentences, key=itemgetter(1))[:25]
easiest = [int(sent[0]) for sent in easiest]
hardest = sorted(sentences, key=itemgetter(1), reverse=True)[:25]
hardest = [int(sent[0]) for sent in hardest]


with open('older_august.csv', 'r', encoding='utf-8') as f:
        file = f.readlines()
        older = [line.split('\t')[5::4] for line in file[1:]]
        older_st = [line.split('\t')[6::4] for line in file[1:]]
        older_person = [[older[sentence][i] for sentence in range(len(older))] for i in range(len(older[0]))]
        # print(len(older_person[0]))
        older_person_st = [[older_st[sentence][i] for sentence in range(len(older_st))] for i in range(len(older_st[0]))]

table_out = 'Subject №\tART easy\tART diff\tART\' easy\tART\' diff\n'
line = '%d\t%f\t%f\t%f\t%f \n'
#print(hardest)
# print(len(older))
for i, person in enumerate(older_person):
                person_easy_values = []
                person_st_easy_values = []
                person_diff_values = []
                person_st_diff_values = []
                # print(easiest)
                for j in range(len(person)):
                                # print(j)
                                if (j + 1) in easiest or (j + 1) in hardest:
                                        try:
                                                val = int(person[j])
                                                # print(person[j])
                                                try:
                                                        val_st = int(older_person_st[i][j])
                                                except:
                                                        val_st = 0
                                                if (j + 1) in easiest:
                                                        person_easy_values.append(val)
                                                        # print(j + 1, 'easy')
                                                        person_st_easy_values.append(val - val_st)
                                                else:
                                                        person_diff_values.append(val)
                                                        # print(j + 1, 'diff')
                                                        person_st_diff_values.append(val - val_st)
                                        except:
                                                continue
                # print(person_easy_values)
                #print(person_easy_values)
                # break
                new_line = line % (i + 1, mean(person_easy_values), mean(person_diff_values), mean(person_st_easy_values), mean(person_st_diff_values))
                table_out += new_line

with open('older_subjects.csv', 'w', encoding='utf-8') as f:
                f.write(table_out)




with open('younger_august.csv', 'r', encoding='utf-8') as f:
        file = f.readlines()
        younger = [line.split('\t')[5::4] for line in file[1:]]
        younger_st = [line.split('\t')[6::4] for line in file[1:]]
        younger_person = [[younger[sentence][i] for sentence in range(len(younger))] for i in range(len(younger[0]))]
        #print(len(younger_person[0]))
        younger_person_st = [[younger_st[sentence][i] for sentence in range(len(younger_st))] for i in range(len(younger_st[0]))]

table_out = 'Subject №\tART easy\tART diff\tART\' easy\tART\' diff\n'
line = '%d\t%f\t%f\t%f\t%f \n'
# print(hardest)
# print(len(younger))
for i, person in enumerate(younger_person):
                person_easy_values = []
                person_st_easy_values = []
                person_diff_values = []
                person_st_diff_values = []
                # print(easiest)
                for j in range(len(person)):
                                # print(j)
                                if (j + 1) in easiest or (j + 1) in hardest:
                                        #if i == 40:
                                                #print(person[j], j+1)
                                        # print(j)
                                        try:
                                                val = int(person[j])
                                                # print(person[j])
                                                try:
                                                        val_st = int(younger_person_st[i][j])
                                                except:
                                                        val_st = 0
                                                if (j + 1) in easiest:
                                                        person_easy_values.append(val)
                                                        # print(j + 1, 'easy')
                                                        person_st_easy_values.append(val - val_st)
                                                else:
                                                        person_diff_values.append(val)
                                                        # print(j + 1, 'diff')
                                                        person_st_diff_values.append(val - val_st)
                                        except:
                                                continue
                # print(person_easy_values)
                #print(person_easy_values)
                # break
                try:
                        new_line = line % (i + 1, mean(person_easy_values), mean(person_diff_values), mean(person_st_easy_values), mean(person_st_diff_values))
                except:
                        new_line = '\n'
                        #print(person)
                table_out += new_line

with open('younger_subjects.csv', 'w', encoding='utf-8') as f:
                f.write(table_out)
