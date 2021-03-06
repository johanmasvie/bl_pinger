import bs4, requests, pickle, time

# Reading list from file
def file_to_list(file):
    list = []
    try:
        file = open(file, 'rb')
        list = pickle.load(file)
    except EOFError:
        list = []
    file.close()
    return list

# Writing list to file
def list_to_file(file, list):

    file = open(file, 'wb')
    pickle.dump(list, file)
    file.close()

# Sending email and push notification
def bl_alert(company, position, link):
    link = "https://bindeleddet.no/jobs"
    webhook_url = ''
    with open('secrets.txt', 'r') as f:
        webhook_url = f.readline()
    print(webhook_url)
    data = {
        "content"   : f'{position} - {company}',
        "username"  : 'BLPinger',
    }
    result = requests.post(webhook_url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

# Download the page
url = 'https://bindeleddet.no/jobs'
getPage = requests.get(url)
getPage.raise_for_status()

# Parse the text for jobs
jobs = bs4.BeautifulSoup(getPage.text, 'html.parser')
internships = jobs.select('div[id$=job-element]')

bl_list = file_to_list('internships.pkl')

for internship in internships:



    position = internship.select('h3')[0].getText()
    company = internship.select('h5')[0].getText()
    link = 'https://bindeleddet.no'

    if (position, company) not in bl_list:
        bl_list.append((position, company))
        bl_alert(company, position, link)
    else:
        continue

list_to_file('internships.pkl', bl_list)