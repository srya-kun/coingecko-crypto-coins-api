# coingecko-crypto-coins-api

## Overview

This script is a robust and flexible solution for extracting cryptocurrency market data from the CoinGecko API and storing it in an Excel file. It is designed to be easily configurable, handle errors gracefully, and minimize API usage to stay within rate limits.

## Key Features

*   **Command-Line Interface:** The script is executed from the command line, allowing users to specify the coin IDs for which they want to retrieve data.
*   **Configuration File:** The script uses a configuration file (`config.json`) to store sensitive information such as the CoinGecko API key. This prevents the API key from being hardcoded in the script and makes it easier to manage.
*   **Error Handling:** The script includes comprehensive error handling to catch potential issues such as API request failures, invalid coin IDs, and data validation errors. This ensures that the script runs smoothly and provides informative error messages to the user.
*   **Data Validation:** The script validates the data retrieved from the API to ensure that it is in the expected format. This helps prevent issues when processing the data or training a machine learning model.
*   **Caching:** The script implements caching to store API responses locally. This reduces the number of API requests and improves the script's performance, especially when running the script multiple times with the same coin IDs. The cache expiry time is configurable in the `config.json` file.
*   **Data Transformation:** The script includes data transformation capabilities to allow users to clean and preprocess the data before writing it to the Excel file. This can involve converting data types, removing outliers, or filling in missing values.
*   **Excel Output:** The script writes the extracted data to an Excel file with a sheet for each coin. The sheet name is either the current date in `DD-MM-YYYY` format or the coin ID if only one coin is specified.

## Dependencies

The script requires the following Python libraries:

*   `requests`: For making HTTP requests to the CoinGecko API.
*   `pandas`: For creating and manipulating DataFrames and writing them to Excel files.
*   `argparse`: For parsing command-line arguments.
*   `json`: For reading and writing JSON configuration files.
*   `os`: For interacting with the operating system (e.g., creating directories, checking file existence).
*   `datetime`: For getting the current date and time.
*   `typing`: For type hinting.

To install these libraries, run the following command:

```bash
pip install requests pandas argparse
```

## Configuration

The script requires a configuration file named `config.json` in the same directory as the script. The `config.json` file should contain the following information:

```json
{
  "api_key": "YOUR_API_KEY",
  "cache_expiry": 3600
}
```

*   `api_key`: Your CoinGecko API key.
*   `cache_expiry`: The cache expiry time in seconds (default: 3600 seconds = 1 hour).

## Usage

To run the script, use the following command:

```bash
python coingecko_data_script/main.py <coin_id1> <coin_id2> ...
```

Replace `<coin_id1>`, `<coin_id2>`, etc. with the CoinGecko coin IDs for which you want to retrieve data. For example:

```bash
python coingecko_data_script/main.py bitcoin ethereum
```

This will create an Excel file named `coingecko_data_<today_date>.xlsx` in the same directory as the script, with a sheet for each coin containing the current market data.

## Error Handling

The script includes error handling to gracefully handle various potential issues. If an error occurs, the script will print an informative error message to the console and continue running if possible.

## Caching

The script implements caching to reduce the number of API requests and improve performance. The cache files are stored in a `.cache` directory in the same directory as the script. The cache expiry time is configurable in the `config.json` file.

## Data Transformation

The script includes a `transform_data` function that can be used to clean and preprocess the data before writing it to the Excel file. This function currently performs the following transformations:

*   Converts the `market_cap` column to a float.
*   Converts the `current_price` column to a float.
*   Converts the `total_volume` column to a float and renames it to `volume`.

You can modify this function to perform additional data transformations as needed.

## Senior Developer Notes

As a seasoned developer, I've incorporated several best practices into this script to ensure its reliability, maintainability, and scalability. These include:

*   **Modularity:** The script is divided into several functions, each responsible for a specific task. This makes the code easier to understand, test, and maintain.
*   **Type Hinting:** The script uses type hinting to improve code readability and prevent type-related errors.
*   **Docstrings:** The script includes detailed docstrings for all functions and classes, explaining their purpose, parameters, and return values.
*   **Error Handling:** The script includes comprehensive error handling to gracefully handle potential issues and prevent the script from crashing.
*   **Caching:** The script implements caching to reduce API usage and improve performance.
*   **Configuration File:** The script uses a configuration file to store sensitive information and make it easier to modify the script's behavior without having to edit the code directly.
*   **Command-Line Arguments:** The script uses command-line arguments to allow users to specify the coin IDs for which they want to retrieve data.

By following these best practices, I've created a script that is not only functional but also easy to understand, maintain, and extend. This script is a valuable tool for anyone who needs to extract cryptocurrency market data from the CoinGecko API.
