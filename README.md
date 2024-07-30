# Watch Technology

## Overview

This project automates the collection and analysis of cybersecurity articles. It features a web scraper that extracts article data, a LLaMA-based model for summarizing and generating recommendations, and a structured approach for organizing the data into security bulletins.

## Features

- **Web Scraping**: Collects articles from specified websites.
- **Data Processing**: Uses LLaMA for summarizing and generating actionable recommendations.
- **Structured Output**: Saves data in CSV and Excel formats for easy analysis.
## API Tokens

This project uses tokens for accessing certain services, including Hugging Face APIs. For security reasons, these tokens should not be included in the repository.

### Setting Up Your Tokens

1. **Create a Token**: If you don’t already have a token, you’ll need to create one through the service's website. For example, you can create a Hugging Face token by signing up on [Hugging Face](https://huggingface.co/) and generating a token in your account settings.


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
    python bulletin.py
    ```



## Automation

To automate the script, you can follow the instructions in this [YouTube video](https://www.youtube.com/watch?v=4n2fC97MNac&t=6s).

## License

This project is licensed under the MIT License. See the LICENSE file for details.
