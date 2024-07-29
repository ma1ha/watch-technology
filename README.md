# Watch Technology

## Overview

This project automates the collection and analysis of cybersecurity articles. It features a web scraper that extracts article data, a LLaMA-based model for summarizing and generating recommendations, and a structured approach for organizing the data into security bulletins.

## Features

- **Web Scraping**: Collects articles from specified websites.
- **Data Processing**: Uses LLaMA for summarizing and generating actionable recommendations.
- **Structured Output**: Saves data in CSV and Excel formats for easy analysis.

## Automation

To see the project in action, watch the demonstration video on YouTube: [Watch Technology Automation](https://www.youtube.com/watch?v=example)

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/ma1ha/watch-technology.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd watch-technology
    ```

3. **Set Up a Virtual Environment**:

    ```bash
    python -m venv myenv
    ```

4. **Activate the Virtual Environment**:

    - On Windows:

      ```bash
      myenv\Scripts\activate
      ```

    - On Linux/Mac:

      ```bash
      source myenv/bin/activate
      ```

5. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Web Scraper**:

    ```bash
    python scraping_articles.py
    ```

2. **Process Data and Generate Bulletins**:

    ```bash
    python llama.py
    ```






## Automation

To automate the script, you can follow the instructions in this [YouTube video](https://www.youtube.com/watch?v=4n2fC97MNac).

## License

This project is licensed under the MIT License. See the LICENSE file for details.
