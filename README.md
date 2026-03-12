# data_downloader_agent

A Python script that downloads a set of pre-configured files from SharePoint sharing links and saves them into a local `downloads/` directory.

## Files downloaded

| Description | Filename |
|---|---|
| eSetup Easergy Pro software | `eSetup Easergy Pro V4.11.0 Installer.exe` |
| P3U30 relay manual | `P3U_ANSI_M_30-208A_web.pdf` |
| P3U30 catalogue | `P3U30_CATALOGUE_.pdf` |
| P5 relay manual | `P5_EN_M_02-503A Jan '26.pdf` |
| P5 relay catalogue | `P5_NRJED313567EN_Feb'26_Web.pdf` |
| P5T30-BACD-JABAA-BAEA order form | `P5T30-BACD-JABAA-BAEA.pdf` |

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the downloader:
   ```bash
   python download_files.py
   ```

Downloaded files will appear in the `downloads/` directory.

## Configuration

The list of files and their SharePoint sharing URLs is stored in `downloads_config.json`.  
To add or remove files, edit that file and re-run the script.