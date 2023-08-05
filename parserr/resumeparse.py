
from __future__ import division

import logging
import os
import re
from datetime import date

import docx2txt
import pdfplumber
import phonenumbers
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from tika import parser

# load pre-trained model
base_path = os.path.dirname(__file__)

nlp = spacy.load('en_core_web_md')

# initialize matcher with a vocab
# this matcher is only used to search for the name
matcher = Matcher(nlp.vocab)

##
file = os.path.join(base_path, "titles_combined.txt")
file = open(file, "r", encoding='utf-8')
designation = [line.strip().lower() for line in file]
designitionmatcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(text) for text in designation if len(nlp.make_doc(text)) < 10]
designitionmatcher.add("Job title", None, *patterns)

file = os.path.join(base_path, "skills.txt")
file = open(file, "r", encoding='utf-8')
skill = [line.strip().lower() for line in file]
skillsmatcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(text) for text in skill if len(nlp.make_doc(text)) < 10]
skillsmatcher.add("Job title", None, *patterns)


file = os.path.join(base_path, "universities.txt")
file = open(file, "r", encoding='utf-8')
univ = [line.strip().lower() for line in file]
univMatcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(text) for text in univ if len(nlp.make_doc(text)) < 10]
univMatcher.add("University", None, *patterns)

file = os.path.join(base_path, "countries.txt")
file = open(file, "r", encoding='utf-8')
country = [line.strip().lower() for line in file]
countryMatcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(text) for text in country if len(nlp.make_doc(text)) < 10]
countryMatcher.add("Country", None, *patterns)

file = os.path.join(base_path, "programming_languages.txt")
file = open(file, "r", encoding='utf-8')
pro_lang = [line.strip().lower() for line in file]
pro_langMatcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(text) for text in pro_lang if len(nlp.make_doc(text)) < 10]
pro_langMatcher.add("Programming_language", None, *patterns)


file = os.path.join(base_path, "companies.txt")
file = open(file, "r", encoding='utf-8')
company = [line.strip().lower() for line in file]
companyMatcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(text) for text in company if len(nlp.make_doc(text)) < 10]
companyMatcher.add("company", None, *patterns)

class resumeparse(object):
    objective = (
        'career goal',
        'objective',
        'career objective',
        'employment objective',
        'professional objective',
        'career summary',
        'professional summary',
        'summary of qualifications',
        'summary',
        # 'digital'
    )

    work_and_employment = (
        'career profile',
        'employment history',
        'work history',
        'work experience',
        'experience',
        'professional experience',
        'professional background',
        'additional experience',
        'career related experience',
        'related experience',
        'programming experience',
        'freelance',
        'freelance experience',
        'army experience',
        'military experience',
        'military background',
    )

    education_and_training = (
        'academic background',
        'academic experience',
        'programs',
        'courses',
        'related courses',
        'education',
        'qualifications',
        'educational background',
        'educational qualifications',
        'educational training',
        'education and training',
        'training',
        'academic training',
        'professional training',
        'course project experience',
        'related course projects',
        'internship experience',
        'internships',
        'apprenticeships',
        'college activities',
        'certifications',
        'special training',
    )

    skills_header = (
        'credentials',
        'areas of experience',
        'areas of expertise',
        'areas of knowledge',
        'skills',
        "other skills",
        "other abilities",
        'career related skills',
        'professional skills',
        'specialized skills',
        'technical skills',
        'computer skills',
        'personal skills',
        'computer knowledge',
        'technologies',
        'technical experience',
        'proficiencies',
        'languages',
        'language competencies and skills',
        'programming languages',
        'competencies'
    )

    misc = (
        'activities and honors',
        'activities',
        'affiliations',
        'professional affiliations',
        'associations',
        'professional associations',
        'memberships',
        'professional memberships',
        'athletic involvement',
        'community involvement',
        'refere',
        'civic activities',
        'extra-Curricular activities',
        'professional activities',
        'volunteer work',
        'volunteer experience',
        'additional information',
        'interests'
    )

    accomplishments = (
        'achievement',
        'licenses',
        'presentations',
        'conference presentations',
        'conventions',
        'dissertations',
        'exhibits',
        'papers',
        'publications',
        'professional publications',
        'research',
        'research grants',
        'project',
        'research projects',
        'personal projects',
        'current research interests',
        'thesis',
        'theses',
    )

    def convert_docx_to_txt(docx_file, docx_parser):
        try:
            if docx_parser == "tika":
                text = parser.from_file(docx_file, service='text')['content']
            elif docx_parser == "docx2txt":
                text = docx2txt.process(docx_file)
            else:
                logging.error('Choose docx_parser from tika or docx2txt ::  is not supported')
                return [], " "
        except RuntimeError as e:
            logging.error('Error in tika installation:: ' + str(e))
            logging.error('--------------------------')
            logging.error('Install java for better result ')
            text = docx2txt.process(docx_file)
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "
        try:
            clean_text = re.sub(r'\n+', '\n', text)
            clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if
                            line.strip()]  # Remove empty strings and whitespaces
            return resume_lines, text
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "

    def convert_pdf_to_txt(pdf_file):
        try:

            raw_text = parser.from_file(pdf_file, service='text')['content']
        except RuntimeError as e:
            logging.error('Error in tika installation:: ' + str(e))
            logging.error('--------------------------')
            logging.error('Install java for better result ')
            pdf = pdfplumber.open(pdf_file)
            raw_text = ""
            for page in pdf.pages:
                raw_text += page.extract_text() + "\n"
            pdf.close()
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "
        try:
            full_string = re.sub(r'\n+', '\n', raw_text)
            full_string = full_string.replace("\r", "\n")
            full_string = full_string.replace("\t", " ")

            # Remove awkward LaTeX bullet characters

            full_string = re.sub(r"\uf0b7", " ", full_string)
            full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
            full_string = re.sub(r'• ', " ", full_string)

            # Split text blob into individual lines
            resume_lines = full_string.splitlines(True)

            # Remove empty strings and whitespaces
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]

            return resume_lines, raw_text
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "

    def find_segment_indices(string_to_search, resume_segments, resume_indices):
        for i, line in enumerate(string_to_search):

            if line[0].islower():
                continue

            header = line.lower()

            if [o for o in resumeparse.objective if header.startswith(o)]:
                try:
                    resume_segments['objective'][header]
                except:
                    resume_indices.append(i)
                    header = [o for o in resumeparse.objective if header.startswith(o)][0]
                    resume_segments['objective'][header] = i
            elif [w for w in resumeparse.work_and_employment if header.startswith(w)]:
                try:
                    resume_segments['work_and_employment'][header]
                except:
                    resume_indices.append(i)
                    header = [w for w in resumeparse.work_and_employment if header.startswith(w)][0]
                    resume_segments['work_and_employment'][header] = i
            elif [e for e in resumeparse.education_and_training if header.startswith(e)]:
                try:
                    resume_segments['education_and_training'][header]
                except:
                    resume_indices.append(i)
                    header = [e for e in resumeparse.education_and_training if header.startswith(e)][0]
                    resume_segments['education_and_training'][header] = i
            elif [s for s in resumeparse.skills_header if header.startswith(s)]:
                try:
                    resume_segments['skills'][header]
                except:
                    resume_indices.append(i)
                    header = [s for s in resumeparse.skills_header if header.startswith(s)][0]
                    resume_segments['skills'][header] = i
            elif [m for m in resumeparse.misc if header.startswith(m)]:
                try:
                    resume_segments['misc'][header]
                except:
                    resume_indices.append(i)
                    header = [m for m in resumeparse.misc if header.startswith(m)][0]
                    resume_segments['misc'][header] = i
            elif [a for a in resumeparse.accomplishments if header.startswith(a)]:
                try:
                    resume_segments['accomplishments'][header]
                except:
                    resume_indices.append(i)
                    header = [a for a in resumeparse.accomplishments if header.startswith(a)][0]
                    resume_segments['accomplishments'][header] = i

    def slice_segments(string_to_search, resume_segments, resume_indices):
        resume_segments['contact_info'] = string_to_search[:resume_indices[0]]

        for section, value in resume_segments.items():
            if section == 'contact_info':
                continue

            for sub_section, start_idx in value.items():
                end_idx = len(string_to_search)
                if (resume_indices.index(start_idx) + 1) != len(resume_indices):
                    end_idx = resume_indices[resume_indices.index(start_idx) + 1]

                resume_segments[section][sub_section] = string_to_search[start_idx:end_idx]

    def segment(string_to_search):
        resume_segments = {
            'objective': {},
            'work_and_employment': {},
            'education_and_training': {},
            'skills': {},
            'accomplishments': {},
            'misc': {}
        }

        resume_indices = []

        resumeparse.find_segment_indices(string_to_search, resume_segments, resume_indices)
        if len(resume_indices) != 0:
            resumeparse.slice_segments(string_to_search, resume_segments, resume_indices)
        else:
            resume_segments['contact_info'] = []

        return resume_segments

    def calculate_experience(resume_text):

        def correct_year(result):
            if len(result) < 2:
                if int(result) > int(str(date.today().year)[-2:]):
                    result = str(int(str(date.today().year)[:-2]) - 1) + result
                else:
                    result = str(date.today().year)[:-2] + result
            return result

        # try:
        experience = 0
        start_month = -1
        start_year = -1
        end_month = -1
        end_year = -1

        not_alpha_numeric = r'[^a-zA-Z\d]'
        number = r'(\d{2})'

        months_num = r'(01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)'
        months_short = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
        months_long = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'
        month = r'(' + months_num + r'|' + months_short + r'|' + months_long + r')'
        regex_year = r'((20|19)(\d{2})|(\d{2}))'
        year = regex_year
        start_date = month + not_alpha_numeric + r"?" + year

        # end_date = r'((' + number + r'?' + not_alpha_numeric + r"?" + number + not_alpha_numeric + r"?" + year + r')|(present|current))'
        end_date = r'((' + number + r'?' + not_alpha_numeric + r"?" + month + not_alpha_numeric + r"?" + year + r')|(present|current|till date|today))'
        longer_year = r"((20|19)(\d{2}))"
        year_range = longer_year + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))" + r'(' + longer_year + r'|(present|current|till date|today))'
        date_range = r"(" + start_date + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))" + end_date + r")|(" + year_range + r")"

        regular_expression = re.compile(date_range, re.IGNORECASE)

        regex_result = re.search(regular_expression, resume_text)

        while regex_result:

            try:
                date_range = regex_result.group()
                # print(date_range)
                # print("*"*100)
                try:

                    year_range_find = re.compile(year_range, re.IGNORECASE)
                    year_range_find = re.search(year_range_find, date_range)
                    # print("year_range_find",year_range_find.group())

                    # replace = re.compile(r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))", re.IGNORECASE)
                    replace = re.compile(r"((\s*to\s*)|" + not_alpha_numeric + r"{1,4})", re.IGNORECASE)
                    replace = re.search(replace, year_range_find.group().strip())
                    # print(replace.group())
                    # print(year_range_find.group().strip().split(replace.group()))
                    start_year_result, end_year_result = year_range_find.group().strip().split(replace.group())
                    # print(start_year_result, end_year_result)
                    # print("*"*100)
                    start_year_result = int(correct_year(start_year_result))
                    if (end_year_result.lower().find('present') != -1 or
                            end_year_result.lower().find('current') != -1 or
                            end_year_result.lower().find('till date') != -1 or
                            end_year_result.lower().find('today') != -1):
                        end_month = date.today().month  # current month
                        end_year_result = date.today().year  # current year
                    else:
                        end_year_result = int(correct_year(end_year_result))


                except Exception as e:
                    # logging.error(str(e))
                    start_date_find = re.compile(start_date, re.IGNORECASE)
                    start_date_find = re.search(start_date_find, date_range)

                    non_alpha = re.compile(not_alpha_numeric, re.IGNORECASE)
                    non_alpha_find = re.search(non_alpha, start_date_find.group().strip())

                    replace = re.compile(start_date + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))", re.IGNORECASE)
                    replace = re.search(replace, date_range)
                    date_range = date_range[replace.end():]

                    start_year_result = start_date_find.group().strip().split(non_alpha_find.group())[-1]
                    start_year_result = int(correct_year(start_year_result))

                    if date_range.lower().find('present') != -1 or date_range.lower().find('current') != -1:
                        end_month = date.today().month  # current month
                        end_year_result = date.today().year  # current year
                    else:
                        end_date_find = re.compile(end_date, re.IGNORECASE)
                        end_date_find = re.search(end_date_find, date_range)

                        end_year_result = end_date_find.group().strip().split(non_alpha_find.group())[-1]

                        try:
                            end_year_result = int(correct_year(end_year_result))
                        except Exception as e:
                            logging.error(str(e))
                            end_year_result = int(re.search("\d+", correct_year(end_year_result)).group())

                if (start_year == -1) or (start_year_result <= start_year):
                    start_year = start_year_result
                if (end_year == -1) or (end_year_result >= end_year):
                    end_year = end_year_result

                resume_text = resume_text[regex_result.end():].strip()
                regex_result = re.search(regular_expression, resume_text)
            except Exception as e:
                logging.error(str(e))
                resume_text = resume_text[regex_result.end():].strip()
                regex_result = re.search(regular_expression, resume_text)

        return end_year - start_year  # Use the obtained month attribute

    def get_experience(resume_segments):
        total_exp = 0
        if len(resume_segments['work_and_employment'].keys()):
            text = ""
            for key, values in resume_segments['work_and_employment'].items():
                text += " ".join(values) + " "
            total_exp = resumeparse.calculate_experience(text)
            return total_exp, text
        else:
            text = ""
            for key in resume_segments.keys():
                if key != 'education_and_training':
                    if key == 'contact_info':
                        text += " ".join(resume_segments[key]) + " "
                    else:
                        for key_inner, value in resume_segments[key].items():
                            text += " ".join(value) + " "
            total_exp = resumeparse.calculate_experience(text)
            return total_exp, text
        return total_exp, " "

    def find_phone(text):
        try:
            return list(iter(phonenumbers.PhoneNumberMatcher(text, None)))[0].raw_string
        except:
            try:
                return re.search(
                    r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',
                    text).group()
            except:
                return ""

    def extract_email(text):
        email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None

    def extract_name(resume_text):
        nlp_text = nlp(resume_text)
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'} ,{'POS': 'PROPN' ,"OP" :"?"}]
        matcher.add('NAME', [pattern])

        matches = matcher(nlp_text)

        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text
        return ""

    def extract_university(text):
        universities = []
        __nlp = nlp(text.lower())
        matches = univMatcher(__nlp)
        for match_id, start, end in matches:
            span = __nlp[start:end]
            universities.append(span.text)
        universities = list(set(universities))
        return universities

    def job_designition(text):
        job_titles = []

        __nlp = nlp(text.lower())

        matches = designitionmatcher(__nlp)
        for match_id, start, end in matches:
            span = __nlp[start:end]
            job_titles.append(span.text)
        job_titles = list(set(job_titles))
        return job_titles

    def programming_lang(text):
        prog_languages = []
        __nlp = nlp(text.lower())
        matches = pro_langMatcher(__nlp)
        for match_id, start, end in matches:
            span = __nlp[start:end]
            prog_languages.append(span.text)
        prog_languages = list(set(prog_languages))
        return prog_languages

    def countries(text):
        countries = []

        __nlp = nlp(text.lower())

        matches = countryMatcher(__nlp)
        for match_id, start, end in matches:
            span = __nlp[start:end]
            countries.append(span.text)
        countries = list(set(countries))
        return countries

    def get_company_working(text):
        companies = []
        __nlp = nlp(text.lower())
        matches = companyMatcher(__nlp)
        for match_id, start, end in matches:
            span = __nlp[start:end]
            companies.append(span.text)
        companies = list(set(companies))
        return companies

    def extract_skills(text):

        skills = []

        __nlp = nlp(text.lower())
        # Only run nlp.make_doc to speed things up

        matches = skillsmatcher(__nlp)
        for match_id, start, end in matches:
            span = __nlp[start:end]
            skills.append(span.text)
        skills = list(set(skills))
        return skills



    def read_file(file, docx_parser="tika"):

        file = os.path.join(file)
        if file.endswith('docx') or file.endswith('doc'):
            if file.endswith('doc') and docx_parser == "docx2txt":
                docx_parser = "tika"
                logging.error("doc format not supported by the docx2txt changing back to tika")
            resume_lines, raw_text = resumeparse.convert_docx_to_txt(file, docx_parser)
        elif file.endswith('pdf'):
            resume_lines, raw_text = resumeparse.convert_pdf_to_txt(file)
        elif file.endswith('txt'):
            with open(file, 'r', encoding='latin') as f:
                resume_lines = f.readlines()

        else:
            resume_lines = None
        resume_segments = resumeparse.segment(resume_lines)
        full_text = " ".join(resume_lines)
        email = resumeparse.extract_email(full_text)
        phone = resumeparse.find_phone(full_text)
        name = resumeparse.extract_name(" ".join(resume_segments['contact_info']))
        total_exp, text = resumeparse.get_experience(resume_segments)
        university = resumeparse.extract_university(full_text)
        designition = resumeparse.job_designition(full_text)
        designition = list(dict.fromkeys(designition).keys())
        company_working = resumeparse.get_company_working(full_text)
        skills = resumeparse.extract_skills(full_text)
        prog_langues = resumeparse.programming_lang(full_text)
        countries = resumeparse.countries(full_text)
        return {
            "email": email,
            "phone": phone,
            "name": name,
            "total_exp": total_exp,
            "university": university,
            "designation": designition,
            "companies_worked_at": company_working,
            "programming_languages_frameworks": prog_langues,
            "skills": skills,
            "countries": countries
        }
