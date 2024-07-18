import re


def clean_value(value):
    cleaned_value = re.sub(r'^[\d,.]+', '', value).strip()
    return cleaned_value


def clean_coin_name(coin_name):
    cleaned_name = coin_name.split(" price\u00a0")[0].strip()
    return cleaned_name


def clean_price_change(value):
    cleaned_value = re.sub(r'\s*\(\d+d\)$', '', value).strip()
    return cleaned_value


def clean_volume_value(value):
    cleaned_value = re.sub(r'[^\d$]', '', value)

    if cleaned_value.startswith('$'):
        cleaned_value = cleaned_value[1:]  # Remove the leading $
        parts = []
        while len(cleaned_value) > 3:
            parts.append(cleaned_value[-3:])
            cleaned_value = cleaned_value[:-3]
        parts.append(cleaned_value)
        cleaned_value = ','.join(reversed(parts))
        cleaned_value = f'${cleaned_value}'  # Add the $ back
        
    return cleaned_value

