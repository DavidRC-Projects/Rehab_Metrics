import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SPREADSHEET = GSPREAD_CLIENT.open("rehab_metrics")

def get_rom_timeline_assessment(rom_degrees, choice, days_since_surgery):
    """
    This function evaluates ROM based on recovery timeline.
    """
    try:
        weeks = days_since_surgery // 7
        user_rom = rom_degrees[choice]
        
        if weeks <= 2:  # Week 0-2
            if user_rom <= 89:
                return "Your ROM is poor for Week 0-2. Consider consulting your healthcare provider."
            elif user_rom == 90:
                return "Your ROM is good for Week 0-2."
            else:
                return "Excellent progress! Your ROM is above expected for Week 0-2."
        
        elif weeks <= 6:  # Week 2-6
            if user_rom <= 90:
                return "Your ROM is poor for Week 2-6. Consider consulting your healthcare provider."
            elif 91 <= user_rom <= 99:
                return "Your ROM is good for Week 2-6."
            else:
                return "Excellent progress! Your ROM is above expected for Week 2-6."
        
        elif weeks <= 12:  # Week 6-12
            if user_rom <= 95:
                return "Your ROM is poor for Week 6-12. Consider consulting your healthcare provider."
            elif 95 <= user_rom <= 99:
                return "Your ROM is good for Week 6-12."
            else:
                return "Excellent progress! Your ROM is above expected for Week 6-12."
        
        else:  # Week 12+
            if user_rom <= 100:
                return "Your ROM is poor for Week 12+. Consider consulting your healthcare provider."
            elif 101 <= user_rom <= 119:
                return "Your ROM is good for Week 12+."
            else:
                return "Excellent progress! Your ROM has reached optimal levels."
    
    except Exception as e:
        return "Unable to assess ROM against timeline."

def get_pain_timeline_assessment(pain_level, days_since_surgery):
    """
    This function evaluates pain levels based on recovery timeline.
    """
    try:
        weeks = days_since_surgery // 7
        pain = int(pain_level)
        
        if weeks <= 2:  # Week 0-2
            if pain >= 7:
                return "Your pain level is high for Week 0-2. This is normal but monitor closely and consult your healthcare provider if it worsens."
            elif 4 <= pain <= 6:
                return "Your pain level is typical for Week 0-2. Continue following your pain management plan."
            else:
                return "Your pain level is well controlled for Week 0-2. Excellent progress!"
        
        elif weeks <= 6:  # Week 2-6
            if pain >= 6:
                return "Your pain level is higher than expected for Week 2-6. Consider consulting your healthcare provider."
            elif 3 <= pain <= 5:
                return "Your pain level is typical for Week 2-6. Continue your prescribed exercises and pain management."
            else:
                return "Your pain is well managed for Week 2-6. Keep up the good work!"
        
        elif weeks <= 12:  # Week 6-12
            if pain >= 5:
                return "Your pain level is concerning for Week 6-12. Please consult your healthcare provider."
            elif 2 <= pain <= 4:
                return "Your pain level is typical for Week 6-12. Continue your rehabilitation program."
            else:
                return "Excellent pain management for Week 6-12. Keep up with your exercises!"
        
        else:  # Week 12+
            if pain >= 4:
                return "Your pain level is higher than expected after Week 12. Consider consulting your healthcare provider."
            elif pain == 2 or pain == 3:
                return "Your pain level is typical for this stage. Continue monitoring and exercising as prescribed."
            else:
                return "Excellent pain management! Continue your maintenance exercises."
    
    except Exception as e:
        return "Unable to assess pain level against timeline."
