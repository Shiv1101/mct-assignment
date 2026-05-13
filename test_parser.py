from services.csv_parser import parse_csv, calculate_metrics

with open("sample_data/sample.csv", "r") as f:
    content = f.read()

data = parse_csv(content)
margin, runway, wc = calculate_metrics(data)

print("Parsed Data:", data)
print("Gross Margin:", margin)
print("Runway Days:", runway)
print("Working Capital:", wc)