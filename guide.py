def get_rom_timeline_assessment(rom_degrees, choice, days_since_surgery):
    """
    Checks range of motion (ROM) based on weeks since surgery.
    Uses rom_degrees, a dictionary holding ROM values for
    different choices.
    """
    try:
        weeks = days_since_surgery // 7
        user_rom = rom_degrees[choice]
        if weeks <= 2:  # Week 0-2
            if user_rom < 90:
                return (
                    "Your ROM is poor for Week 0-2. "
                    "Consider consulting your healthcare provider."
                )
            elif user_rom == 90:
                return (
                    "Your ROM is good for Week 0-2."
                )
            else:
                return (
                    "Excellent progress! Your ROM is above expected "
                    "for Week 0-2."
                )
        elif weeks <= 6:  # Week 2-6
            if user_rom <= 90:
                return (
                    "Your ROM is poor for Week 2-6. "
                    "Consider consulting your healthcare provider."
                )
            elif user_rom <= 100:
                return (
                    "Your ROM is functional but still needs work "
                    "for Week 2-6."
                )
            else:
                return (
                    "Excellent progress! Your ROM is above expected "
                    "for Week 2-6."
                )
        elif weeks <= 12:  # Week 6-12
            if user_rom <= 90:
                return (
                    "Your ROM is poor for Week 6-12. "
                    "Consider consulting your healthcare provider."
                )
            elif user_rom <= 100:
                return (
                    "Your ROM is functional but still needs work "
                    "for Week 6-12."
                )
            else:
                return (
                    "Excellent progress! Your ROM is above expected "
                    "for Week 6-12."
                )
        else:  # Week 12+
            if user_rom <= 99:
                return (
                    "Your ROM is poor for Week 12+. "
                    "Consider consulting your healthcare provider."
                )
            elif user_rom == 100:
                return (
                    "Your ROM is good but can still improve "
                    "for Week 12+."
                )
            else:
                return (
                    "Excellent progress! Your ROM has reached "
                    "optimal levels for function."
                )
    except Exception:
        return "Unable to assess ROM against timeline."


def get_pain_timeline_assessment(pain_level, days_since_surgery):
    """
    Checks pain level based on weeks since surgery.
    Uses pain_level as the current pain value.
    """
    try:
        weeks = days_since_surgery // 7
        pain = int(pain_level)
        if weeks > 12:  # Week 12+
            if pain >= 5:
                return (
                    "Your pain level is significantly elevated for Week 12+. "
                    "Please consult your healthcare provider."
                )
            elif pain == 4:
                return (
                    "Your pain level is elevated for Week 12+. "
                    "Consider consulting your healthcare provider."
                )
            else:
                return (
                    "Excellent, your pain is well managed. "
                    "Keep doing your exercises to improve function."
                )
        elif weeks <= 2:  # Week 0-2
            if pain >= 8:
                return (
                    "Your pain level is high for Week 0-2. This is normal "
                    "but monitor closely and consult your healthcare "
                    "provider if it worsens or suddenly increases."
                )
            elif 6 <= pain <= 7:
                return (
                    "Your pain level is typical for Week 0-2. "
                    "Continue following your exercise plan."
                )
            elif pain <= 5:
                return (
                    "Your pain level is well controlled for Week 0-2. "
                    "Excellent progress!"
                )
        elif weeks <= 6:  # Week 2-6
            if pain >= 6:
                return (
                    "Your pain level is higher than expected for Week 2-6. "
                    "Consider consulting your healthcare provider."
                )
            elif pain == 5:
                return (
                    "Your pain level is typical for Week 2-6. "
                    "Continue your prescribed exercises."
                )
            else:
                return (
                    "Your pain is well managed for Week 2-6. "
                    "Keep up the good work!"
                )
        else:  # Week 6-12
            if pain >= 6:
                return (
                    "Your pain level is concerning for Week 6-12. "
                    "Please consult your healthcare provider."
                )
            elif pain == 5:
                return (
                    "Your pain level is typical for Week 6-12. "
                    "Continue your exercises."
                )
            else:
                return (
                    "Excellent pain level for Week 6-12. "
                    "Keep up with your exercises!"
                )
    except Exception:
        return "Unable to assess pain level against timeline."


def get_weight_bearing_timeline_assessment(wb_status, days_since_surgery):
    """
    Checks weight bearing status based on weeks since surgery.
    Uses wb_status to describe the current weight bearing level.
    Uses wb_levels dict to map weight bearing status strings to numbers.
    """
    try:
        if days_since_surgery < 0:
            days_since_surgery = 0
        weeks = days_since_surgery // 7
        wb_levels = {
            "0-25% weight-bearing": 1,
            "50-75% weight-bearing": 2,
            "75%+ weight-bearing": 3,
            "100% weight-bearing": 4
        }
        wb_level = wb_levels.get(wb_status)
        if wb_level is None:
            return (
                "Unable to assess weight bearing status: "
                "Invalid data format"
            )
        if weeks < 2:  # Week 0-2
            if wb_level == 1:
                return (
                    "Your weight bearing status is poor."
                    "Please consult your healthcare provider for guidance."
                )
            elif wb_level == 2:
                return (
                    "Your weight bearing is expected. "
                    "Follow your healthcare provider's guidance for "
                    "progression."
                )
            elif wb_level == 3:
                return (
                    "Your weight bearing is progressing well. "
                    "Continue following your exercises."
                )
            else:
                return (
                    "Your weight bearing status is excellent "
                    "for this stage!"
                )
        elif weeks < 6:  # Week 2-6
            if wb_level <= 2:
                return (
                    "Your weight bearing is below expected. "
                    "Please consult your healthcare provider."
                )
            elif wb_level == 3:
                return (
                    "Your weight bearing is below expected. "
                    "Please continue your exercises and consult your "
                    "healthcare provider if this worsens."
                )
            else:
                return (
                    "Excellent progress! Your weight bearing "
                    "is advancing well."
                )
        elif weeks < 12:  # Week 6-12
            if wb_level <= 2:
                return (
                    "Your weight bearing is lower than "
                    "expected. Consider consulting your healthcare "
                    "provider."
                )
            elif wb_level == 3:
                return (
                    "Your weight bearing is below expected. "
                    "Please continue your exercises and consult your "
                    "healthcare provider if this worsens."
                )
            else:
                return (
                    "Excellent! Your weight bearing status "
                    "is appropriate."
                )
        else:  # Week 12+
            if wb_level <= 3:
                return (
                    "Your weight bearing is lower than "
                    "expected. Consider consulting your healthcare "
                    "provider."
                )
            else:
                return (
                    "Excellent! You have achieved full "
                    "weight bearing status keep up the good work!."
                )
    except Exception:
        return (
            "Unable to assess weight bearing status: "
            "Invalid data format"
        )
