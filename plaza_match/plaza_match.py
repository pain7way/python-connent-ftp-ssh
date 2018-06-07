
# coding: utf-8

# In[22]:


#step1
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
info_site = pd.read_csv('./gc/ENGINEE_SITE.csv')
cf_company = pd.read_csv('./gc/budget_cf_company.csv')
bf_service = pd.read_csv('./gc/MERCHANT_PLAZAINFO.csv')
w_org_ds = pd.read_csv('./gc/field_w_org_ds.csv')
tpm_project = pd.read_csv('./gc/entactmgt_tpm_project.csv')
bf_plaza = pd.read_csv('./gc/lease_bf_plaza.csv')
pos_ods = pd.read_csv('./gc/PASSENGERODS_PLAZAINFO.csv')
pos_dim = pd.read_csv('./gc/PASSENGER_DIMPLAZA.csv')

info_site['enginee_site_cleaan.kydate']=pd.to_datetime(info_site['enginee_site_cleaan.kydate'])
cf_company['budget_cf_company_clean.opendate']=pd.to_datetime(cf_company['budget_cf_company_clean.opendate'])
bf_service['merchant_plazainfo.opendate']=pd.to_datetime(bf_service['merchant_plazainfo.opendate'])
w_org_ds['field_w_org_ds_cleaan.operdate']=pd.to_datetime(w_org_ds['field_w_org_ds_cleaan.operdate'])
tpm_project['entactmgt_tpm_project_clean.opendate']=pd.to_datetime(tpm_project['entactmgt_tpm_project_clean.opendate'])
bf_plaza['lease_bf_plaza_clean.opendate']=pd.to_datetime(bf_plaza['lease_bf_plaza_clean.opendate'])
pos_ods['passengerods_plazainfo.businessstartdate']=pd.to_datetime(pos_ods['passengerods_plazainfo.businessstartdate'])
pos_dim['passenger_dimplaza.opendate']=pd.to_datetime(pos_dim['passenger_dimplaza.opendate'])


info_site['enginee_site_cleaan.description']=info_site['enginee_site_cleaan.description'].apply(lambda x:unicode(x,'utf8'))
cf_company['budget_cf_company_clean.companyname']=cf_company['budget_cf_company_clean.companyname'].apply(lambda x:unicode(x,'utf8'))
bf_service['merchant_plazainfo.plazaname']=bf_service['merchant_plazainfo.plazaname'].apply(lambda x:unicode(str(x),'utf8'))
w_org_ds['field_w_org_ds_cleaan.orgname']=w_org_ds['field_w_org_ds_cleaan.orgname'].apply(lambda x:unicode(str(x),'utf8'))
tpm_project['entactmgt_tpm_project_clean.projectname']=tpm_project['entactmgt_tpm_project_clean.projectname'].apply(lambda x:unicode(str(x),'utf8'))
bf_plaza['lease_bf_plaza_clean.plazaname']=bf_plaza['lease_bf_plaza_clean.plazaname'].apply(lambda x:unicode(x,'utf8'))
pos_ods['passengerods_plazainfo.fullplazaname']=pos_ods['passengerods_plazainfo.fullplazaname'].apply(lambda x:unicode(str(x),'utf8'))
pos_dim['passenger_dimplaza.plazaname']=pos_dim['passenger_dimplaza.plazaname'].apply(lambda x:unicode(str(x),'utf8'))
# In[26]:


#step2
# -*- coding: utf-8
"""
pandas process
"""
import datetime
import sim_model
tree = sim_model.BKTree(sim_model.edit_distance)
#resub_list=['有限','责任','公司','发展','咨询','设计','股份']
resub_list=[]
import re

def safe_unicode(text):
    """
    Attempts to convert a string to unicode format
    """
    # convert to text to be "Safe"!
    if isinstance(text,unicode):
        return text
    else:
        return text.decode('utf-8') 
#sname2taxcode={}
class meta_info():
    def __init__(self, companyname,companyid,companyidvalue,companytable,opendate):
        self.companytable = companytable
        self.companyid = companyid
        self.companyidvalue = companyidvalue
        self.companyname = companyname
        self.opendate=opendate

company_info_dict={}
import re
import string

def add_string(string,resub_list=None):
    c=0
    if resub_list:
        for str_sub in resub_list:
            pat=safe_unicode(str_sub)
            if pat in safe_unicode(string):
                continue
            else:
                c+=1
    #print c
    if c==3:
        return safe_unicode(string+u'万达广场')
    else:
        return safe_unicode(string)
_list=['万达广场','万达茂','酒吧街']

def add_info_tree(table,name,companyid,cn_table,opendate_col):
    if cn_table=='ENGINEE_SITE':
        table_index='1'
    elif cn_table=='budget_cf_company':
        table_index='2'
    elif cn_table=='MERCHANT_PLAZAINFO':
        table_index='3'
    elif cn_table=='field_w_org_ds':
        table_index='4'
    elif cn_table=='entactmgt_tpm_project':
        table_index='5'
    elif cn_table=='lease_bf_plaza':
        table_index='6'
    elif cn_table=='PASSENGERODS_PLAZAINFO':
        table_index='7'
    else:
        table_index='8'
    for i in range(len(table[name])):
        if pd.isnull(table[name][i]):
            continue
        if pd.isnull(table[opendate_col][i]):
            #print table[opendate_col][i]
            table[opendate_col][i]=datetime.datetime.now()
        if isinstance(table[name][i],unicode):
            company_name=add_string(table[name][i],_list)
            #print table[opendate_col][i]
  
            if cn_table in ['PASSENGER_DIMPLAZA','lease_bf_plaza','PASSENGERODS_PLAZAINFO']:
                opendate=pd.to_datetime(str(table[opendate_col][i]).split()[0])
            else:
                opendate=table[opendate_col][i] 
            #print type(company_name)
            #company_name = "hello,world!!%[545]你好234世界。。。"
            company_name2 = re.sub("[A-Za-z0-9\!\%\[\]\,\。\(\)]", "", company_name)
            #print type(company_name)
            tree.add(sim_model.resub_string(company_name2+'_'+table_index,resub_list))
        
            company_info_dict[company_name2+'_'+table_index]=meta_info(table[name][i],companyid,table[companyid][i],cn_table,opendate)
            #COMPANYNAME
        else:
            continue
    
'''
广场表-工程信息化系统SITE   ENGINEE_SITE.csv
'''
add_info_tree(info_site,'enginee_site_cleaan.description','enginee_site_cleaan.siteid','ENGINEE_SITE','enginee_site_cleaan.kydate')
'''
广场表-广场表-全面预算系统CF_COMPANY_new   budget_cf_company.csv
'''
add_info_tree(cf_company,'budget_cf_company_clean.companyname','budget_cf_company_clean.companyid','budget_cf_company','budget_cf_company_clean.opendate')
'''
广场表-商户服务系统PLAZAINFO  MERCHANT_PLAZAINFO.csv
'''
add_info_tree(bf_service,'merchant_plazainfo.plazaname','merchant_plazainfo.plazaid','MERCHANT_PLAZAINFO','merchant_plazainfo.opendate')

'''
广场表-广场表-现场管理系统W_ORG_DS  field_w_org_ds.csv
'''
add_info_tree(w_org_ds,'field_w_org_ds_cleaan.orgname','field_w_org_ds_cleaan.orgid','field_w_org_ds','field_w_org_ds_cleaan.operdate')
'''
广场表-营销企划系统TPM_Project  entactmgt_tpm_project.csv
'''
add_info_tree(tpm_project,'entactmgt_tpm_project_clean.projectname','entactmgt_tpm_project_clean.projectid','entactmgt_tpm_project','entactmgt_tpm_project_clean.opendate')
'''
广场表-租赁系统BF_PLAZA  lease_bf_plaza.csv
'''
add_info_tree(bf_plaza,'lease_bf_plaza_clean.plazaname','lease_bf_plaza_clean.plazaid','lease_bf_plaza','lease_bf_plaza_clean.opendate')

'''
广场表-广场表-POS(ODS)客流系统PlazaInfo   PASSENGERODS_PLAZAINFO.csv
'''

add_info_tree(pos_ods,'passengerods_plazainfo.fullplazaname','passengerods_plazainfo.plazainfoid','PASSENGERODS_PLAZAINFO','passengerods_plazainfo.businessstartdate')

'''
广场表-POS客流系统DimPlaza  PASSENGER_DIMPLAZA.csv
'''
add_info_tree(pos_dim,'passenger_dimplaza.plazaname','passenger_dimplaza.plazaid','PASSENGER_DIMPLAZA','passenger_dimplaza.opendate')


# In[24]:


#step3
#bf_plaza = pd.read_excel('./广场表/广场表-租赁系统BF_PLAZA.xlsx', sheetname=0)
import re
import string
import csv,codecs
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def safe_unicode(text):
    """
    Attempts to convert a string to unicode format
    """
    # convert to text to be "Safe"!
    if isinstance(text,unicode):
        return text
    else:
        return text.decode('utf-8') 

def add_string(string,resub_list=None):
    c=0
    if resub_list:
        for str_sub in resub_list:
            pat=safe_unicode(str_sub)
            if pat in safe_unicode(string):
                continue
            else:
                c+=1
    #print c
    if c==3:
        return safe_unicode(string+u'万达广场')
    else:
        return safe_unicode(string)
_list=['万达广场','万达茂','酒吧街']


def batch_match(input_file,colname,outputfile,opendate_col):
    read=pd.read_csv(input_file)
    read[colname]=read[colname].apply(lambda x:unicode(x,'utf8'))
     

    with codecs.open(outputfile, 'w') as csv_file:
        csv_file.write(codecs.BOM_UTF8)
        writer = csv.writer(csv_file)
        FIELDS = ['NewAdd','归属表名', 'IDname', 'IDvalue', '公司名称','distance','days']
        #先写入columns_name
        writer.writerow(FIELDS)
        #写入多行用writerows
        # 设置列名称
        for i in range(len(read[colname])):
            if pd.isnull(read[colname][i]):
                continue
            if pd.isnull(read[opendate_col][i]):
                read[opendate_col][i]=datetime.datetime.now()
            if isinstance(read[colname][i],unicode):
                #print type(read[colname][i].encode('unicode-escape').decode('string_escape'))
                company_name=add_string(read[colname][i],_list)
                #print type(pd.to_datetime(str(read[opendate_col][i]).split()[0]))
                qurey_date=pd.to_datetime(str(read[opendate_col][i]).split()[0])


                for k,v in list(set(sorted(tree.find(company_name, 1)))):
                    #print type(company_info_dict[v].companyid)
                    #print(type(company_info_dict[v].companyname.encode('utf-8')))
                    table=company_info_dict[v].companytable
                    cid=company_info_dict[v].companyid.decode('utf-8')
                    #print (company_info_dict[v].companyidvalue.astype(str))
                    cvalue=safe_unicode(str(company_info_dict[v].companyidvalue)).decode('utf-8')
                    name=str(company_info_dict[v].companyname.encode('utf-8'))#.decode('utf-8')
                    opendate=company_info_dict[v].opendate
                    #print('北京通州万达广场',table,cid,cvalue,name,k)
                    days_chazhi=qurey_date-opendate
                    days=days_chazhi.days
                    if k<0.17 and abs(days)<1:
                        if u'万达城' in company_name:
                            if u'万达城' not in name:
                                continue
                                #print days
                                #writer.writerows([[str(read[colname][i].encode("utf-8")  ),table,cid,cvalue,name,k,days]])
                            #else:
                            #    continue
                        if u'万达茂' in company_name:
                            if u'万达茂' not in name:
                                continue
                                #print days
                                #writer.writerows([[str(read[colname][i].encode("utf-8")  ),table,cid,cvalue,name,k,days]])
                            #else:
                            #    continue
                        if u'酒吧街' in company_name:
                            if u'酒吧街' not in name:
                                continue
                                #print days
                                #writer.writerows([[str(read[colname][i].encode("utf-8")  ),table,cid,cvalue,name,k,days]])
                            #else:
                            #    continue
                        writer.writerows([[str(read[colname][i].encode("utf-8")  ),table,cid,cvalue,name,k,days]])
                    else:
                        continue
            else:
                continue
t1=time.time()
batch_match(u'./gc/budget_cf_company.csv','budget_cf_company_clean.companyname','./Plaza_Match.csv','budget_cf_company_clean.opendate')
t2=time.time()
print(t2-t1)

