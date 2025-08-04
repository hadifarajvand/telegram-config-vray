# Setup Guide for Telegram Configuration Collector

This guide will help you set up the Telegram Configuration Collector on your own GitHub repository.

## Prerequisites

- A GitHub account
- Python 3.11 or higher (for local testing)
- Basic knowledge of Git and GitHub

## Step 1: Fork or Clone the Repository

### Option A: Fork the Repository
1. Go to the original repository: https://github.com/soroushmirzaei/telegram-configs-collector
2. Click the "Fork" button in the top right corner
3. This will create a copy in your GitHub account

### Option B: Clone and Create New Repository
1. Clone the repository locally:
   ```bash
   git clone https://github.com/soroushmirzaei/telegram-configs-collector.git
   cd telegram-configs-collector
   ```
2. Create a new repository on GitHub
3. Update the remote origin:
   ```bash
   git remote set-url origin https://github.com/hadifarajvand/telegram-config-vray.git
   ```

## Step 2: Run the Setup Script

The easiest way to configure the repository is to use the provided setup script:

```bash
python setup.py
```

This script will:
- Ask for your GitHub username and repository name
- Ask for your email and name
- Update all the necessary files automatically

## Step 3: Manual Configuration (Alternative)

If you prefer to configure manually, follow these steps:

### 3.1 Update README.md
The README.md file has been updated with your GitHub username and repository name.

### 3.2 Update GitHub Workflows
Edit the following files and replace the placeholder values:
- `.github/workflows/schedule.yml`
- `.github/workflows/push.yml`

Replace:
- `your-email@example.com` with `hadifarajvand@gmail.com`
- `Your Name` with `Hadi Farajvand`

### 3.3 Create Initial Files
Create these files if they don't exist:

**last update**
```
2024-01-01 00:00:00+03:30
```

**invalid telegram channels.json**
```json
[]
```

**splitted/no-match**
```
#Non-Adaptive Configurations
```

## Step 4: Customize Configuration Files

### 4.1 Telegram Channels
Edit `telegram channels.json` to include the Telegram channel usernames you want to monitor. Example:
```json
[
    "channel1",
    "channel2",
    "channel3"
]
```

### 4.2 Subscription Links
Edit `subscription links.json` to include your preferred subscription sources. The current file includes various public sources, but you can add or remove as needed.

## Step 5: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Step 6: Test Locally (Optional)

You can test the script locally before pushing to GitHub:

```bash
python main.py
```

This will:
- Download the GeoIP database
- Process Telegram channels
- Generate configuration files
- Create the directory structure

## Step 7: Push to GitHub

Commit and push your changes:

```bash
git add .
git commit -m "Initial setup for Telegram Configuration Collector"
git push origin main
```

## Step 8: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. Click "Enable Actions" if prompted
4. The workflows will automatically run on:
   - Schedule: Every hour at 15 minutes past the hour
   - Push: Every time you push changes to the main branch

## Step 9: Verify Setup

After the first run, you should see:
- Various configuration files in the repository
- Organized directories for different protocol types
- Country-based configuration files
- Network and security type files

## Configuration Options

### Customizing the Schedule
To change when the script runs, edit `.github/workflows/schedule.yml` and modify the cron expression:
```yaml
- cron: '15 * * * *'  # Runs at 15 minutes past every hour
```

### Adding Custom Telegram Channels
Edit `telegram channels.json` and add channel usernames (without the @ symbol):
```json
[
    "your_channel_name",
    "another_channel"
]
```

### Adding Custom Subscription Sources
Edit `subscription links.json` and add your preferred subscription URLs:
```json
[
    "https://your-subscription-url.com/config.txt",
    "https://another-source.com/proxies.txt"
]
```

## Troubleshooting

### Common Issues

1. **GitHub Actions not running**
   - Check that Actions are enabled in your repository settings
   - Verify the workflow files are in the correct location (`.github/workflows/`)

2. **Script fails to run**
   - Check the Actions tab for error messages
   - Verify all required files exist
   - Check that the Python version is 3.11 or higher

3. **No configurations generated**
   - Check that the Telegram channels in `telegram channels.json` are valid
   - Verify that the subscription links in `subscription links.json` are accessible
   - Check the "no-match" file for failed configurations

### Getting Help

If you encounter issues:
1. Check the GitHub Actions logs for error messages
2. Review the generated files to see what was processed
3. Test the script locally to debug issues
4. Check the original repository for updates and improvements

## Security Considerations

- The script processes public Telegram channels and subscription links
- No sensitive information is stored or transmitted
- All generated configurations are publicly accessible
- Consider the privacy implications of sharing proxy configurations

## License

This project is based on the original work by Soroush Mirzaei. Please respect the original license and attribution. 