# YouTube Downloader

This Python script allows you to download individual videos and complete playlists from YouTube directly to your computer. It uses the `pytube` library to manage downloads and supports multiple simultaneous downloads through threading, dynamically adapting to the number of CPU cores on your system.

## Features

- Download individual YouTube videos.
- Download complete YouTube playlists.
- Simultaneous downloads using threading based on the number of CPU cores.
- Check if the video already exists in the specified directory and notify accordingly.

## Prerequisites

Before you begin, make sure you have Python installed on your system (Python 3.6 or higher is recommended). Additionally, this script depends on the `pytube` library, which can be installed via pip.

## Installation

To use this script, follow the steps below:

1. Clone this repository using Git:
    ```bash
    git clone https://github.com/Pugn0/YouTube-Downloader.git
    ```
2. Navigate to the cloned directory:
    ```bash
    cd YouTube-Downloader
    ```
3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

After installation, you can run the script directly from the terminal. The script interacts with the user through the terminal to receive necessary inputs (download type, URL, and destination directory).

To start the script, run:
    ```bash
    python script_name.py
    ```

You will be prompted to choose between downloading a video or a complete playlist, provide the corresponding URL, and specify the directory where you want to save the downloaded files.

## Disclaimer

This script is provided for educational and demonstration purposes only. Using scripts to download YouTube videos may violate YouTube's terms of service. It is the user's responsibility to ensure that their use of the script complies with applicable terms and laws.

## Contributions

Contributions to the project are welcome. To contribute, please create a pull request with your suggestions for improvements or fixes.

## License

This project is distributed under the MIT license. See the `LICENSE` file for more details.

## Contact

- GitHub: [Pugn0](https://github.com/Pugn0)
- Telegram: [pugno_fc](https:/t.me/pugno_fc)
