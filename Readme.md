# Phishing URL Detection

This script scans emails for phishing URLs and moves them to the trash if they are deemed malicious. It uses a machine learning model to classify URLs as phishing or not.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/noorgx/NoPhishyZeta.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Obtain a Gmail app password:

   - Go to your Google Account settings.
   - In the "Security" section, select "App passwords."
   - If prompted, sign in to your Google Account.
   - At the bottom, click "Select app" and choose "Mail."
   - Click "Select device" and choose "Other (Custom name)" to name your app.
   - Click "Generate."
   - Follow the instructions to enter the app password (the 16-character code in the yellow bar) on your device.

4. Update the `username` and `password` variables in the script with your Gmail email address and app password.

## Usage

Run the script and enter your Gmail email address and app password when prompted. The script will continuously scan for new emails every minute.

```bash
python app.py
```

## Notes

- This script uses a machine learning model to classify URLs, which may not be 100% accurate. Exercise caution when using the script and review any URLs marked as spam manually if needed.
