import json
import xmltodict

def convert_xml_to_json(resp):
    xml_string = resp['response']
    try:
        # Parse the XML string
        parsed_xml = xmltodict.parse(f"<root>{xml_string}</root>")
        # Convert to JSON
        json_data = json.dumps(parsed_xml['root'], indent=2)
        return json_data
    except Exception as e:
        print("An error occurred:", e)
        return {}
