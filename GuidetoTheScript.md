# Website Blocker Script

## Running the Script in the Background

### 1. Create a `.plist` File

Create a `.plist` file in `~/Library/LaunchAgents/` (e.g., `com.user.websiteblocker.plist`) with the following content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.websiteblocker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/your/script.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>

```

### 2. Load the Service

Load the service using `launchctl`:

`launchctl load ~/Library/LaunchAgents/com.user.websiteblocker.plist`

### 3. Verify the Service

Check if the service is running:

`launchctl list | grep com.user.websiteblocker`
