
# coding: utf-8

# In[409]:


#Input & output files path
work_dir = '/Users/qinli/Downloads/'
input_path = work_dir + 'find-political-donors-master/insight_testsuite/tests/test_1/input/itcont.txt' 
Fin = open(input_path,'r')
#Fout_date_path = work_dir + 'find-political-donors-master/insight_testsuite/tests/test_1/output/medianvals_by_date.txt'
#Fout_zip_path = work_dir + 'find-political-donors-master/insight_testsuite/tests/test_1/output/medianvals_by_zip.txt'

Fout_date_path = '/Users/qinli/Downloads/find-political-donors-master/insight_testsuite/temp/output/medianvals_by_date.txt'
Fout_zip_path = '/Users/qinli/Downloads/find-political-donors-master/insight_testsuite/temp/output/medianvals_by_zip.txt'
Fout_date = open(Fout_date_path,'w')
Fout_zip = open(Fout_zip_path,'w')

def searchall(L, value):
    nn = L.count(value)
    ii=[]
    i = -1
    try:
        while 1:
            i = L.index(value, i+1)
            ii.append(i)
    except ValueError:
        pass
    return ii

def construct_array(CUSTOMER_SUMMARY,an):
    a = []
    for line in CUSTOMER_SUMMARY:
        a.append(line[an])
    return a

def calculation_from_same_zipcode(CUSTOMER_SUMMARY):
    zipcode_output = construct_array(CUSTOMER_SUMMARY,1)
    amt_output = construct_array(CUSTOMER_SUMMARY,3)
    id = construct_array(CUSTOMER_SUMMARY,0)
    x = searchall(id,id[-1])
    y = searchall(zipcode_output,zipcode_output[-1])
    same_zip_index = common_elements(x,y)
    summ = sum(list(amt_output[i] for i in same_zip_index))
    median_zipcode = summ / float(len(same_zip_index))
    return (median_zipcode,len(same_zip_index),summ)

def sorted_by_recipient_and_date(CUSTOMER_SUMMARY):
    CUSTOMER_SUMMARY1 = sorted(CUSTOMER_SUMMARY)
    NEW_SUMMARY = []
    i=0
    id = construct_array(CUSTOMER_SUMMARY1,0)
    while i < len(CUSTOMER_SUMMARY1):
        n = len(searchall(id,id[i]))
        ini = (searchall(id,id[i]))[0]
        CUSTOMER_SUMMARY1[ini:ini+n] = sorted(CUSTOMER_SUMMARY1[ini:ini+n], key=lambda x:x[1])
        for j in range(ini,ini+n):
            NEW_SUMMARY.append(CUSTOMER_SUMMARY1[j])
        i += n
    return NEW_SUMMARY

  
def common_elements(list1, list2):
    return [element for element in list1 if element in list2]
    
# main()
CUSTOMER_SUMMARY = []
for line in Fin:
    CUSTOMER_INFO = ['']*5
    info = line.split('|')
    CUSTOMER_INFO[0] = info[0]   # CMTE_ID
    CUSTOMER_INFO[1] = (info[10])[:5] #ZIP_CODE
    CUSTOMER_INFO[2] = info[13] #TRANSACTION_DT
    CUSTOMER_INFO[3] = int(info[14]) #TRANSACTION_AMT
    CUSTOMER_INFO[4] = info[15] #OTHER_ID
    if CUSTOMER_INFO[4] != '':        
        continue
    CUSTOMER_SUMMARY.append(CUSTOMER_INFO)
    # in zipcode
    meridian = int(round((calculation_from_same_zipcode(CUSTOMER_SUMMARY))[0]))
    num_count_zip = int(round((calculation_from_same_zipcode(CUSTOMER_SUMMARY))[1]))
    totaln_zip = int(round((calculation_from_same_zipcode(CUSTOMER_SUMMARY))[2]))
    #write to texts 
    output_zip = CUSTOMER_INFO[0] + '|' + str(CUSTOMER_INFO[1]) + '|' + str(meridian) + '|' + str(num_count_zip) + '|' + str(totaln_zip)
    Fout_zip.write(output_zip)
    Fout_zip.write('\n')      
Fout_zip.close()
# in date
CUSTOMER_SUMMARY1 = sorted_by_recipient_and_date(CUSTOMER_SUMMARY)
date_output = construct_array(CUSTOMER_SUMMARY1,2)
id = construct_array(CUSTOMER_SUMMARY1,0)
amt_output = construct_array(CUSTOMER_SUMMARY1,3)
i=0
while i < len(CUSTOMER_SUMMARY1):
    x = searchall(date_output,date_output[i])
    y = searchall(id,id[i])
    common = common_elements(x,y)
    summ = sum(list(amt_output[j] for j in common))
    totaln_date = int(round(summ))
    meridian = int(round(summ/float(len(common))))
    i += len(common)
    num_count_date = len(common)
    output_date = CUSTOMER_SUMMARY1[x[0]][0] + '|' + str(CUSTOMER_SUMMARY1[x[0]][2]) + '|' + str(meridian) + '|' + str(num_count_date) + '|' + str(totaln_date)
    Fout_date.write(output_date)
    Fout_date.write('\n')  
    #write to texts
Fout_date.close()

