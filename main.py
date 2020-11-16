import pandas as pd
from statistics import mean
import time
import json
import pycountry_convert as pc

start_time = time.time()

def csv_to_dataframe(filepath):
    try:
        csv_reader = pd.read_csv(filepath)
    except FileNotFoundError:
        print('File Not Found')
        return(None)
    return(csv_reader)


def developer_dataframe(csv_reader):
    try:
        developer_dataframe = csv_reader.loc[(csv_reader['MainBranch'] == 'I am a developer by profession')]
    except:
        print('Provided dataframe is faulty')
        return(None)
    return(developer_dataframe)
    
def generate_country_list(dataframe):
    try:
        country_dataframe = dataframe.loc[dataframe['Country'].notnull()]
    except:
        print('Provided dataframe is faulty')
        return(None)
    country_list = country_dataframe['Country'].tolist()
    unique_country_list = list(set(country_list))
    return(unique_country_list)
    
def continent_classification(unique_country_list):
    
    continent_dict = {}

    if(unique_country_list is None):
        print("Country list is empty")
        return(None)
        
    unique_country_list = list(set(unique_country_list))
    
    continent_code_to_continent = {'AF':'Africa','AS':'Asia','NA':'North America',
                                   'SA':'South America','EU':'Europe','OC':'Oceania'}
    for country in unique_country_list:
        
        try:
            country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
            continent_name = continent_code_to_continent[pc.country_alpha2_to_continent_code(country_code)]
        except:
            print('Country unknown ERROR:',country)
            continue
        
        if continent_name not in continent_dict.keys():
            continent_dict[continent_name] = []
        
        continent_dict[continent_name].append(country)
    
    if('The former Yugoslav Republic of Macedonia' in unique_country_list):
        continent_dict['Europe'].append('The former Yugoslav Republic of Macedonia')
        
    for outlier in ['Hong Kong (S.A.R.)','Republic of Korea','timor-leste']:  
        if(outlier in unique_country_list):
            continent_dict['Asia'].append(outlier)
    
    for outlier in ['Libyan Arab Jamahiriya','Congo, Republic of the...']:  
        if(outlier in unique_country_list):
            continent_dict['Africa'].append(outlier)
            
    if('Venezuela, Bolivarian Republic of...' in unique_country_list):
        continent_dict['South America'].append('Venezuela, Bolivarian Republic of...')
    

    return(continent_dict)
    
def question_one(developer_datagram):
    
    try:
        dev = developer_datagram.loc[developer_datagram['Age1stCode'].notnull()]
    except:
        print('Dataframe with given values is unavailable')
        return(0)
        
    #Arbitrary age taken for categories which do not have a numerical value
#    dev.loc[dev['Age1stCode']=='Younger than 5 years','Age1stCode'] = 4
#    dev.loc[dev['Age1stCode']=='Older than 85','Age1stCode'] = 88
    
    #Categories without numerical age value are removed
    dev = developer_datagram.loc[(developer_datagram['Age1stCode']!='Younger than 5 years')
      &(developer_datagram['Age1stCode'].notnull())
      &(developer_datagram['Age1stCode']!='Older than 85')]
    
    
    #Create a list of ages
    age_list = dev['Age1stCode'].astype(int).tolist()
    #print(age_list)
    
    #Calculating average age
    age_mean = mean(age_list)
        
    return(age_mean)

def question_two(developer_datagram,unique_country_list):
    
    countrywise_data = {}
    
    if(developer_datagram is None):
        print("Empty dataframe")
        return
    elif(len(unique_country_list)==0):
        print("Empty country list")
        return
   
    for country in unique_country_list:
        count = 0
        
        country_datagram = developer_datagram.loc[developer_datagram['Country']==country]
        
        if(country_datagram.empty):
            continue
        
        country_total = len(country_datagram.index)
    
        language_worked_with = country_datagram.loc[country_datagram['LanguageWorkedWith'].notnull()]
        language_list = language_worked_with['LanguageWorkedWith'].tolist()
    
        #Counting occurences of python in each string of languages
        for string in language_list:
            if(string.find('Python')):
                count = count + 1
        
        #Percentage calculation
        countrywise_data[country] = (count/country_total)*100
            
    return(countrywise_data)
    

def question_three(developer_datagram,continent_dict):
    
    
    continent_salary_dict = {}
    
    if(developer_datagram is None):
        print("Empty dataframe")
        return
    elif(not bool(continent_dict)):
        print("Empty Continent Dictionary")
        return
    
    #Calculate the means of salaries by iterating through the continents
    for continent in continent_dict.keys():
        
        #Dataframe created based on the countries in a continent
        continent_datagram = developer_datagram.loc[(developer_datagram['Country'].isin(continent_dict[continent]))
        &(developer_datagram['ConvertedComp'].notnull())]
        
        if(continent_datagram.empty):
            continent_salary_dict[continent]=0
            continue
        
        continent_comp_list = continent_datagram['ConvertedComp'].astype(int).tolist()
        
        salary_mean = mean(continent_comp_list)
        
        continent_salary_dict[continent] = salary_mean
    
    return(continent_salary_dict)


def question_four(csv_reader):
    
    language_count = {}
    
    if(csv_reader is None):
        print("Empty dataframe")
        return
    
    #Obtaining a list of strings containing semi-colon delimited languages
    next_language = csv_reader['LanguageDesireNextYear'].astype(str).tolist()
    
    #Iterating through the list of strings obtained 
    for languages in next_language:
        lang_list = languages.split(';')
        for language in lang_list:
            if(language not in language_count.keys()):
                language_count[language]=1
            else:
                language_count[language] = language_count[language] + 1
    
    #Operation to obtain the key with maximum value
    next_desired_language = max(language_count,key=language_count.get)
    
    
    return(next_desired_language)


def question_five(csv_reader,continent_dict):
    
    continent_gender_hobby = {}
    
    if(csv_reader is None):
        print("Empty dataframe")
        return
    elif(not bool(continent_dict)):
        print("Empty continent dictionary")
        return
    
    for continent in continent_dict.keys():
        continent_datagram_total = csv_reader.loc[csv_reader['Country'].isin(continent_dict[continent])]
        
        man_datagram = continent_datagram_total.loc[continent_datagram_total['Gender']=='Man']
        woman_datagram = continent_datagram_total.loc[continent_datagram_total['Gender']=='Woman']
        others_datagram = continent_datagram_total.loc[~continent_datagram_total['Gender'].isin(['Man','Woman'])]
        
        if(continent not in continent_gender_hobby.keys()):
            continent_gender_hobby[continent]={}
        
        continent_gender_hobby[continent]['Man'] = man_datagram['Hobbyist'].value_counts().to_dict()
        continent_gender_hobby[continent]['Woman'] = woman_datagram['Hobbyist'].value_counts().to_dict()    
        continent_gender_hobby[continent]['Others'] = others_datagram['Hobbyist'].value_counts().to_dict()
    

        
    return(continent_gender_hobby)
    


def question_six(csv_reader,continent_dict):
    career_satisfy = {}
    job_satisfy = {}
    
    if(csv_reader is None):
        print("Empty dataframe")
        return
    elif(not bool(continent_dict)):
        print("Empty continent dictionary")
        return
    
    for continent in continent_dict.keys():
        continent_datagram_total = csv_reader.loc[csv_reader['Country'].isin(continent_dict[continent])]
    
        man_datagram = continent_datagram_total.loc[continent_datagram_total['Gender']=='Man']
        woman_datagram = continent_datagram_total.loc[continent_datagram_total['Gender']=='Woman']
        others_datagram = continent_datagram_total.loc[~continent_datagram_total['Gender'].isin(['Man','Woman'])]
    
        if(continent not in career_satisfy.keys()):
            career_satisfy[continent]={}
            job_satisfy[continent]={}
        
        career_satisfy[continent]['Man'] = man_datagram['CareerSat'].value_counts().to_dict()
        job_satisfy[continent]['Man'] = man_datagram['JobSat'].value_counts().to_dict()
    
        career_satisfy[continent]['Woman'] = woman_datagram['CareerSat'].value_counts().to_dict() 
        job_satisfy[continent]['Woman'] = woman_datagram['JobSat'].value_counts().to_dict()
        
        career_satisfy[continent]['Others'] = others_datagram['CareerSat'].value_counts().to_dict()
        job_satisfy[continent]['Others'] = others_datagram['JobSat'].value_counts().to_dict()
    

    return(job_satisfy,career_satisfy)

def main():
    
    filepath = 'survey_results_public.csv'
    main_dataframe = csv_to_dataframe(filepath)
    developer = developer_dataframe(main_dataframe)
    country_list = generate_country_list(main_dataframe)
    continent_dict = continent_classification(country_list)
    
    print('\nQ1.Find the average age of developers when they wrote their first line of code\n')
    age_mean = question_one(developer)
    print("Average age is: ",age_mean,'\n')

    print('Q2.Deduce the percentage of developers who know python in each country\n')
    countrywise_data = question_two(developer,country_list)
    print(json.dumps(countrywise_data,indent=2))

    
    print('Q3.Generate a report for the average salary of developer based on continent\n')
    continent_salary_dict = question_three(developer,continent_dict)
    print("Average salary of developer based on continent(in USD):\n",json.dumps(continent_salary_dict,indent=2),'\n')

    print('Q4.Based on this survey, what will be the most desired programming language for the year 2020?\n')
    next_desired_language = question_four(main_dataframe)
    print("Most desired language in 2020 is:",next_desired_language,'\n')

    print('Q5.What is the distribution of people who code as a hobby based on gender and continent?\n')
    continent_gender_hobby = question_five(main_dataframe,continent_dict)
    print("Distribution of people who code as a hobby is:\n",json.dumps(continent_gender_hobby,indent=2),'\n')

    print('Q6.Generate the report for job and career satisfaction of developer based on their gender and continent?\n')
    if(question_six(main_dataframe,continent_dict) is not None):    
        job_satisfy,career_satisfy = question_six(main_dataframe,continent_dict)
        print("Job satisfaction is:\n",json.dumps(job_satisfy,indent=2),'\n')
        print("Career satisfaction is:\n",json.dumps(career_satisfy,indent=2),'\n')
    else:
        print(None)
    

if __name__ == '__main__':
    main()
print("\n--- %s seconds ---" % (time.time() - start_time))