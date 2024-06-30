### README File

# LinkedIn Job Scraper

This tool automates the process of logging into LinkedIn, searching for jobs, and extracting job posting information in the past 24 hours using Python and Selenium.
https://github.com/AbhijitChallapalli/Jobs_Scrapping/assets/83178772/e2b7c345-c218-4425-b257-85e78f01781a
## Setup Instructions

### 1. Create a Virtual Environment
First, create a virtual environment to manage the project's dependencies separately from other Python projects.
```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment
Activate the virtual environment:
```bash
source venv/bin/activate
```

### 3. Install Dependencies
Install all the necessary dependencies listed in the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Install Google Chrome
Download and install Google Chrome for Linux:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
# Fix any dependency errors
sudo apt-get install -f
```

### 5. Check Chrome Installation
Verify that Google Chrome is correctly installed:
```bash
google-chrome --version
```

### 6. Set Up Chrome Driver
Download the appropriate version of ChromeDriver for your system and ensure it's executable:
```bash
wget https://chromedriver.storage.googleapis.com/<version>/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
```

### 7. Configure Environment Variables
Create an `.env` file to securely store your LinkedIn credentials:
```bash
echo "LINKEDIN_USER=username" >> .env
echo "LINKEDIN_PASS=password" >> .env
```

or 

```bash
LINKEDIN_USER=username
LINKEDIN_PASS=password
```

### 8. Run the Scraper
Finally, execute the scraper to start collecting job postings:
```bash
python jobs.py
```

## Output
The scraper will output a CSV file containing the job postings from the past 24 hours based on your specified keywords.

## Contributions
Contributions are welcome! Please fork the repository and submit pull requests with any enhancements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
