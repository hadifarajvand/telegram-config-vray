# Quick Start Guide

Get your Telegram Configuration Collector up and running in 5 minutes!

## 🚀 Quick Setup

### 1. Fork the Repository
- Go to https://github.com/hadifarajvand/telegram-config-vray
- Click "Fork" in the top right corner
- This creates your own copy

### 2. Run the Setup Script
```bash
git clone https://github.com/hadifarajvand/telegram-config-vray.git
cd telegram-config-vray
python setup.py
```

### 3. Push to GitHub
```bash
git add .
git commit -m "Initial setup"
git push origin main
```

### 4. Enable Actions
- Go to your repository on GitHub
- Click "Actions" tab
- Click "Enable Actions"

That's it! The script will run automatically every hour and generate configuration files.

## 📁 What You'll Get

After the first run, you'll have organized configuration files:

```
├── protocols/
│   ├── vmess
│   ├── vless
│   ├── trojan
│   └── shadowsocks
├── networks/
│   ├── tcp
│   ├── ws
│   └── grpc
├── security/
│   ├── tls
│   └── non-tls
├── countries/
│   ├── us/
│   ├── gb/
│   └── ...
└── splitted/
    ├── mixed
    └── mixed-0 to mixed-9
└── layers/
    ├── ipv4
    ├── ipv6
    └── clash.yaml
```

## 🔧 Customization

### Add Your Own Telegram Channels
Edit `telegram channels.json`:
```json
[
    "your_channel_name",
    "another_channel"
]
```

### Add Your Own Subscription Sources
Edit `subscription links.json`:
```json
[
    "https://your-source.com/config.txt"
]
```

## 📊 Monitoring

- Check the "Actions" tab to see when the script runs
- View generated files in your repository
- Check the "no-match" file for failed configurations

## 🆘 Need Help?

- Read the full [SETUP.md](SETUP.md) for detailed instructions
- Check the [README.md](readme.md) for complete documentation
- Look at the Actions logs if something goes wrong

## ⚡ Pro Tips

1. **Test locally first**: Run `python main.py` to test before pushing
2. **Monitor the logs**: Check Actions tab for any errors
3. **Customize the schedule**: Edit the cron expression in `.github/workflows/schedule.yml`
4. **Add your own sources**: Modify the subscription links for your needs

## 🔒 Security Note

This script processes public Telegram channels and subscription links. All generated configurations are publicly accessible. Consider the privacy implications before sharing. 
