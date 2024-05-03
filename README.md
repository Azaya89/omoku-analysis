---
title: Power supply dashboard
emoji: 📈
colorFrom: gray
colorTo: green
sdk: docker
pinned: true
---

# Omoku Analysis Dashboard Automation

## Overview
This repository supports the Omoku Analysis Dashboard, which is hosted on Hugging Face Spaces. It's designed to automate the data updating process for the dashboard, ensuring that the displayed data is consistently refreshed from a Google Sheets source. This README provides guidance on how the automation works, how to utilize the repository for similar projects, and how you can contribute to its development.

## Purpose
- **For GitHub Users**: This repository contains scripts, automation workflows (GitHub Actions), and documentation for setting up and managing the dashboard's data pipeline.
- **For Hugging Face Users**: If you're viewing this on Hugging Face Spaces, this repository is where all the backend automation is managed. You can explore how the dashboard data is updated automatically and even adapt the methods for your own projects.

## How It Works
1. **Data Source**: Data is stored and manually updated in a Google Sheet.
2. **Data Processing**:
   - A [Python script](update_data.py) is used to download data from the Google Sheet and convert it to a CSV file.
   - The script is automatically triggered by GitHub Actions to run at a specified time daily.
3. **Automation**:
   - Two main GitHub Actions workflows handle the automation:
     - [One workflow](.github/workflows/update_data_workflow.yml) pulls the latest data from Google Sheets, converts it to CSV, and pushes it to the repository.
     - [The other workflow](.github/workflows/main.yml) pushes updates from the GitHub repository to the Hugging Face Space.

## Dashboard
Access the live dashboard here: [Omoku Analysis Dashboard](https://huggingface.co/spaces/Azaya89/omoku-analysis)

## Getting Started
To set up this project locally or contribute to it, follow these steps:
1. Clone the repository:
   ```
   git clone git@github.com:Azaya89/omoku-analysis.git
   ```
2. Install the required Python libraries:
   ```
   pip install -r requirements.txt
   ```
3. Set up your Google API credentials and save them as `omoku-analysis-cred_key.json`

## Contributing
Contributions to the Omoku Analysis project are welcome! Please consider the following ways to contribute:
- Submit bugs and feature requests.
- Review the source code and enhance the automation scripts.
- Update documentation as the project evolves.

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details.