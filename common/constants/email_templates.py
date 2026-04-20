DEFAULT_CAMPAIGN_EMAILS = [
    {
        "sender": "Sarah Jenkins",
        "from_email": "sarah.jenkins@company.com",
        "subject": "Q3 Team Offsite Planning - Please Review",
        "body": "<p>Hi team,</p><p>I have attached the initial draft for our Q3 offsite. Please take a look and let me know if you have any feedback on the proposed schedule.</p><p>We need to lock in the venue by next Friday.</p><p>Best,<br>Sarah</p>",
        "link_text": "",
        "is_phishing": False,
    },
    {
        "sender": "PayPal Support",
        "from_email": "security@paypal.com",
        "subject": "Action Required: Verify Your Account Activity",
        "body": "<p>Dear customer,</p><p>We noticed unusual login activity on your account from an unrecognized device on October 24.</p><p>To prevent permanent suspension of your services, you must verify your identity immediately.</p><p>Please click the secure link below to confirm your recent activity and restore full access to your account.</p><p>Failure to complete this verification within 24 hours will result in account closure.</p><p>Sincerely,<br>The Security Team</p>",
        "link_text": "Verify Your Account",
        "is_phishing": True,
    },
    {
        "sender": "IT Department",
        "from_email": "helpdesk@company.com",
        "subject": "Urgent: Mandatory Software Update Required",
        "body": "<p>Attention all employees,</p><p>A critical security update has been released for all company devices. This update must be installed immediately to maintain network access.</p><p>Please download and install the update from the link below. The installation process will take approximately 10 minutes.</p><p>Update Link: [INSTALL_UPDATE]</p><p>If you experience any issues during installation, contact IT support immediately.</p><p>Thank you,<br>IT Department</p>",
        "link_text": "Install Update Now",
        "is_phishing": True,
    },
]
