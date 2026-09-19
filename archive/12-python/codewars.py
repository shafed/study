def make_readable(seconds):
    hours = seconds // 3600
    seconds -= hours * 3600
    minutes = seconds // 60
    seconds -= minutes * 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
