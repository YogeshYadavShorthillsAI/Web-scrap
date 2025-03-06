from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://m.timesjobs.com/jobfunction/it-software-jobs').text
# print(html_text)
soup = BeautifulSoup(html_text,'lxml')
# print(soup)
jobs = soup.find_all(class_ = 'srp-job-bx')
# print(jobs.prettify)
with open(f'files/file.txt','w') as f:
    for job in jobs:
        company_name = job.h4.span.text.strip()
        desc = job.h3.text.strip()

        # Extract skills
        skills_container = job.find("div", class_="srp-keyskills")
        skills = [skill.text.strip() for skill in skills_container.find_all("a")] if skills_container else []

        # Extract location, experience, and salary
        loc = job.find("div", class_="srp-loc")
        exp = job.find("div", class_="srp-exp")
        sal = job.find("div", class_="srp-sal")

        loc_text = loc.text.strip() if loc and loc.text.strip() else "N/A"
        exp_text = exp.text.strip() if exp and exp.text.strip() else "N/A"
        sal_text = sal.text.strip() if sal and sal.text.strip() else "N/A"

        # Print extracted data
        print(f"Company Name: {company_name}")
        print(f"Job Title: {desc}")
        print(f"Location: {loc_text}")
        print(f"Experience: {exp_text}")
        print(f"Salary: {sal_text}")
        print("Skills Required:", ", ".join(skills) if skills else "N/A")
        print("-" * 50)
            
        f.write(f"Company Name: {company_name}\n")
        f.write(f"Job Title: {desc}\n")
        f.write(f"Location: {loc_text}\n")
        f.write(f"Experience: {exp_text}\n")
        f.write(f"Salary: {sal_text}\n")
        f.write(f"skills required :")
        for skill in skills:f.write(f'{skill}, ')
        f.write("\n")
        f.write('--'*50)
        f.write("\n")
    f.close() 

        