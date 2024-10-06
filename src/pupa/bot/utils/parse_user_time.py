from datetime import datetime, time

FORMATS = [
	"%H:%M",
	"%H %M",
	"%H%M",

]


def parse_user_time(time_string: str) -> time | None:
	for fmt in FORMATS:
		try:
			parsed_datetime = datetime.strptime(time_string, fmt)
			return parsed_datetime.time()
		except ValueError as e:
			continue

	return None


print(parse_user_time('1620').hour)