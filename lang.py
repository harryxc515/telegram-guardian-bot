LANG = {
    "en": {
        "help": (
            "🤖 Guardian Bot Help\n\n"
            "/on /off – VC protection\n"
            "/status – protection status\n"
            "/stats – group analytics\n"
            "/warnings – check warnings\n"
            "/resetwarnings – reset warnings\n"
            "/whitelist domain\n"
            "/setlang en|hi"
        ),
        "muted": "🔇 Muted for {time} seconds."
    },
    "hi": {
        "help": (
            "🤖 गार्डियन बॉट सहायता\n\n"
            "/on /off – VC सुरक्षा\n"
            "/status – स्थिति\n"
            "/stats – ग्रुप आँकड़े\n"
            "/warnings – चेतावनी\n"
            "/resetwarnings – रीसेट\n"
            "/whitelist domain\n"
            "/setlang en|hi"
        ),
        "muted": "🔇 आपको {time} सेकंड के लिए म्यूट किया गया है।"
    }
}

def t(lang, key, **k):
    return LANG.get(lang, LANG["en"]).get(key, key).format(**k)